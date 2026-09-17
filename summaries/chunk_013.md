## Important thesis facts

- The work compares one-dimensional bin-packing heuristics and a genetic algorithm, with solution quality measured as the number of bins and runtime measured in seconds. [chunk_013]
- The benchmark runner groups instances by capacity: Easy for capacity below 1,000, Medium for capacity from 1,000 through 99,999, and Hard for capacity at least 100,000. [chunk_013]
- The shown experiment configuration uses 10 sampled instances per category, GA population size 40, 50 generations, mutation probability 0.2, and one declared run per instance, although `RUNS_PER_INSTANCE` is not used in the shown loop. [chunk_013]
- The paper naming supplied by the user distinguishes MR, MR+, FF, FF+, FF++, FFD, FFD+, FFD++, NF, NFD, NFD+, and BF; in particular, FF+ uses an STL vector, FF++ uses an STL map/lookup table, FFD uses Heapsort, and the decreasing `+`/`++` variants combine the corresponding FF structure with Counting Sort. [chunk_013]
- The user states that implementations of the paper’s algorithms already exist in C++ under the `bin-packing-heuristics` folder and wants that folder inspected before deciding what the Python implementation is missing. [chunk_013]

## Decisions and rationale

- The user decided that every available algorithm must be printed in the console, rejecting the assistant’s choice to show only a smaller “best of class” subset; the user noted that a 2K monitor provides enough horizontal space. [chunk_013]
- The user asked for the existing C++ implementations in `bin-packing-heuristics` to be treated as the comparison point for identifying omissions in Python. [chunk_013]
- Earlier, the assistant proposed skipping the complex tree-based `++` variants “for now,” but that is an assistant proposal attributed to an earlier user preference and is not reaffirmed in the final user request. [chunk_013]
- The assistant chose lookup-based implementations for First Fit and Best Fit and Counting Sort for decreasing variants on the rationale that integer item sizes permit faster lookup/sorting, while noting that a capacity-indexed lookup may be unattractive for capacity 100,000. [chunk_013]

## Algorithms/formulas

- The baseline algorithms shown are First Fit (`FF`), Next Fit (`NF`), Best Fit (`BF`), and Max-Rest/Worst-Fit (`MR`); decreasing variants are produced by sorting item IDs by descending item size before calling the same packing function. [chunk_013]
- `first_fit` scans bins in creation order and places an item in the first bin whose used capacity plus item size is at most capacity plus `1e-6`. [chunk_013]
- `next_fit` considers only the current final bin and opens a new bin whenever the next item does not fit. [chunk_013]
- `best_fit` scans all bins and selects the feasible bin with the smallest residual capacity. [chunk_013]
- `max_rest` scans all bins and selects the feasible bin with the largest residual capacity. [chunk_013]
- `max_rest_pq` represents MR+ with a heap of negative remaining capacities, making the bin with the greatest remaining space available at the heap root; it is described in the code as `O(N log N)` rather than the scanning implementation’s `O(N^2)`. [chunk_013]
- `counting_sort` buckets item IDs by integer item size and reconstructs them from the largest size to zero; the runner falls back to ordinary descending sort if any item size is non-integral. [chunk_013]
- `first_fit_lookup` stores a last-used bin index keyed by item size and resumes the First Fit scan from that index. [chunk_013]
- `best_fit_lookup` uses an array indexed by exact remaining capacity and searches upward from the integer item size for the smallest available residual bucket; it falls back to ordinary Best Fit only when bin capacity itself is non-integral. [chunk_013]
- The assistant’s stated inventory is 14 heuristics plus GA, 15 algorithms total: FF, FFD, FFL, FFD+, BF, BFD, BFL, NF, NFD, NFD+, MR, MRD, MR+, MRD+, and GA. This count is a claim based on the shown Python runner, not a confirmed match to the paper or C++ folder. [chunk_013]

## Implementation details

- The shown `heuristic.py` code imports `heapq` and defines `first_fit`, `next_fit`, `best_fit`, `max_rest`, `counting_sort`, `first_fit_lookup`, `best_fit_lookup`, and `max_rest_pq`. [chunk_013]
- The shown `run_experiments.py` imports those functions, discovers every `.txt` file under `data`, parses all contained instances, attaches source folder/file metadata, randomly samples up to 10 instances from each category, and writes results to `results/experiment_results.xlsx` and `results/experiment_results.txt`. [chunk_013]
- `solve_heuristic` records wall-clock duration, optionally applies ordinary descending sort or Counting Sort, invokes the selected packing function, and returns bin count plus duration. [chunk_013]
- The expanded result row shown includes value/time columns for FF, FFD, FFL, FFD+, BF, BFD, BFL, NF, NFD, NFD+, MR, MRD, MR+, MRD+, and GA, plus instance metadata, optimal value, and `Gap_GA`. [chunk_013]
- The shown console header and print statement intentionally include only FF, FFD, FFD+, BFL, NFD+, MR+, and GA, even though more columns are written to the DataFrame and text report; this directly conflicts with the user’s final display requirement. [chunk_013]
- The detailed text report shown prints most variants but its final MR line omits `MRD+`, despite `MRD+` being computed and stored in Excel. [chunk_013]
- The plotting script reads the Excel results, computes `Gap_<algorithm> = algorithm result - Optimal`, and creates average-gap and log-scale average-time bar charts across Easy, Medium, and Hard categories for the stated 15-algorithm list. [chunk_013]
- The runner creates a bin visualization and a convergence plot for every tested instance, despite a comment saying convergence plots should be saved only for the first instance of each category or every fifth instance. [chunk_013]
- Multiple near-duplicate versions of `run_experiments.py` are shown in the conversation; the chunk does not establish which version was actually saved, except that the observed console output matches the reduced-column version. [chunk_013]

