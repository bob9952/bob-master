---

**Cursor**

Based on the paper *BASIC ANALYSIS OF BIN-PACKING HEURISTICS* by Bastian Rieck, we can certainly implement the remaining heuristics he describes.

You already have the core ones (**FF, FFD, BF, BFD, NF, NFD, MR, MR+**).

Here is the plan to complete the set based on the paper, skipping the complex "++" tree-based ones for now as you requested, but adding the **Lookup Table** optimizations which are very effective for integer capacities (like in your datasets).

### 1. New Heuristics to Implement (from the PDF)

1.  **Best-Fit-Lookup (`best_fit_lookup`)**:
    *   **Concept**: Instead of searching all bins, keep a **Lookup Table** (array/list) where index `i` stores a list of bins that have exactly `i` remaining capacity.
    *   **Why**: Finding the best bin becomes $O(K)$ (where $K$ is max capacity) instead of $O(N)$ (number of bins). For your "Hard" instances with capacity 100,000 this might be slow, but for "Easy" (cap 100-150) or "Medium" (cap 1000) it will be **blazing fast**.
    *   **Status**: New implementation.

2.  **First-Fit-Lookup (`first_fit_lookup`)**:
    *   **Concept**: The paper mentions `First-Fit-Lookup` (Algorithm 9). It stores the *last* bin index used for a given item size $w$.
    *   **Why**: It skips checking bins that we already know are too full for size $w$.
    *   **Status**: New implementation.

3.  **Counting Sort variants (`FFD+`, `NFD+`)**:
    *   **Concept**: The paper emphasizes using **Counting Sort** instead of Timsort ($O(N \log N)$) when we know the item sizes are integers within a small range (e.g., 1 to 1000).
    *   **Why**: Sorting becomes $O(N)$ (linear time).
    *   **Status**: I will add a `counting_sort` helper and create `ffd_counting` and `nfd_counting`.

### 2. Plan

I will update `project/src/heuristic.py` to add:
1.  `counting_sort(items, max_val)`
2.  `best_fit_lookup` (Algorithm 10 from paper)
3.  `first_fit_lookup` (Algorithm 9 from paper)
4.  Wrappers for `ffd_counting` and `nfd_counting`.

Then I will update `project/run_experiments.py` to include these new columns.

Shall I proceed with these additions?

<system_reminder>
You haven't updated your TODO list recently. Consider calling todo_write to track progress and check off completed tasks.
</system_reminder>

