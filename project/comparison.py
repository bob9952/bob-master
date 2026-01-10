import os
import time
from src.parser import parse_instance_file
from src.ga import GeneticAlgorithm
from src.heuristic import first_fit

def solve_with_ffd(items_dict, bin_capacity):
    """
    Standard First Fit Decreasing Heuristic
    """
    sorted_items = sorted(items_dict.keys(), key=lambda k: items_dict[k], reverse=True)
    bins = first_fit(sorted_items, items_dict, bin_capacity)
    return len(bins)

def run_comparison():
    # Robust pathing relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    
    # binpack5 to binpack8 are the Triplets (Hard) - Located in Falkenauer/T/
    triplet_file_path = os.path.join(data_dir, "Falkenauer", "T", "binpack5.txt") 
    
    # Check if file exists, if not, try alternative location or warn
    if not os.path.exists(triplet_file_path):
         # Fallback to just data root if flattening happened
         triplet_file_path = os.path.join(data_dir, "binpack5.txt")
         
    if not os.path.exists(triplet_file_path):
        print(f"Error: Could not find binpack5.txt at {triplet_file_path}")
        return

    # Use the new universal parser function
    instances = parse_instance_file(triplet_file_path)
    
    if not instances:
        print("No instances found. Check data directory.")
        return

    print(f"Comparison on Triplets (Hard Instances) - {triplet_file_path}")
    print(f"{'Instance':<25} | {'Optimal':<8} | {'FFD':<8} | {'GA (My)':<8} | {'Gap (GA)':<8}")
    print("-" * 75)
    
    # Run on first 5 triplet instances
    for instance in instances[:5]:
        name = instance['name']
        capacity = instance['capacity']
        items = instance['items_dict']
        optimal = instance['best_known']
        
        # FFD
        ffd_bins = solve_with_ffd(items, capacity)
        
        # GA
        # Increase population and generations for better convergence on hard instances
        ga = GeneticAlgorithm(items, capacity, pop_size=100, generations=500, mutation_prob=0.2)
        best_sol = ga.run()
        ga_bins = best_sol.num_bins
        
        gap = ga_bins - optimal
        
        print(f"{name:<25} | {optimal:<8} | {ffd_bins:<8} | {ga_bins:<8} | {gap:<8}")

if __name__ == "__main__":
    run_comparison()

