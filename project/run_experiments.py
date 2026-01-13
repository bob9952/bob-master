import os
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
from src.parser import parse_instance_file
from src.ga import GeneticAlgorithm
from src.heuristic import (
    first_fit, next_fit, best_fit, max_rest, max_rest_pq,
    first_fit_lookup, best_fit_lookup, counting_sort
)
from src.solution_manager import SolutionManager

# Settings
SAMPLES_PER_FOLDER = 10  # Sample size
POP_SIZE = 40            # Reduced for faster testing
GENERATIONS = 50         # Reduced for faster testing
RUNS_PER_INSTANCE = 1

def solve_heuristic(items_dict, bin_capacity, func, sort_descending=False, use_counting_sort=False):
    """
    Generic wrapper to run a heuristic.
    """
    start = time.time()
    
    keys = list(items_dict.keys())
    
    # Sorting logic
    if sort_descending:
        if use_counting_sort:
            # Check if all values are integers
            all_ints = all(float(items_dict[k]).is_integer() for k in keys)
            if all_ints:
                max_val = max(int(items_dict[k]) for k in keys)
                keys = counting_sort(keys, items_dict, max_val)
            else:
                # Fallback to standard sort for floats
                keys = sorted(keys, key=lambda k: items_dict[k], reverse=True)
        else:
            keys = sorted(keys, key=lambda k: items_dict[k], reverse=True)
    
    # Run heuristic
    bins = func(keys, items_dict, bin_capacity)
    
    duration = time.time() - start
    return len(bins), duration