## Experiments/results

- The user reports running `python run_experiments.py`; the observed output says 6,195 optimal solutions were loaded from Excel. [chunk_013]
- The observed instance distribution is 880 Easy, 508 Medium, and 10 Hard instances, with 10 sampled from each category for 30 total tests. [chunk_013]
- The first shown result is `N2C1W2_L.txt` with 100 items, capacity 100, and optimum 62; FF, FFD, FFD+, BFL, and MR+ each use 62 bins, NFD+ uses 76, and GA uses 63 in 0.94 seconds. [chunk_013]
- The displayed heuristic timings for that row range from 0.0001 to 0.0005 seconds, but this is a single observed row from one random sample and does not establish comparative performance generally. [chunk_013]
- No observed output from `plot_results.py`, no inspection of the C++ folder, and no validation of algorithm equivalence are present in this chunk. [chunk_013]

## Sources/references

- The assistant cites Bastian Rieck’s paper *Basic Analysis of Bin-Packing Heuristics* as the basis for the proposed lookup and Counting Sort variants, but no bibliographic metadata, quotations with page references, or independently checked paper text appear in the chunk. [chunk_013]
- The user supplies the text of “Table 2. Naming schemes used in figures 1 and 2,” which is the strongest source in this chunk for the intended meanings of FF+, FF++, FFD, FFD+, FFD++, and related abbreviations. [chunk_013]
- The existing C++ code in `bin-packing-heuristics` is identified by the user as an implementation source, but it is not opened or reviewed in this chunk. [chunk_013]
- `data/Solutions.xlsx` is used by `SolutionManager` as the source of optimal values when an instance does not provide `best_known`; the observed run reports 6,195 loaded solutions. [chunk_013]

## Rejected approaches

- The user rejects limiting console output to selected optimized or “best of class” algorithms and requires every algorithm to be displayed. [chunk_013]
- Treating FFL/BFL as sufficient coverage of the paper’s named FF+/FF++ family is not accepted as settled; the user directs the assistant to compare against the existing C++ implementations. [chunk_013]
- Implementing more Python variants without first checking `bin-packing-heuristics` is implicitly rejected by the user’s instruction to inspect that folder for anything missed. [chunk_013]
- The earlier plan to skip `++` variants remains only a provisional assistant proposal and may be superseded by the user’s later request to account for all implemented algorithms. [chunk_013]

## Unresolved questions

- Which algorithms and data structures are actually implemented in the C++ `bin-packing-heuristics` folder, and which of them lack faithful Python equivalents? [chunk_013]
- How should the Python names FFL and BFL map to the paper’s FF+, FF++, FFD+, and FFD++ names, if at all? [chunk_013]
- Is the shown `first_fit_lookup` algorithm behaviorally equivalent to the paper’s FF++ lookup-table method, or is it merely a different optimization with a similar label? [chunk_013]
- Is `best_fit_lookup` part of the cited paper’s required comparison set? The user-provided naming table ends at BF and does not establish a BFL abbreviation. [chunk_013]
- The `best_fit_lookup` implementation truncates item sizes and residual capacities with `int()` after checking only that bin capacity is integral; correctness for non-integral item sizes is therefore uncertain. [chunk_013]
- The capacity-indexed Best Fit lookup allocates `capacity + 1` buckets and scans up to capacity for each item, so its actual speed and memory behavior on Hard instances with capacity 100,000 remain unverified. [chunk_013]
- The final console layout that includes all algorithms, their timings, optimum, GA gap, and any desired non-GA gaps has not yet been designed or shown. [chunk_013]
- It is unclear whether GA should be counted as a heuristic in the user-facing total; the assistant reports 14 heuristics plus GA, while the user asks how many heuristics exist. [chunk_013]
- Random sampling has no shown seed, so reruns may select different Easy and Medium instances; repeatability is unresolved. [chunk_013]
- No evidence in the chunk confirms that any of the displayed code blocks were written to repository files or passed syntax, unit, equivalence, or end-to-end validation. [chunk_013]
