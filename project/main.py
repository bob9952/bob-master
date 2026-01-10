import os
import time
from src.parser import parse_instance_file
from src.ga import GeneticAlgorithm
from src.heuristic import first_fit

def solve_with_ffd(items_dict, bin_capacity):
    """
    Standard First Fit Decreasing Heuristic
    """
    # Sort items decreasing
    sorted_items = sorted(items_dict.keys(), key=lambda k: items_dict[k], reverse=True)
    bins = first_fit(sorted_items, items_dict, bin_capacity)
    return len(bins)

def main():
    # Robust pathing
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    
    files = ["Falkenauer/U/binpack1.txt"] # Start with the first file (Uniform)
    
    # GA Parameters
    POP_SIZE = 50
    GENERATIONS = 100
    
    print(f"{'Instance':<15} | {'Optimal':<8} | {'FFD':<8} | {'GA':<8} | {'Time (s)':<8}")
    print("-" * 65)
    
    for filename in files:
        # Construct path and handle potential missing files
        filepath = os.path.join(data_dir, filename)
        if not os.path.exists(filepath):
             filepath = os.path.join(data_dir, os.path.basename(filename)) # Try flat structure
             
        if not os.path.exists(filepath):
            print(f"Skipping {filename}: Not found.")
            continue
            
        instances = parse_instance_file(filepath)
        
        # Run on first 5 instances for demo
        for instance in instances:
            name = instance['name']
            capacity = instance['capacity']
            items = instance['items_dict']
            optimal = instance['best_known']
            
            # 1. Run FFD
            ffd_bins = solve_with_ffd(items, capacity)
            
            # 2. Run GA
            start_time = time.time()
            ga = GeneticAlgorithm(items, capacity, pop_size=POP_SIZE, generations=GENERATIONS)
            best_sol = ga.run()
            ga_bins = best_sol.num_bins
            duration = time.time() - start_time
            
            print(f"{name:<15} | {optimal:<8} | {ffd_bins:<8} | {ga_bins:<8} | {duration:<8.2f}")

if __name__ == "__main__":
    main()