def main():
    # Use default SolutionManager path which looks for data/Solutions.xlsx
    sol_manager = SolutionManager()
    
    # Robust pathing relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Directories
    results_dir = os.path.join(script_dir, "results")
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        
    base_data_dir = os.path.join(script_dir, "data")
    
    # Output Files
    output_xlsx = os.path.join(results_dir, "experiment_results.xlsx")
    output_txt = os.path.join(results_dir, "experiment_results.txt")
    
    # Collect all instance files
    all_instances = []
    
    # 1. Walk through directories
    for root, dirs, files in os.walk(base_data_dir):
        target_files = [f for f in files if f.endswith(".txt")]
        
        for f in target_files:
            file_path = os.path.join(root, f)
            folder_name = os.path.basename(os.path.dirname(file_path))
            
            # Parse all instances from this file
            parsed_instances = parse_instance_file(file_path)
            
            if not parsed_instances:
                continue
                
            for instance in parsed_instances:
                instance['_folder'] = folder_name
                instance['_file'] = f
                all_instances.append(instance)

    # 2. Categorize and Sample
    categories = {'Easy': [], 'Medium': [], 'Hard': []}
    
    for inst in all_instances:
        cap = inst['capacity']
        name = inst['name']
        folder = inst['_folder']
        
        is_wascher = "Waescher" in name or "Wäscher" in folder
        is_hard28 = "Hard28" in folder or "Hard28" in name
        
        if cap >= 100000 or is_wascher or is_hard28:
            categories['Hard'].append(inst)
        elif cap >= 1000:
            categories['Medium'].append(inst)
        else:
            categories['Easy'].append(inst)
            
    final_test_set = []
    
    # Sample from each category
    print(f"\nInstance Distribution:")
    for cat, insts in categories.items():
        count = len(insts)
        sample_size = min(count, SAMPLES_PER_FOLDER)
        selected = random.sample(insts, sample_size)
        final_test_set.extend(selected)
        print(f"  - {cat}: {count} available -> {sample_size} selected")
        
        # Sort selected by name for nicer output
        selected.sort(key=lambda x: x['name'])

    print(f"\nTotal tests: {len(final_test_set)}")
    
    # Data storage for DataFrame
    results_data = []

    # Open TXT file for writing detailed report
    with open(output_txt, 'w') as txtfile:
        # CONSOLE HEADER (Clean & Focused)
        header = f"{'Cat':<8} | {'Instance':<20} | {'Itm':<4} {'Cap':<7} | {'Opt':<4} | {'FF':<4} {'FFD':<4} {'FFD+':<5} {'FFL':<4} | {'BF':<4} {'BFD':<4} {'BFL':<4} | {'NF':<4} {'NFD':<4} {'NFD+':<5} | {'MR':<4} {'MRD':<4} {'MR+':<4} {'MRD+':<5} | {'GA':<4} {'tGA':<7}"
        print("-" * len(header))
        print(header)
        print("-" * len(header))
        
        # TXT FILE HEADER (Detailed)
        txtfile.write("-" * 80 + "\n")
        txtfile.write(f"{'Category':<8} | {'Instance':<25} | {'Opt':<4} | {'GA':<4} {'Gap':<4} | {'Time':<6}\n")
        txtfile.write("-" * 80 + "\n")

        for i, instance in enumerate(final_test_set):
            
            name = instance['name']
            capacity = instance['capacity']
            items = instance['items_dict']
            num_items = len(items)
            folder_name = instance['_folder']
            
            # Determine Category
            # Hard: Capacity >= 100,000 OR specifically hard datasets like Wäscher or Hard28
            is_wascher = "Waescher" in name or "Wäscher" in folder_name
            is_hard28 = "Hard28" in folder_name or "Hard28" in name
            
            if capacity >= 100000 or is_wascher or is_hard28: 
                category = "Hard"
            elif capacity >= 1000: 
                category = "Medium"
            else: 
                category = "Easy"
            
            # Get Optimal
            optimal = instance['best_known']
            if not optimal:
                optimal = sol_manager.get_optimal(name)
            
            # --- RUN HEURISTICS ---
            ff, t_ff = solve_heuristic(items, capacity, first_fit, False)
            ffd, t_ffd = solve_heuristic(items, capacity, first_fit, True)
            
            # New: First Fit Lookup
            ffl, t_ffl = solve_heuristic(items, capacity, first_fit_lookup, False)
            
            bf, t_bf = solve_heuristic(items, capacity, best_fit, False)
            bfd, t_bfd = solve_heuristic(items, capacity, best_fit, True)

            # New: Best Fit Lookup
            bfl, t_bfl = solve_heuristic(items, capacity, best_fit_lookup, False)
            
            nf, t_nf = solve_heuristic(items, capacity, next_fit, False)
            nfd, t_nfd = solve_heuristic(items, capacity, next_fit, True)
            
            # New: Counting Sort Variants (FFD+, NFD+)
            ffdc, t_ffdc = solve_heuristic(items, capacity, first_fit, True, use_counting_sort=True)
            nfdc, t_nfdc = solve_heuristic(items, capacity, next_fit, True, use_counting_sort=True)
            
            mr, t_mr = solve_heuristic(items, capacity, max_rest, False)
            mrd, t_mrd = solve_heuristic(items, capacity, max_rest, True)

            mrpq, t_mrpq = solve_heuristic(items, capacity, max_rest_pq, False)
            mrdpq, t_mrdpq = solve_heuristic(items, capacity, max_rest_pq, True)
            
            # --- RUN GA ---
            start_ga = time.time()
            ga = GeneticAlgorithm(items, capacity, pop_size=POP_SIZE, generations=GENERATIONS, mutation_prob=0.2)
            best_sol = ga.run()
            ga_res = best_sol.num_bins
            ga_time = time.time() - start_ga
            
            # --- VISUALIZATION ---
            # 1. Visualize Bins
            plots_dir = os.path.join(results_dir, "plots", "bins")
            best_sol.visualize_bins(name, folder_path=plots_dir)

            # 2. Visualize Convergence (Save only for first instance of each category or every 5th)
            conv_dir = os.path.join(results_dir, "plots", "convergence")
            if not os.path.exists(conv_dir):
                os.makedirs(conv_dir)
                
            plt.figure(figsize=(10, 5))
            plt.plot(ga.history['best'], label='Best Fitness')
            plt.plot(ga.history['avg'], label='Average Fitness', linestyle='--')
            plt.xlabel('Generation')
            plt.ylabel('Fitness (Cost)')
            plt.title(f'GA Convergence: {name}')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(conv_dir, f"{name}_conv.png"))
            plt.close()

            # Gaps
            gap_ga = (ga_res - optimal) if optimal else 0
            
            # Record Data
            row = {
                "Category": category,
                "Dataset": folder_name,
                "Instance": name,
                "Items": num_items,
                "Capacity": capacity,
                "Optimal": optimal,
                "FF": ff, "FF_Time": t_ff,
                "FFD": ffd, "FFD_Time": t_ffd,
                "FFL": ffl, "FFL_Time": t_ffl,
                "FFD+": ffdc, "FFD+_Time": t_ffdc,
                "BF": bf, "BF_Time": t_bf,
                "BFD": bfd, "BFD_Time": t_bfd,
                "BFL": bfl, "BFL_Time": t_bfl,
                "NF": nf, "NF_Time": t_nf,
                "NFD": nfd, "NFD_Time": t_nfd,
                "NFD+": nfdc, "NFD+_Time": t_nfdc,
                "MR": mr, "MR_Time": t_mr,
                "MRD": mrd, "MRD_Time": t_mrd,
                "MR+": mrpq, "MR+_Time": t_mrpq,
                "MRD+": mrdpq, "MRD+_Time": t_mrdpq,
                "GA": ga_res, "GA_Time": ga_time,
                "Gap_GA": gap_ga
            }
            results_data.append(row)
            
            # Print to Console (Formatted Table - Ultra Wide with Time Columns)
            # Helper for formatting pairs
            def p(val, t): return f"{val:<5} {t:<7.4f}"
            
            # Safe opt string
            opt_str = str(optimal) if optimal is not None else "-"
            
            # Print ALL columns (Focused)
            # Truncate name to fit 20 chars
            short_name = (name[:17] + '..') if len(name) > 20 else name
            
            print(f"{category:<8} | {short_name:<20} | {num_items:<4} {capacity:<7g} | {opt_str:<4} | " + 
                  f"{ff:<4} {ffd:<4} {ffdc:<5} {ffl:<4} | " + 
                  f"{bf:<4} {bfd:<4} {bfl:<4} | " + 
                  f"{nf:<4} {nfd:<4} {nfdc:<5} | " + 
                  f"{mr:<4} {mrd:<4} {mrpq:<4} {mrdpq:<5} | " + 
                  f"{ga_res:<4} {ga_time:<7.3f}")
            
            # Write to TXT (Detailed)
            line1 = f"{category:<8} | {name[:23]:<25} | {opt_str:<4} | {ga_res:<4} {gap_ga:<4} | {ga_time:.2f}s"
            line2 = f"   FF:{ff}({t_ff:.4f}) FFD:{ffd}({t_ffd:.4f}) FFD+:{ffdc}({t_ffdc:.4f}) FFL:{ffl}({t_ffl:.4f})"
            line3 = f"   BF:{bf}({t_bf:.4f}) BFD:{bfd}({t_bfd:.4f}) BFL:{bfl}({t_bfl:.4f})"
            line4 = f"   NF:{nf}({t_nf:.4f}) NFD:{nfd}({t_nfd:.4f}) NFD+:{nfdc}({t_nfdc:.4f})"
            line5 = f"   MR:{mr}({t_mr:.4f}) MRD:{mrd}({t_mrd:.4f}) MR+:{mrpq}({t_mrpq:.4f})"
            
            txtfile.write(line1 + "\n")
            txtfile.write(line2 + "\n")
            txtfile.write(line3 + "\n")
            txtfile.write(line4 + "\n")
            txtfile.write(line5 + "\n")
            txtfile.write("-" * 80 + "\n")
            txtfile.flush()

    # Save to Excel
    df = pd.DataFrame(results_data)
    df.to_excel(output_xlsx, index=False)
    
    print(f"\nExperiments completed.")
    print(f"Excel Data:    {output_xlsx}")
    print(f"Readable Log:  {output_txt}")

if __name__ == "__main__":
    main()
