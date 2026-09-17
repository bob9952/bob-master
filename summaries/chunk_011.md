## Important thesis facts

- [Evidence: experiment console output] The project studies one-dimensional bin packing by comparing a permutation-based genetic algorithm (GA) with constructive heuristics: First Fit (FF), First Fit Decreasing (FFD), Best Fit (BF), Best Fit Decreasing (BFD), Next Fit (NF), Next Fit Decreasing (NFD), Max-Rest/Worst-Fit (MR), and Max-Rest Decreasing (MRD). [chunk_011]
- [Evidence: experiment console output] `SolutionManager` reported loading 6,195 optimal solutions from Excel; available instances were split into 880 Easy, 508 Medium, and 10 Hard cases, and the displayed run randomly sampled 10 from each category for 30 tests total. [chunk_011]
- [Evidence: code shown in conversation] Difficulty was defined only by bin capacity: Easy when capacity is below 1,000, Medium when capacity is at least 1,000 but below 100,000, and Hard when capacity is at least 100,000. This is a project-specific experimental classification, not an established theoretical hardness measure. [chunk_011]
- [User choice] The user liked the Excel/report output and Easy/Medium/Hard distribution, did not think a logarithmic plot scale was currently needed, and wanted to improve the work incrementally. [chunk_011]
- [User choice] The user endorsed comparing a GA decoded with First Fit against one decoded with Best Fit and was interested in adding missing heuristic variants from the cited heuristic-analysis PDF. [chunk_011]

## Decisions and rationale

- [User choice] Keep the existing readable Excel, text, and plot outputs and explore additions on top of them rather than replacing the reporting approach. [chunk_011]
- [Assistant proposal, not verified as completed] Add priority-queue Max-Rest (`MR+`) and its decreasing-order variant (`MRD+`) because the PDF describes the priority queue as the main optimized MR implementation and because it should preserve MR solution quality while changing runtime. [chunk_011]
- [Assistant proposal] Retain both ordinary MR/MRD and MR+/MRD+ in the comparison so any runtime difference can be observed, although the assistant warned that instances with only 100–500 items may be too small to show a meaningful speedup. [chunk_011]
- [Assistant proposal] Defer the PDF's map/vector-optimized First Fit and capacity-indexed Best Fit variants; the assistant judged FF optimization more delicate to reproduce correctly and argued that a capacity lookup for BF could be counterproductive when capacity is 100,000 but there are only about 50–100 bins. [chunk_011]
- [Assistant proposal] Further GA work could test fitness exponent values such as `k=3` or `k=4`, larger populations, and separate FF and BF decoders. These are ideas, not reported experiments in this chunk. [chunk_011]

## Algorithms/formulas

- [Evidence: source excerpt supplied by user] The PDF naming scheme is MR = Max-Rest, MR+ = Max-Rest with a priority queue, FF = First Fit, FF+ = FF with an STL vector that removes almost-full bins, FF++ = FF with an STL map lookup, FFD = decreasing-order FF with Heapsort, FFD+/FFD++ = optimized FF plus Counting Sort, NF = Next Fit, NFD/NFD+ = decreasing-order NF with ordinary/Counting Sort, and BF = Best Fit. [chunk_011]
- [Evidence: source excerpt supplied by user] Replacing Heapsort with Counting Sort for FFD and NFD changes sorting from `O(n log n)` to `O(n)` when its assumptions apply. [chunk_011]
- [Evidence: source excerpt supplied by user] A bin may be closed once its remaining capacity is smaller than the minimum item weight; the excerpt prints the “limit capacity” relation as `c_l = K - w`, but the wording/formula should be checked against the original PDF because the pasted text is encoding-damaged and potentially inconsistent. [chunk_011]
- [Evidence: source excerpt supplied by user] The PDF says its map-based FF stores a bin index for an item weight and can skip earlier bins for later items of at least that weight; its asymptotic bound remains `O(n^2)`. [chunk_011]
- [Code shown, claimed complexity] Proposed `max_rest_pq` uses Python `heapq` with keys `(-remaining_capacity, bin_index)`, always tries the bin with maximum free capacity, reinserts it after placement, and opens a new bin if the maximum-space bin cannot fit the item; the assistant labels it `O(n log n)` versus scan-based MR's `O(n^2)`. [chunk_011]
- [Evidence: code shown in conversation] The heuristic wrapper creates the item-key order, optionally sorts keys by descending item size, invokes the selected packing function, and reports the number of returned bins and elapsed time; this same switch produces ordinary and decreasing variants. [chunk_011]
- [Evidence: code shown in conversation] GA gap is computed as `GA bins - optimal bins` when an optimum is available. [chunk_011]