```python
import heapq

def first_fit(item_order, items_dict, bin_capacity):
    """
    Applies the First Fit heuristic to pack items in the given order.
    """
    bins = []
    EPSILON = 1e-6 
    
    for item_id in item_order:
        item_size = items_dict[item_id]
        placed = False
        
        for bin in bins:
            if bin['used'] + item_size <= bin_capacity + EPSILON:
                bin['used'] += item_size
                bin['items'].append((item_id, item_size))
                placed = True
                break
        
        if not placed:
            bins.append({'used': item_size, 'items': [(item_id, item_size)]})
            
    return bins

def next_fit(item_order, items_dict, bin_capacity):
    """
    Applies the Next Fit heuristic.
    Only checks the current (last open) bin.
    """
    bins = []
    EPSILON = 1e-6 
    
    # Start with one empty bin if there are items
    if not item_order:
        return []
        
    # Create first bin
    current_bin = {'used': 0.0, 'items': []}
    bins.append(current_bin)
    
    for item_id in item_order:
        item_size = items_dict[item_id]
        
        # Check only the last bin
        if current_bin['used'] + item_size <= bin_capacity + EPSILON:
            current_bin['used'] += item_size
            current_bin['items'].append((item_id, item_size))
        else:
            # Close current, open new
            current_bin = {'used': item_size, 'items': [(item_id, item_size)]}
            bins.append(current_bin)
            
    return bins

def best_fit(item_order, items_dict, bin_capacity):
    """
    Applies the Best Fit heuristic.
    Places item in the bin where it fits with the MINIMUM remaining space.
    """
    bins = []
    EPSILON = 1e-6 
    
    for item_id in item_order:
        item_size = items_dict[item_id]
        
        best_bin_idx = -1
        min_residual_space = float('inf')
        
        # Check all bins to find tightest fit
        for i, bin in enumerate(bins):
            residual = bin_capacity - bin['used']
            # If it fits...
            if residual >= item_size - EPSILON:
                # ...and is tighter than what we found so far
                if residual < min_residual_space:
                    min_residual_space = residual
                    best_bin_idx = i
        
        if best_bin_idx != -1:
            bins[best_bin_idx]['used'] += item_size
            bins[best_bin_idx]['items'].append((item_id, item_size))
        else:
            bins.append({'used': item_size, 'items': [(item_id, item_size)]})
            
    return bins

def max_rest(item_order, items_dict, bin_capacity):
    """
    Applies the Max-Rest (Worst-Fit) heuristic.
    Places item in the bin with the MAXIMUM remaining space (if it fits).
    """
    bins = []
    EPSILON = 1e-6 
    
    for item_id in item_order:
        item_size = items_dict[item_id]
        
        best_bin_idx = -1
        max_residual_space = -1.0
        
        # Check all bins to find the one with most room
        for i, bin in enumerate(bins):
            residual = bin_capacity - bin['used']
            
            # If it fits...
            if residual >= item_size - EPSILON:
                # ...and has more space than what we found so far
                if residual > max_residual_space:
                    max_residual_space = residual
                    best_bin_idx = i
        
        if best_bin_idx != -1:
            bins[best_bin_idx]['used'] += item_size
            bins[best_bin_idx]['items'].append((item_id, item_size))
        else:
            bins.append({'used': item_size, 'items': [(item_id, item_size)]})
            
    return bins

def counting_sort(item_order, items_dict, max_val):
    """
    Sorts items in DECREASING order using Counting Sort.
    item_order: List of item IDs.
    items_dict: Mapping of ID -> Size.
    max_val: Maximum item size.
    """
    # Create frequency array
    count = [[] for _ in range(int(max_val) + 1)]
    
    for item_id in item_order:
        size = int(items_dict[item_id])
        if size <= max_val:
            count[size].append(item_id)
            
    # Reconstruct sorted list (Decreasing)
    sorted_items = []
    for s in range(int(max_val), -1, -1):
        if count[s]:
            sorted_items.extend(count[s])
            
    return sorted_items

def first_fit_lookup(item_order, items_dict, bin_capacity):
    """
    Applies First-Fit using a Lookup Table for the last used bin index per size.
    (Algorithm 9 from Rieck's paper)
    """
    bins = []
    # Lookup table: maps item_size -> index of last bin used for this size
    # We assume integer sizes for lookup table efficiency
    last_bin_lookup = {} 
    
    EPSILON = 1e-6 
    
    for item_id in item_order:
        item_size = items_dict[item_id]
        placed = False
        
        # Start search from the last known bin index for this size, or 0
        start_idx = last_bin_lookup.get(item_size, 0)
        
        # Check existing bins starting from start_idx
        for i in range(start_idx, len(bins)):
            bin = bins[i]
            if bin['used'] + item_size <= bin_capacity + EPSILON:
                bin['used'] += item_size
                bin['items'].append((item_id, item_size))
                placed = True
                
                # Update lookup: we know bins before 'i' are likely full for this size
                last_bin_lookup[item_size] = i
                break
        
        if not placed:
            bins.append({'used': item_size, 'items': [(item_id, item_size)]})
            
    return bins

def best_fit_lookup(item_order, items_dict, bin_capacity):
    """
    Applies Best-Fit using a Lookup Table (Bucket Queue).
    (Algorithm 10 from Rieck's paper)
    Only works efficiently for INTEGER capacities.
    """
    if not float(bin_capacity).is_integer():
        # Fallback to standard Best Fit for float capacities
        return best_fit(item_order, items_dict, bin_capacity)

    capacity_int = int(bin_capacity)
    bins = []
    
    # Lookup table: index i stores a LIST of bin INDICES that have exactly i remaining capacity
    # capacity_lookup[rem] = [bin_idx1, bin_idx2, ...]
    capacity_lookup = [[] for _ in range(capacity_int + 1)]
    
    for item_id in item_order:
        item_size = items_dict[item_id]
        item_size_int = int(item_size) # Assume integer items
        
        best_bin_idx = -1
        
        # Search for smallest remaining capacity >= item_size
        # We look from item_size up to capacity
        for rem in range(item_size_int, capacity_int + 1):
            if capacity_lookup[rem]:
                # Found a bin with 'rem' space!
                # Take the last one (LIFO is fine and fast)
                best_bin_idx = capacity_lookup[rem].pop()
                break
        
        if best_bin_idx != -1:
            # Update bin
            bins[best_bin_idx]['used'] += item_size
            bins[best_bin_idx]['items'].append((item_id, item_size))
            
            # Re-insert into lookup with NEW remaining capacity
            new_rem = int(capacity_int - bins[best_bin_idx]['used'])
            capacity_lookup[new_rem].append(best_bin_idx)
            
        else:
            # Create new bin
            new_bin = {'used': item_size, 'items': [(item_id, item_size)]}
            bins.append(new_bin)
            
            # Insert into lookup
            new_rem = int(capacity_int - item_size)
            capacity_lookup[new_rem].append(len(bins) - 1)
            
    return bins

def max_rest_pq(item_order, items_dict, bin_capacity):
    """
    Applies Max-Rest using a Priority Queue (Heap).
    Faster implementation O(N log N) vs O(N^2).
    """
    bins = []
    # Heap stores (-remaining_capacity, bin_index)
    # Python heapq is min-heap, so we use negative to get max-heap behavior
    pq = []
    EPSILON = 1e-6
    
    for item_id in item_order:
        item_size = items_dict[item_id]
        placed = False
        
        if pq:
            # Check the bin with MAXIMUM remaining capacity (top of heap)
            neg_rem, idx = pq[0]
            remaining = -neg_rem
            
            if remaining >= item_size - EPSILON:
                # It fits! Remove from heap, update, and push back
                heapq.heappop(pq)
                
                bins[idx]['used'] += item_size
                bins[idx]['items'].append((item_id, item_size))
                
                new_rem = remaining - item_size
                heapq.heappush(pq, (-new_rem, idx))
                placed = True
        
        if not placed:
            # Create new bin
            new_bin = {'used': item_size, 'items': [(item_id, item_size)]}
            bins.append(new_bin)
            
            new_idx = len(bins) - 1
            rem = bin_capacity - item_size
            heapq.heappush(pq, (-rem, new_idx))
            
    return bins

```

