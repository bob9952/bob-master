import os
import random
import time
import pandas as pd
from src.parser import parse_instance_file
from src.ga import GeneticAlgorithm
from src.heuristic import first_fit, next_fit, best_fit, max_rest, max_rest_pq
from src.solution_manager import SolutionManager

# Settings
SAMPLES_PER_FOLDER = 10  # Sample size
POP_SIZE = 40            # Reduced for faster testing
GENERATIONS = 50         # Reduced for faster testing
RUNS_PER_INSTANCE = 1

def solve_heuristic(items_dict, bin_capacity, func, sort_descending=False):
    """
    Generic wrapper to run a heuristic.
    """
    start = time.time()
    
    # Sort keys if needed
    keys = list(items_dict.keys())
    if sort_descending:
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
        if cap >= 100000:
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
        # CONSOLE HEADER (Clean, single line)
        header = f"{'Cat':<8} | {'Instance':<30} | {'Itm':<5} {'Cap':<8} | {'Opt':<4} | {'FF':<5} {'tFF':<8} | {'FFD':<5} {'tFFD':<8} | {'BF':<5} {'tBF':<8} | {'BFD':<5} {'tBFD':<8} | {'NF':<5} {'tNF':<8} | {'NFD':<5} {'tNFD':<8} | {'MR':<5} {'tMR':<8} | {'MRD':<5} {'tMRD':<8} | {'MR+':<5} {'tMR+':<8} | {'MRD+':<5} {'tMRD+':<8} | {'GA':<5} {'tGA':<8} | {'Gap':<4}"
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
            if capacity >= 100000: category = "Hard"
            elif capacity >= 1000: category = "Medium"
            else: category = "Easy"
            
            # Get Optimal
            optimal = instance['best_known']
            if not optimal:
                optimal = sol_manager.get_optimal(name)
            
            # --- RUN HEURISTICS ---
            ff, t_ff = solve_heuristic(items, capacity, first_fit, False)
            ffd, t_ffd = solve_heuristic(items, capacity, first_fit, True)
            
            bf, t_bf = solve_heuristic(items, capacity, best_fit, False)
            bfd, t_bfd = solve_heuristic(items, capacity, best_fit, True)
            
            nf, t_nf = solve_heuristic(items, capacity, next_fit, False)
            nfd, t_nfd = solve_heuristic(items, capacity, next_fit, True)
            
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
                "BF": bf, "BF_Time": t_bf,
                "BFD": bfd, "BFD_Time": t_bfd,
                "NF": nf, "NF_Time": t_nf,
                "NFD": nfd, "NFD_Time": t_nfd,
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
            def p(val, t): return f"{val:<5} {t:<8.4f}"
            
            # Safe opt string
            opt_str = str(optimal) if optimal is not None else "-"
            
            print(f"{category:<8} | {name:<30} | {num_items:<5} {capacity:<8g} | {opt_str:<4} | {p(ff, t_ff)} | {p(ffd, t_ffd)} | {p(bf, t_bf)} | {p(bfd, t_bfd)} | {p(nf, t_nf)} | {p(nfd, t_nfd)} | {p(mr, t_mr)} | {p(mrd, t_mrd)} | {p(mrpq, t_mrpq)} | {p(mrdpq, t_mrdpq)} | {ga_res:<5} {ga_time:<8.2f} | {gap_ga:<4}")
            
            # Write to TXT (Detailed)
            line1 = f"{category:<8} | {name[:23]:<25} | {opt_str:<4} | {ga_res:<4} {gap_ga:<4} | {ga_time:.2f}s"
            line2 = f"   FF:{ff}({t_ff:.4f}) FFD:{ffd}({t_ffd:.4f}) BF:{bf}({t_bf:.4f}) BFD:{bfd}({t_bfd:.4f})"
            line3 = f"   NF:{nf}({t_nf:.4f}) NFD:{nfd}({t_nfd:.4f}) MR:{mr}({t_mr:.4f}) MRD:{mrd}({t_mrd:.4f})"
            line4 = f"   MR+:{mrpq}({t_mrpq:.4f}) MRD+:{mrdpq}({t_mrdpq:.4f})"
            
            txtfile.write(line1 + "\n")
            txtfile.write(line2 + "\n")
            txtfile.write(line3 + "\n")
            txtfile.write(line4 + "\n")
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
