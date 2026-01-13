import random
import matplotlib.pyplot as plt
import math
import os
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

    def visualize_bins(self, instance_name, folder_path="project/results/plots/bins"):
        """
        Visualizes the bins and items for this chromosome.
        Saves the plot to folder_path/instance_name.png
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        bins_per_row = 6
        num_bins = len(self.bins)
        num_rows = math.ceil(num_bins / bins_per_row)
        
        # Use a colormap
        color_map = plt.get_cmap('tab20')

        # Limit figure size for very large instances
        fig_width = 15
        fig_height = max(2, num_rows) * 2
        
        plt.figure(figsize=(fig_width, fig_height))

        for i, bin_data in enumerate(self.bins):
            # Bin data structure from heuristic: {'used': float, 'items': [item_id, ...]}
            # But wait, heuristic.py first_fit returns: [{'used': size, 'items': [id1, id2]}, ...]
            
            plt.subplot(num_rows, bins_per_row, i + 1)
            y_offset = 0
            
            items = bin_data['items']
            
            # If items are just IDs, we need to look up sizes.
            # But wait, does first_fit return just IDs or (id, size)?
            # Let's check heuristic.py
            
            for item_index, (item_id, item_size) in enumerate(items):
                color = color_map(item_index % 20)

                plt.bar([0.5], [item_size], bottom=[y_offset], width=0.9, edgecolor='black', color=color)

                text_pos_y = y_offset + item_size / 2
                text = f"id: {item_id}\n{item_size}"
                
                # Only show text if item is large enough
                if item_size > self.bin_size * 0.05:
                    plt.text(0.5, text_pos_y, text, ha='center', va='center', fontsize=8, color='white')

                y_offset += item_size

            plt.ylim(0, self.bin_size)
            plt.title(f"Bin {i} ({bin_data['used']})")
            plt.xticks([])
            plt.yticks([])

        plt.tight_layout()
        save_path = os.path.join(folder_path, f"{instance_name}.png")
        plt.savefig(save_path)
        plt.close()

