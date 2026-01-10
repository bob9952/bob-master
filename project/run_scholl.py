import os
import argparse
import sys
# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.parser import parse_instance_file
from src.ga import GeneticAlgorithm
from src.heuristic import first_fit
from src.solution_manager import SolutionManager

def solve_with_ffd(items_dict, bin_capacity):
    sorted_items = sorted(items_dict.keys(), key=lambda k: items_dict[k], reverse=True)
    bins = first_fit(sorted_items, items_dict, bin_capacity)
    return len(bins)

def run_single_instance(file_path):
    # 1. Parse Instance
    instances = parse_instance_file(file_path)
    if not instances:
        print("No instances found.")
        return

    instance = instances[0]
    name = instance['name']
    capacity = instance['capacity']
    items = instance['items_dict']
    
    # 2. Get Optimal from Manager
    # Use default Excel path (project/data/Solutions.xlsx)
    sol_manager = SolutionManager()
    
    # Check if file has it (Falkenauer) or use Manager (Scholl)
    best_known = instance['best_known']
    if not best_known:
        best_known = sol_manager.get_optimal(name)
    
    print(f"\n--- Testing Instance: {name} ---")
    print(f"Capacity: {capacity}")
    print(f"Items: {len(items)}")
    
    optimal_str = f"{best_known}" if best_known else "Unknown"
    print(f"Optimal (Best Known): {optimal_str}")
    
    # FFD
    ffd_bins = solve_with_ffd(items, capacity)
    print(f"FFD Result: {ffd_bins}")
    
    # GA
    print("Running GA...")
    ga = GeneticAlgorithm(items, capacity, pop_size=100, generations=500, mutation_prob=0.2)
    best_sol = ga.run()
    ga_bins = best_sol.num_bins
    
    print(f"GA Result: {ga_bins}")
    
    if best_known:
        gap = ga_bins - best_known
        print(f"Gap: {gap}")

if __name__ == "__main__":
    # Determine base directory relative to this script file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    
    # Check specific file path
    target_file = os.path.join(data_dir, "Scholl", "set_1", "N1C1W1_A.txt")
    
    if os.path.exists(target_file):
        run_single_instance(target_file)
    else:
        # Fallback check - maybe it's in the root of data
        target_file = os.path.join(data_dir, "N1C1W1_A.txt")
        if os.path.exists(target_file):
            run_single_instance(target_file)
        else:
            print(f"File not found at: {target_file}")
            print(f"Please copy N1C1W1_A.txt to {os.path.join(data_dir, 'Scholl', 'set_1')}")
