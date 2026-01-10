import random
from src.heuristic import first_fit

class Chromosome:
    def __init__(self, value, items_dict, bin_size):
        self.value = value # Permutation of item IDs
        self.items_dict = items_dict
        self.bin_size = bin_size
        self.bins = []
        self.fitness = 0.0
        
        # Evaluate immediately
        self.evaluate()

    def evaluate(self):
        # Decode: Construct bins using First Fit
        self.bins = first_fit(self.value, self.items_dict, self.bin_size)
        
        # Calculate Fitness: Falkenauer's k-power objective
        # Fitness = Sum((fill_ratio)^k) / N
        # This rewards full bins more than equal distribution.
        
        N = len(self.bins)
        if N == 0:
            self.fitness = 0.0
            return

        k = 2 # Exponent factor (k=2 is standard, can try 4)
        sum_filled_ratios = sum((bin['used'] / self.bin_size) ** k for bin in self.bins)
        
        # We want to MAXIMIZE this fitness (range 0 to 1)
        # But your original code minimized (1 - ratio). 
        # Let's stick to Maximization for standard GA logic, or minimize negative.
        # Original code: return 1 - (sum_filled_ratios / N) -> Minimize this.
        # Let's keep it simple: Fitness is just the Falkenauer metric to MAXIMIZE.
        # However, to be compatible with `min(population, key=lambda x: x.fitness)` 
        # we should return a "Cost" (lower is better).
        
        # Cost = Number of Bins - Falkenauer Metric (a small fraction)
        # This way, fewer bins is always better. Within same number of bins, tighter packing is better.
        
        self.fitness = N - (sum_filled_ratios / N) 

    def mutate(self, pm=0.05):
        """Swap Mutation"""
        if random.random() < pm:
            idx1, idx2 = random.sample(range(len(self.value)), 2)
            self.value[idx1], self.value[idx2] = self.value[idx2], self.value[idx1]
            self.evaluate() # Re-evaluate after change
        return self
    
    @property
    def num_bins(self):
        return len(self.bins)

