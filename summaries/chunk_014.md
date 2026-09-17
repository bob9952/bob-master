## Important thesis facts

- [User-provided benchmark description] The benchmark collection supports BPP format (`n`, bin capacity `c`, then one weight per item) and CSP format (`m`, `c`, then weight-demand pairs); parser compatibility with both formats was not demonstrated in this chunk. [chunk_014]
- [User-provided benchmark description] Falkenauer contains 160 instances: 80 uniform instances with `n=120..1000`, `c=150`, and 80 triplet instances with `n=60..501`, `c=1000`. [chunk_014]
- [User-provided benchmark description] Scholl contains 1,210 instances split into sets of 720, 480, and 10; capacities are `100..150`, `1000`, and `100000`, respectively, with `n=50..500`. [chunk_014]
- [User-provided benchmark description] Wäscher contains 17 historically difficult instances with `n=27..239` and `c=10000`; Hard28 contains 28 instances with `n=160..200` and `c=1000`; Schwerin contains two sets of 100 instances with `n=100` and `n=120`, both with `c=1000`. [chunk_014]
- [User-provided benchmark description] The Delorme-Iori-Martello random set varies `n`, capacity, and item-weight bounds, with 10 instances per parameter quadruple; ANI/AI and GI are additional named difficult/benchmark families. [chunk_014]
- [Confirmed run output] `Solutions.xlsx` has nine sheets whose row counts sum exactly to 6,195: Falkenauer 160, Scholl 1,210, Wäscher 17, Schwerin 200, Schoenfield Hard28 28, Randomly Generated 3,840, Augmented Non-IRUP 250, Augmented IRUP 250, and GI 240. [chunk_014]
- [Caution] The message “Successfully loaded 6195 optimal solutions” is stronger than the evidence: the run confirms 6,195 unique names/rows loaded, but the shown verifier does not validate `Best LB == Best UB`, `Status == Solved`, or which bound `SolutionManager` uses. [chunk_014]

## Decisions and rationale

- [User decision/request] Inspect the remaining C++ heuristic implementations, validate mapping between local instances and all sheets of `Solutions.xlsx`, and correct the unexpectedly small hard-instance pool. [chunk_014]
- [Proposed decision] Treat Scholl set 3, Wäscher, and Hard28 as hard by dataset identity rather than capacity alone, because capacity thresholds classify only the 10 Scholl set-3 instances as hard. [chunk_014]
- [Proposed decision] Use a verification script that loads every workbook sheet and compares local `.txt` filenames with workbook `Name` values before relying on the optimal-solution mapping. [chunk_014]
- [Proposed experiment design] Sample up to 10 instances from each Easy/Medium/Hard category and print all heuristic result/time columns to exploit an ultra-wide console. [chunk_014]

## Algorithms/formulas

- [Code shown] First Fit scans bins in opening order and uses the first bin satisfying `used + item_size <= capacity + 1e-6`; otherwise it opens a bin. [chunk_014]
- [Code shown] Next Fit considers only the current last bin, opening a new bin when the next item does not fit. [chunk_014]
- [Code shown] Best Fit selects a feasible bin with minimum residual capacity, while Max-Rest/Worst-Fit selects one with maximum residual capacity. [chunk_014]
- [Code shown] Decreasing variants sort item IDs by descending weight; for integral weights, the proposed “plus” variants may use descending counting sort, otherwise they fall back to Python sorting. [chunk_014]
- [Code shown, naming unverified] `first_fit_lookup` stores, per item size, a bin index from which later searches begin and is described as analogous to C++ FF++; equivalence to the source algorithm was asserted but not evidenced with tests in this chunk. [chunk_014]
- [Code shown] `best_fit_lookup` buckets bin indices by integer remaining capacity and searches upward from the item size; non-integral bin capacity falls back to ordinary Best Fit, although integral item weights are only assumed, not enforced inside the function. [chunk_014]
- [Code shown] `max_rest_pq` maintains `(-remaining_capacity, bin_index)` in `heapq`, giving an intended `O(n log n)` Max-Rest implementation instead of scanning all bins. [chunk_014]
- [Code shown] GA gap is calculated as `ga_bins - optimal` when an optimal value is truthy; otherwise the code records zero, which can conceal missing-reference data. [chunk_014]

## Implementation details

- [Code shown] The experiment runner recursively parses every `.txt` under `data`, annotates parsed instances with source folder/file, runs FF/FFD/FF lookup/counting-sort, BF/BFD/BF lookup, NF/NFD/counting-sort, MR/MRD/priority-queue variants, and one GA run. [chunk_014]
- [Code shown] Reduced test settings are `SAMPLES_PER_FOLDER=10`, `POP_SIZE=40`, `GENERATIONS=50`, `RUNS_PER_INSTANCE=1`, and GA mutation probability `0.2`; `RUNS_PER_INSTANCE` is declared but not used in the shown loop. [chunk_014]
- [Code shown] Outputs include a wide console table, detailed text log, Excel results, one bin visualization per tested instance, and convergence plots of best and average fitness. [chunk_014]
- [Code shown] Workbook verification uses `pd.read_excel(..., sheet_name=None, engine='openpyxl')`, flattens non-null `Name` values into a dictionary, and compares them with local `.txt` basenames or basenames without extensions. [chunk_014]
- [Implementation defect in shown proposal] `is_hard28` is computed during result-row categorization but omitted from the `if capacity >= 100000 or is_wascher` condition; the earlier pool-building condition also checks Wäscher but not Hard28, so the proposed code does not actually move Hard28 into Hard. [chunk_014]
- [Implementation concern] The shown Wäscher detection mixes `Waescher` in an instance name with `Wäscher` in a folder name and does not show normalization for mojibake or alternative spellings; robust matching remains unverified. [chunk_014]
- [Implementation concern] Sorting each sampled list happens after `final_test_set.extend(selected)`, so it does not reorder the already-copied combined test list. [chunk_014]