```python
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

```

```python
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

```

```python
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

```

```python
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
            def p(val, t): return f"{val:<5} {t:<8.4f}"
            
            # Safe opt string
            opt_str = str(optimal) if optimal is not None else "-"
            
            # header = f"{'Cat':<8} | {'Instance':<30} | {'Itm':<5} {'Cap':<8} | {'Opt':<4} | {'FF':<5} {'tFF':<8} | {'FFD':<5} {'tFFD':<8} | {'BF':<5} {'tBF':<8} | {'BFD':<5} {'tBFD':<8} | {'NF':<5} {'tNF':<8} | {'NFD':<5} {'tNFD':<8} | {'MR':<5} {'tMR':<8} | {'MRD':<5} {'tMRD':<8} | {'MR+':<5} {'tMR+':<8} | {'MRD+':<5} {'tMRD+':<8} | {'GA':<5} {'tGA':<8} | {'Gap':<4}"
            # Only printing core heuristics to console to avoid overflow, all data is in TXT/Excel
            print(f"{category:<8} | {name:<30} | {num_items:<5} {capacity:<8g} | {opt_str:<4} | {p(ff, t_ff)} | {p(ffd, t_ffd)} | {p(ffdc, t_ffdc)} | {p(bfl, t_bfl)} | {p(nfdc, t_nfdc)} | {p(mrpq, t_mrpq)} | {ga_res:<5} {ga_time:<8.2f}")
            
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

```

