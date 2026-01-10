import os

# Define paths
bpplib_path = "BPPLIB/Instances/Benchmarks/1_Falkenauer/Falkenauer/Falkenauer_T"
instance_name = "Falkenauer_t60_00.txt"

# 1. Solve with standard FFD (First Fit Decreasing)
def solve_ffd(items_dict, bin_size):
    # Sort items decreasing
    sorted_items = sorted(items_dict.items(), key=lambda x: x[1], reverse=True)
    bins = []
    
    for item_id, item_size in sorted_items:
        placed = False
        for bin in bins:
            if bin['used'] + item_size <= bin_size:
                bin['used'] += item_size
                bin['items'].append((item_id, item_size))
                placed = True
                break
        if not placed:
            bins.append({'used': item_size, 'items': [(item_id, item_size)]})
    return len(bins)

# Read Instance
items_dict, bin_size = read_instance(instance_name, bpplib_path)
optimal_bins = len(items_dict) // 3 # Known property of Triplets

# Run FFD
ffd_result = solve_ffd(items_dict, bin_size)
print(f"Instance: {instance_name}")
print(f"Optimal: {optimal_bins}")
print(f"FFD Result: {ffd_result} (Gap: {ffd_result - optimal_bins})")

# Run GA
print("\nRunning GA...")
pop_size = 50
num_generations = 100
avg_fit, best_fit = main_loop(instance_name, pop_size, items_dict, bin_size, num_generations)

