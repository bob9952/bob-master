import random
import time
from src.chromosome import Chromosome
from src.heuristic import best_fit, counting_sort

class GeneticAlgorithm:
    def __init__(self, items_dict, bin_size, pop_size=50, generations=100, crossover_prob=0.8, mutation_prob=0.1):
        self.items_dict = items_dict
        self.bin_size = bin_size
        self.pop_size = pop_size
        self.generations = generations
        self.pc = crossover_prob
        self.pm = mutation_prob

        self.gene_pool = list(items_dict.keys())
        self.population = []
        self.best_chromosome = None
        self.history = {'best': [], 'avg': []}

    def _ffd_order(self):
        """Item order that reproduces First-Fit-Decreasing when decoded by
        Chromosome's First-Fit decoder (decreasing size, ties by counting
        sort when all sizes are integers, else a stable Python sort)."""
        keys = self.gene_pool
        all_ints = all(float(self.items_dict[k]).is_integer() for k in keys)
        if all_ints and keys:
            max_val = max(int(self.items_dict[k]) for k in keys)
            return counting_sort(keys, self.items_dict, max_val)
        return sorted(keys, key=lambda k: self.items_dict[k], reverse=True)

    def _bfd_order(self, ffd_order):
        """Item order obtained by flattening the bins that Best-Fit-Decreasing
        would build (item-by-item, bin-by-bin). Decoding this permutation with
        the (First-Fit) chromosome decoder does not exactly reproduce BFD's bin
        count, but it injects BFD's grouping structure as a distinct, high
        quality seed individual for extra population diversity."""
        bfd_bins = best_fit(ffd_order, self.items_dict, self.bin_size)
        order = []
        for b in bfd_bins:
            order.extend(item_id for item_id, _size in b['items'])
        return order

    def _seed_orders(self):
        """Heuristic orderings injected into gen-0 so the GA's First-Fit
        decoder reproduces (at least) FF's and FFD's bin counts immediately.
        Falkenauer's triplet ('t*') instances are a well known adversarial
        case for FFD/BFD (sorting by size destroys the triplet grouping that
        makes plain, unsorted First-Fit near-optimal) -- so we seed the
        *natural* file order (== plain FF) as well as FFD/BFD, rather than
        FFD alone, to guarantee the GA is never worse than the best of FF,
        FFD and the BFD-grouping seed.
        """
        seeds = []
        seen = set()

        def add(order):
            key = tuple(order)
            if order and key not in seen:
                seen.add(key)
                seeds.append(order)

        # 1) Natural / file order == plain First-Fit when decoded by the GA.
        add(self.gene_pool.copy())

        # 2) First-Fit-Decreasing order.
        ffd_order = self._ffd_order()
        add(ffd_order)

        # 3) Best-Fit-Decreasing grouping order (diversity seed).
        add(self._bfd_order(ffd_order))

        return seeds

    def initialize_population(self):
        self.population = []

        # --- Seeding: inject heuristic solutions (FF, FFD, BFD-grouping) ---
        # so the initial population's best individual is never worse than
        # those heuristics. Combined with elitism (see run()), this guarantees
        # the GA's final result is never worse than min(FF, FFD, BFD-seed).
        for order in self._seed_orders():
            if len(self.population) >= self.pop_size:
                break
            chrom = Chromosome(order.copy(), self.items_dict, self.bin_size)
            self.population.append(chrom)

        # --- Fill the rest of the population with random permutations ---
        while len(self.population) < self.pop_size:
            value = self.gene_pool.copy()
            random.shuffle(value)
            chrom = Chromosome(value, self.items_dict, self.bin_size)
            self.population.append(chrom)

        # Initial Best
        self.best_chromosome = min(self.population, key=lambda x: x.fitness)

    def select_parents(self):
        # Tournament Selection (k=5)
        tournament_size = 5
        selected = random.sample(self.population, 2 * tournament_size)
        
        parent1 = min(selected[:tournament_size], key=lambda x: x.fitness)
        parent2 = min(selected[tournament_size:], key=lambda x: x.fitness)
        
        return parent1, parent2

    def crossover(self, parent1, parent2):
        if random.random() > self.pc:
            return (Chromosome(parent1.value.copy(), self.items_dict, self.bin_size),
                    Chromosome(parent2.value.copy(), self.items_dict, self.bin_size))

        # Order Crossover (OX1) or simply Cut and Fill to preserve permutation
        size = len(parent1.value)
        cut = random.randint(1, size - 1)
        
        def create_child(p1_genes, p2_genes):
            child_genes = p1_genes[:cut]
            # Fill remaining from p2, preserving order, skipping those already in child
            existing = set(child_genes)
            for gene in p2_genes:
                if gene not in existing:
                    child_genes.append(gene)
            return child_genes

        child1_genes = create_child(parent1.value, parent2.value)
        child2_genes = create_child(parent2.value, parent1.value)
        
        return (Chromosome(child1_genes, self.items_dict, self.bin_size),
                Chromosome(child2_genes, self.items_dict, self.bin_size))

    def run(self):
        self.initialize_population()
        
        for gen in range(self.generations):
            new_population = []
            
            # Elitism: Keep best
            new_population.append(self.best_chromosome)
            
            while len(new_population) < self.pop_size:
                p1, p2 = self.select_parents()
                c1, c2 = self.crossover(p1, p2)
                c1.mutate(self.pm)
                c2.mutate(self.pm)
                new_population.append(c1)
                if len(new_population) < self.pop_size:
                    new_population.append(c2)
            
            self.population = new_population
            
            # Update stats
            current_best = min(self.population, key=lambda x: x.fitness)
            if current_best.fitness < self.best_chromosome.fitness:
                self.best_chromosome = current_best
                
            avg_fit = sum(c.fitness for c in self.population) / self.pop_size
            self.history['best'].append(self.best_chromosome.fitness)
            self.history['avg'].append(avg_fit)
            
            # Optional: Print progress
            # if gen % 10 == 0:
            #     print(f"Gen {gen}: Best Bins = {self.best_chromosome.num_bins}")
                
        return self.best_chromosome