## Implementation details

- [Evidence: code shown in conversation] The experiment settings shown were `SAMPLES_PER_FOLDER = 10`, `POP_SIZE = 40`, `GENERATIONS = 50`, `RUNS_PER_INSTANCE = 1`, and GA mutation probability `0.2`; `RUNS_PER_INSTANCE` was declared but the displayed loop ran one GA construction directly per selected instance. [chunk_011]
- [Evidence: code shown in conversation] Instance files are recursively read from `project/data`, parsed with `parse_instance_file`, tagged with source folder/file metadata, sampled via `random.sample`, and written through pandas to `project/results/experiment_results.xlsx` plus a readable text log. [chunk_011]
- [Evidence: observed commands] `python run_experiments.py` generated the table and result files; `python plot_results.py` reported saving `comparison_gap.png` and `comparison_time.png`. [chunk_011]
- [Assistant proposal/code, completion uncertain] The repeated patch text imports `heapq`, adds `max_rest_pq` to `project/src/heuristic.py`, imports it in `project/run_experiments.py`, executes MR+/MRD+, and adds their bin counts/timings to console, Excel, and text output. The transcript contains repeated code blocks but no test run proving the edits were applied successfully. [chunk_011]
- [Evidence: Git status supplied by user] The parent repository reported `BPPLIB (untracked content)`, `Metaheuristic-Algorithms (modified content)`, and deletion of the Excel lock file `project/results/~$experiment_results.xlsx`; this indicates nested-repository/submodule state requires inspection before deciding how to stage files. [chunk_011]
- [Uncertain assistant advice] The assistant suggested either committing changes inside actual submodules or converting them to normal directories with `git rm --cached` and re-adding files, but `.gitmodules`, gitlink index entries, and nested `.git` metadata were not actually inspected; `dir /a BPPLIB\.git` returned “file not found.” [chunk_011]

## Experiments/results

- [Evidence: observed 30-instance run] GA achieved the optimum on 3/10 Easy cases, 6/10 Medium cases, and 0/10 Hard cases; its gaps were Easy `0–5`, Medium `0–3`, and Hard `2–3`. [chunk_011]
- [Evidence: observed 30-instance run] On all ten Hard instances, GA used 58 or 59 bins while FF/FFD/BF/BFD/MR/MRD used 59 or 60 bins; GA improved those heuristics by one bin in 9/10 cases and tied them on `HARD0.txt`. NF/NFD were worse at 63–66 bins. [chunk_011]
- [Evidence: observed 30-instance run] On Easy cases, GA was not uniformly better: for example `N4C2W1_A.txt` had optimum/FF/BF 210 versus GA 215, and `N3C3W2_I.txt` had optimum 79, FF/BF 80, and GA 82. [chunk_011]
- [Evidence: observed 30-instance run] `Falkenauer_t120_07.txt` gave optimum 40, FF/BF/NF/MR 40, FFD/BFD/MRD 46, NFD 48, and GA 43; this demonstrates that decreasing order can worsen these heuristics on a particular instance and that GA was not best there. [chunk_011]
- [Evidence: observed timings] Constructive heuristics generally completed below about 0.014 seconds in the displayed run, while GA ranged from 0.18 to 18.35 seconds; the clearest result is a substantial quality/runtime trade-off, not universal GA dominance. [chunk_011]
- [Evidence: source excerpt supplied by user, external benchmark] The PDF reports Next Fit as fastest because it manages only one bin, priority-queue Max-Rest as nearly as fast, and FF/FFD as the slowest in its C++ `-O3` tests on an Intel Celeron M 1.5 GHz; it warns that very small timings are inaccurate due to timer resolution. These external timings are not directly comparable with the Python experiments. [chunk_011]
- [Assistant interpretation, partly contradicted by data] The assistant characterized GA as generally matching or beating heuristics and called the results “excellent,” but the Easy results include several cases where FF/BF are better; thesis claims should therefore use aggregate statistics and exact counts rather than that broad characterization. [chunk_011]

