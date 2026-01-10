import random
import time
from src.chromosome import Chromosome

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

    def initialize_population(self):
        self.population = []
        for _ in range(self.pop_size):
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