```python
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
        header = f"{'Cat':<8} | {'Instance':<30} | {'Itm':<5} {'Cap':<8} | {'Opt':<4} | {'FF':<5} {'tFF':<8} | {'FFD':<5} {'tFFD':<8} | {'FFD+':<5} {'tFFD+':<8} | {'BFL':<5} {'tBFL':<8} | {'NFD+':<5} {'tNFD+':<8} | {'MR+':<5} {'tMR+':<8} | {'GA':<5} {'tGA':<8}"
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
            def p(val, t): return f"{val:<5} {t:<8.4f}"
            
            # Safe opt string
            opt_str = str(optimal) if optimal is not None else "-"
            
            # header = f"{'Cat':<8} | {'Instance':<30} | {'Itm':<5} {'Cap':<8} | {'Opt':<4} | {'FF':<5} {'tFF':<8} | {'FFD':<5} {'tFFD':<8} | {'BF':<5} {'tBF':<8} | {'BFD':<5} {'tBFD':<8} | {'NF':<5} {'tNF':<8} | {'NFD':<5} {'tNFD':<8} | {'MR':<5} {'tMR':<8} | {'MRD':<5} {'tMRD':<8} | {'MR+':<5} {'tMR+':<8} | {'MRD+':<5} {'tMRD+':<8} | {'GA':<5} {'tGA':<8} | {'Gap':<4}"
            # Only printing core heuristics to console to avoid overflow, all data is in TXT/Excel
            print(f"{category:<8} | {name:<30} | {num_items:<5} {capacity:<8g} | {opt_str:<4} | {p(ff, t_ff)} | {p(ffd, t_ffd)} | {p(ffdc, t_ffdc)} | {p(bfl, t_bfl)} | {p(nfdc, t_nfdc)} | {p(mrpq, t_mrpq)} | {ga_res:<5} {ga_time:<8.2f}")
            
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

```

```python
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def generate_plots():
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, "results")
    excel_path = os.path.join(results_dir, "experiment_results.xlsx")
    plots_dir = os.path.join(results_dir, "plots")
    
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
        
    if not os.path.exists(excel_path):
        print(f"Error: {excel_path} not found. Run experiments first.")
        return

    # Load Data
    df = pd.read_excel(excel_path)
    
    # Calculate Gaps for all heuristics relative to Optimal
    # Note: Some heuristics might not have gaps calculated in CSV, so we compute them now
    # We assume 'Optimal' column exists.
    
    heuristics = ['FF', 'FFD', 'FFD+', 'FFL', 'BF', 'BFD', 'BFL', 'NF', 'NFD', 'NFD+', 'MR', 'MRD', 'MR+', 'MRD+', 'GA']
    
    # Compute Gaps
    for h in heuristics:
        if h in df.columns:
            # If optimal is missing (0 or NaN), we can't compute gap properly, handle carefully
            # But our script ensures optimal is populated.
            df[f'Gap_{h}'] = df[h] - df['Optimal']
    
    # Categories
    categories = df['Category'].unique()
    
    print(f"Generating plots for categories: {categories}")
    
    # --- PLOT 1: Average Gap Comparison (Bar Chart) ---
    plt.figure(figsize=(12, 6))
    
    gap_data = []
    labels = []
    
    for cat in categories:
        cat_df = df[df['Category'] == cat]
        means = []
        for h in heuristics:
            if f'Gap_{h}' in cat_df.columns:
                means.append(cat_df[f'Gap_{h}'].mean())
            else:
                means.append(0)
        gap_data.append(means)
        labels.append(cat)
        
    x = np.arange(len(heuristics))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # We expect 3 categories: Easy, Medium, Hard. 
    # Adjust width offset dynamically
    for i, cat in enumerate(labels):
        offset = (i - len(labels)/2) * width + (width/2)
        ax.bar(x + offset, gap_data[i], width, label=cat)

    ax.set_ylabel('Average Gap from Optimal (Bins)')
    ax.set_title('Heuristic Performance: Solution Quality (Lower is Better)')
    ax.set_xticks(x)
    ax.set_xticklabels(heuristics)
    ax.legend()
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "comparison_gap.png"))
    print("Saved comparison_gap.png")
    
    # --- PLOT 2: Average Time Comparison (Log Scale) ---
    # Time columns: FF_Time, FFD_Time, etc.
    
    time_data = []
    
    for cat in categories:
        cat_df = df[df['Category'] == cat]
        means = []
        for h in heuristics:
            col_name = f"{h}_Time"
            if col_name in cat_df.columns:
                means.append(cat_df[col_name].mean())
            else:
                means.append(0)
        time_data.append(means)
        
    fig, ax = plt.subplots(figsize=(14, 7))
    
    for i, cat in enumerate(labels):
        offset = (i - len(labels)/2) * width + (width/2)
        ax.bar(x + offset, time_data[i], width, label=cat)

    ax.set_ylabel('Average Time (seconds) - Log Scale')
    ax.set_title('Heuristic Performance: Computational Time (Lower is Better)')
    ax.set_xticks(x)
    ax.set_xticklabels(heuristics)
    ax.set_yscale('log') # Log scale because GA is much slower
    ax.legend()
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "comparison_time.png"))
    print("Saved comparison_time.png")

if __name__ == "__main__":
    generate_plots()


```