## Sources/references

- [User-supplied source] Bastian Rieck, *Basic Analysis of Bin-Packing Heuristics* (PDF title as supplied); the pasted material includes algorithm naming, implementation notes, runtime discussion, and benchmark table excerpts, but full bibliographic metadata was not provided. [chunk_011]
- [Reference quoted from supplied PDF; not independently verified] Janos Balogh, Jozsef Bekesi, Gabor Galambos, and Gerhard Reinelt, “Lower bound for the online bin packing problem with restricted repacking,” *SIAM Journal on Computing* 38(1), 398–410 (2008). [chunk_011]
- [Reference quoted from supplied PDF; not independently verified] Janos Balogh, Jozsef Bekesi, Gabor Galambos, and Gerhard Reinelt, “On-line bin packing with restricted repacking,” *Journal of Combinatorial Optimization* 27(1), 115–131 (2014). [chunk_011]
- [Reference quoted from supplied PDF; not independently verified] Michael R. Garey and David S. Johnson, *Computers and Intractability: A Guide to the Theory of NP-Completeness*, W. H. Freeman & Co. (listed in the pasted bibliography as 1990). [chunk_011]
- [Evidence quality note] The PDF excerpts contain mojibake and malformed mathematical symbols, so names, accents, dates, formulas, page numbers, and quotations must be checked against the original document before thesis citation. [chunk_011]

## Rejected approaches

- [User choice] A logarithmic scale for plots was not wanted at this stage, though the user left open revisiting it later. [chunk_011]
- [Assistant decision/proposal] Do not immediately implement every PDF variant; prioritize MR+ because it is straightforward, while postponing FF+/FF++ due to correctness complexity. [chunk_011]
- [Assistant decision/proposal] Do not implement a capacity-indexed `BF++` for the current benchmark mix because scanning up to capacity 100,000 may cost more than scanning the relatively small number of open bins. This was reasoned but not benchmarked. [chunk_011]
- [Assistant advice requiring caution] Do not assume `git add --recursive` solves the repository display issue; if the directories are gitlinks/submodules, the parent tracks their commit objects rather than all nested files. Conversely, converting them to normal directories should not be attempted until the actual repository metadata and intended ownership are confirmed. [chunk_011]

## Unresolved questions

- [Unresolved] Were the proposed `max_rest_pq`, MR+, and MRD+ edits actually written to the working tree, and do focused correctness tests show MR and MR+ always produce identical bin counts for the same order? [chunk_011]
- [Unresolved] How should GA-with-FF versus GA-with-BF be represented in the chromosome/decoder design, and will both variants use identical seeds, populations, stopping rules, and repeated runs for a fair comparison? [chunk_011]
- [Unresolved] The experiment uses unseeded random sampling and only one stochastic GA run per instance; a reproducible seed, fixed benchmark set, multiple independent runs, dispersion measures, and statistical comparison remain to be designed. [chunk_011]
- [Unresolved] Capacity thresholds are being used as proxies for Easy/Medium/Hard; the thesis needs a defensible rationale or a stronger difficulty definition based on instance family, size, structure, known gap, or empirical behavior. [chunk_011]
- [Unresolved] Aggregate metrics still need to be reported, such as mean/median absolute gap, percentage gap, optimum-hit rate, runtime distribution, and paired comparisons by category and dataset family. [chunk_011]
- [Unresolved] The anomalous Falkenauer result and the assistant's unsupported description of it as a known “Triplets” dataset should be verified from the source data/literature before inclusion. [chunk_011]
- [Unresolved] Determine whether `BPPLIB` and `Metaheuristic-Algorithms` are registered git submodules/gitlinks, nested repositories, or ordinary folders, and whether the user wants their full source copied into the main repository or only submodule commit references. [chunk_011]
- [Unresolved] Confirm the exact formulas and implementation semantics in the original PDF, especially the printed limit-capacity relation and the precise FF+/FF++/BF++ data structures, before reproducing or citing them. [chunk_011]