## Experiments/results

- [Confirmed run output] The verifier loaded 6,195 unique workbook names across all nine sheets. [chunk_014]
- [Confirmed run output] It found 1,255 of 1,263 local `.txt` files by its filename comparison and reported eight missing files: `T\binpack5.txt` through `T\binpack8.txt` and `U\binpack1.txt` through `U\binpack4.txt`. [chunk_014]
- [Confirmed diagnosis from shown categorization] A capacity-only hard rule of `capacity >= 100000` explains the observed count of 10 by selecting Scholl set 3 while placing Wäscher (`c=10000`) and Hard28 (`c=1000`) in Medium. [chunk_014]
- [Derived expectation, conditional] If all three named families are present and intentionally defined as Hard, their combined pool should contain at least 55 instances (`10 + 17 + 28`); this was not confirmed by a post-fix run. [chunk_014]
- [No evidence yet] No heuristic correctness tests, C++/Python result comparisons, GA performance results, or corrected category counts were executed in the chunk. [chunk_014]

## Sources/references

- [User-provided citation] E. Falkenauer, “A hybrid grouping genetic algorithm for bin packing,” *Journal of Heuristics* 2(1):5-30, 1996; instances said to come from OR-Library. [chunk_014]
- [User-provided citation] A. Scholl, R. Klein, and C. Jürgens, “Bison: a fast hybrid procedure for exactly solving the one-dimensional bin packing problem,” *Computers & Operations Research* 24(7):627-645, 1997. [chunk_014]
- [User-provided citation] G. Wäscher and T. Gau, “Heuristics for the integer one-dimensional cutting stock problem: a computational study,” *OR Spectrum* 18(3):131-144, 1996. [chunk_014]
- [User-provided citation] P. Schwerin and G. Wäscher, “The bin-packing problem: a problem generator and some numerical experiments with FFD packing and MTP,” *International Transactions in Operational Research* 4(5-6):377-389, 1997. [chunk_014]
- [User-provided citation] J. E. Schoenfield, “Fast, exact solution of open bin packing problems without linear programming,” technical report, US Army Space and Missile Defense Command, 2002. [chunk_014]
- [User-provided citation] M. Delorme, M. Iori, and S. Martello, “Bin Packing and Cutting Stock Problems: Mathematical Models and Exact Algorithms,” *European Journal of Operational Research* 255(1):1-20, 2016. [chunk_014]
- [User-provided citation] T. Gschwind and S. Irnich, “Dual Inequalities for Stabilized Column Generation Revisited,” *INFORMS Journal on Computing* 28(1):175-194, 2016. [chunk_014]
- [Assistant claim, unverified in chunk] The relevant C++ logic files were said to be `first-fit.cpp`, `best-fit.cpp`, `next-fit.cpp`, `max-rest.cpp`, with only the custom heap implementation `simple-heap.cpp` remaining; no C++ source excerpts or file listing were included as evidence. [chunk_014]

## Rejected approaches

- [Rejected approach] Defining difficulty solely as `capacity >= 100000` was rejected because benchmark difficulty is family-specific and this rule captures only Scholl set 3. [chunk_014]
- [Rejected/limited approach] Reading only the workbook’s default first sheet is insufficient; all sheets must be loaded to account for the full benchmark catalogue. [chunk_014]
- [Rejected need, assistant opinion] Reimplementing the internal C++ custom heap was considered unnecessary because Python `heapq` can provide the required priority-queue behavior; correctness parity still needs behavioral validation. [chunk_014]

## Unresolved questions

- [Unresolved] Does the actual `SolutionManager` load all sheets, choose `Best UB` appropriately, normalize names consistently, and reject unsolved rows or unequal lower/upper bounds? Its implementation was not shown. [chunk_014]
- [Unresolved] Are the eight unmatched `binpack*.txt` files genuinely absent from the workbook, or are they container files whose parsed internal instance names map to workbook rows? The verifier compares files, not parsed instance names. [chunk_014]
- [Unresolved] Are copied Wäscher files BPP or CSP, and can the existing parser preserve demands correctly if they are CSP? No sample file was inspected. [chunk_014]
- [Unresolved] Which explicit, normalized dataset/folder rules should define Easy, Medium, and Hard, particularly for Hard28, Wäscher, ANI/AI, GI, and augmented IRUP families? [chunk_014]
- [Unresolved] Do the Python lookup/counting-sort/priority-queue variants return identical bin counts and assignments to the C++ implementations on controlled fixtures, and are labels such as `FFD+`, `FFL`, `BFL`, `MR+`, and `MRD+` faithful to the paper? [chunk_014]
- [Unresolved] The sampling is nondeterministic because no random seed is shown; a reproducibility policy for thesis experiments remains to be decided. [chunk_014]