---

**User**

python run_experiments.py



Successfully loaded 6195 optimal solutions from Excel.

Instance Distribution:

  - Easy: 880 available -> 10 selected

  - Medium: 508 available -> 10 selected

  - Hard: 10 available -> 10 selected

Total tests: 30

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Cat      | Instance                       | Itm   Cap      | Opt  | FF    tFF      | FFD   tFFD     | FFD+  tFFD+    | BFL   tBFL     | NFD+  tNFD+    | MR+   tMR+     | GA    tGA

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Easy     | N2C1W2_L.txt                   | 100   100      | 62   | 62    0.0005   | 62    0.0004   | 62    0.0004   | 62    0.0002   | 76    0.0001   | 62    0.0001   | 63    0.94



are we sure that we put here all herustics that we have in columns ?! 



How many herusitics we have now at the moment?! 



---

**Cursor**

You currently have **15 algorithms** implemented in total (14 Heuristics + GA).

**1. Why are they not all in the console?**
The console output is limited to the "Best of Class" algorithms to prevent the text from wrapping and becoming unreadable. I hid the slower/basic versions (like standard `MR` or `BF`) and showed the optimized ones (`MR+`, `BFL`) instead.

**2. Complete List of Implemented Algorithms:**
All 15 are calculated and saved to your **Excel/TXT report**, even if they aren't printed to the console:

| Type | Basic | Decreasing (Sorted) | Optimized / Lookup | Optimized Decreasing |
| :--- | :--- | :--- | :--- | :--- |
| **First Fit** | `FF` | `FFD` | `FFL` (Lookup) | `FFD+` (Counting Sort) |
| **Best Fit** | `BF` | `BFD` | `BFL` (Lookup) | — |
| **Next Fit** | `NF` | `NFD` | — | `NFD+` (Counting Sort) |
| **Max Rest** | `MR` | `MRD` | `MR+` (Priority Queue) | `MRD+` (PQ + Sort) |
| **Meta** | `GA` | — | — | — |

**Total:** 4 (FF variants) + 3 (BF variants) + 3 (NF variants) + 4 (MR variants) + 1 (GA) = **15 Algorithms**.

**Next Step:**
Since you just ran the experiments, you can now generate the final "Master Plot" which **will** show every single one of these 15 algorithms:

```bash
python project/plot_results.py
```

This will give you the complete picture.



```shellscript
python project/plot_results.py
```

---

**User**

Table 2. Naming schemes used in gures 1 and 2



MR Max-Rest

MR+ Max-Rest using a priority queue

FF First-Fit

FF+ First-Fit using the vector container from the STL. Thus, “almost full” bins can be removed without having to re-order the array.

FF++ First-Fit using the map container from the STL. Thus, a lookup table is created that

determines the proper bin more rapidly.

FFD First-Fit-Decreasing using the Heapsort algorithm.

FFD+ First-Fit-Decreasing using FF+ and Counting Sort.

FFD++ First-Fit-Decreasing using FF++ and Counting Sort.

NF Next-Fit

NFD Next-Fit-Decreasing

NFD+ Next-Fit-Decreasing using Counting Sort.

BF Best-Fit



The thing is that i have implementaiton to this inside bin-packing-heuristics folder just in cpp not in python 



So just look into that folder if something you missed out 





The console output is limited to the "Best of Class" algorithms to prevent the text from wrapping and becoming unreadable. I hid the slower/basic versions (like standard MR or BF) and showed the optimized ones (MR+, BFL) instead.



I want every algotihm to be shown! I have space because i use 2k  monitor 

