## Important thesis facts

- Actual user-reported run evidence: `SolutionManager` loaded 6,195 optimal solutions from `Solutions.xlsx`, and the parser/categorizer found 880 Easy, 480 Medium, and 55 Hard instances; 10 were randomly sampled from each category, for 30 planned tests. The pasted output is partial, so completion of all 30 tests is not established here. [chunk_015]
- Assistant-reported verification, not independently evidenced in this chunk: 17 Waescher rows and 28 Hard28 rows were loaded from Excel, and 1,255 of 1,263 local files matched (reported as 99.4%). The assistant’s stronger statement that coverage was “100%” is an interpretation that still depends on the multi-instance parsing claim. [chunk_015]
- Assistant explanation, unverified in this chunk: the eight unmatched physical files, `binpack1.txt` through `binpack8.txt`, are Falkenauer containers holding 20 instances each; Excel records the contained instance names (for example, `Falkenauer_u120_00.txt`) rather than the container filenames, and the parser allegedly splits and renames them accordingly. [chunk_015]
- The experiment compares constructive heuristics and variants against a genetic algorithm, using known/best-known bin counts as the quality reference and execution time as a second metric. [chunk_015]

## Decisions and rationale

- Code decision shown in the proposed/repeated `run_experiments.py`: classify an instance as Hard when capacity is at least 100,000 or its folder/name identifies Waescher or Hard28; this was intended to prevent recognized hard benchmark families from being misclassified solely by capacity. [chunk_015]
- Experiment configuration shown in code: sample at most 10 instances from each Easy/Medium/Hard category, use GA population size 40, 50 generations, mutation probability 0.2, and one run per instance. Comments describe the population and generation values as reduced for faster testing, so these are development-scale settings rather than justified final thesis parameters. [chunk_015]
- Presentation decision requested by the user: keep the detailed Excel output, which the user approved, but simplify terminal output because the full table does not fit a 2K monitor; terminal rows should retain capacity, item count, heuristic results, GA result, and GA time, with one additional decimal place for short timings. This request is not implemented within the chunk. [chunk_015]
- Earlier display proposal/code reduced the instance column from 30 to 20 characters and truncated long names to 17 characters plus `..`; this only partially addressed width and was superseded by the user’s request to remove excess console fields. [chunk_015]

## Algorithms/formulas

- Heuristics invoked in code are First Fit (FF), First Fit Decreasing (FFD), lookup-based First Fit (FFL), Best Fit (BF), Best Fit Decreasing (BFD), lookup-based Best Fit (BFL), Next Fit (NF), Next Fit Decreasing (NFD), Max Rest (MR), Max Rest Decreasing (MRD), priority-queue Max Rest (`MR+`), and its decreasing form (`MRD+`). [chunk_015]
- `FFD+` and `NFD+` use counting sort before First Fit or Next Fit when all item values are integral; for non-integral values, the wrapper falls back to the standard descending sort. [chunk_015]
- The recorded GA absolute gap is `Gap_GA = GA_bins - optimal_bins` when an optimal value is truthy; otherwise the code records zero. That fallback can make a missing optimum indistinguishable from a true zero gap. [chunk_015]
- Category rule in code: Hard if `capacity >= 100000` or Waescher/Hard28 is identified; otherwise Medium if `capacity >= 1000`; otherwise Easy. This is an experiment-specific stratification rule, not a cited theoretical definition of bin-packing difficulty. [chunk_015]

## Implementation details

- Proposed/repeated code recursively walks `project/data` for `.txt` files, parses every physical file with `parse_instance_file`, and adds source folder/file metadata to every parsed logical instance. [chunk_015]
- Optimal values are taken first from `instance['best_known']`; when that value is falsy, the code queries `SolutionManager.get_optimal(name)`. [chunk_015]
- `solve_heuristic` copies item keys, optionally sorts them, times only the selected heuristic call plus sorting performed inside the wrapper, and returns the number of bins and elapsed wall-clock seconds using `time.time()`. [chunk_015]
- The GA is instantiated per selected instance as `GeneticAlgorithm(items, capacity, pop_size=40, generations=50, mutation_prob=0.2)`; the returned best solution supplies `num_bins`. GA runtime is measured around construction plus `run()`. [chunk_015]
- For every processed instance, code generates a bin visualization and a convergence plot containing best and average fitness by generation. Although a comment says convergence plots might be saved only for selected instances, the shown implementation saves one for every instance. [chunk_015]
- Results are accumulated with dataset metadata, bin counts, timings for all algorithms, GA bin count/time, and GA gap, then exported to `results/experiment_results.xlsx`; a detailed text report is also written incrementally to `results/experiment_results.txt`. [chunk_015]
- The code contains `RUNS_PER_INSTANCE = 1`, but the loop does not use that variable; it performs exactly one GA/heuristic evaluation per sampled instance. Random sampling and GA behavior are not seeded in the shown code. [chunk_015]
- Multiple near-identical full code listings occur in the conversation, including an earlier categorization pass that omitted Hard28 and later versions that include it. These listings are proposals/conversation artifacts, not proof of the current repository contents. [chunk_015]

## Experiments/results

- Actual partial run evidence shows the revised classification produced 55 available Hard instances rather than the earlier reported 10, consistent with adding Waescher and Hard28 recognition; because only sampled output is pasted, the exact composition of those 55 is not directly verified. [chunk_015]
- In the pasted Easy sample, many heuristics reached the listed optimum, whereas Next Fit variants were often worse; examples include `N3C1W4_E` with optimum 142, FF/FFD/BF/MR families at 142, NF/NFD/NFD+ at 163, and GA at 142 in 3.28 s. [chunk_015]
- On `Falkenauer_u500_0..` (name truncated in console), the listed optimum was 206; FFD/BFD produced 207, MRD/MRD+ 209, GA 213 in 11.89 s, FF/FFL 219, and the shown Next Fit variants 272 or 292. This is one sampled observation, not an aggregate conclusion. [chunk_015]
- GA sometimes matched or improved on the displayed heuristic results (`N1C3W2_I`: optimum/GA 19 while shown heuristics produced 20; `N3W2B1R2`: optimum/GA 41 while most shown heuristics produced 44), but it also missed the optimum (`N4C2W2_M`: optimum 261, GA 265; `N1C1W1_A`: optimum 25, GA 26). [chunk_015]
- The displayed heuristic runtimes are generally fractions of a millisecond to a few milliseconds, while displayed GA times range from about 0.14 s to 14.04 s in the pasted rows. These are raw single-run observations and should not be treated as stable performance estimates. [chunk_015]
- A separate earlier partial run printed one Easy instance, `N4C2W4_I`, with optimum 287; all shown non-Next-Fit heuristics returned 287, Next Fit variants returned 376, and GA returned 292 in 16.31 s. [chunk_015]

## Sources/references

- No bibliographic source, paper, DOI, URL, or formal benchmark citation is supplied in this chunk. Dataset-family names mentioned are Falkenauer, Waescher, Hard28, and Scholl 3, but their provenance must be documented elsewhere before thesis use. [chunk_015]
- `Solutions.xlsx` is the implementation’s reference source for optimal/best-known values, but the chunk does not establish who produced it, its version, or whether every value is proven optimal rather than merely best known. [chunk_015]

## Rejected approaches

- Capacity-only Hard classification (`capacity >= 100000`) was rejected because it yielded only 10 Hard instances and omitted recognized Waescher and Hard28 cases. [chunk_015]
- Printing every metric and timing in a single ultra-wide terminal table was rejected by the user because it did not fit the available display; the detailed Excel format was explicitly retained as desirable. [chunk_015]
- A 30-character instance column was rejected as too wide; reducing it to 20 characters helped but did not resolve the broader console-density problem. [chunk_015]
- Relying on the assistant’s Python execution environment was abandoned after it reported that `python` resolved to a Windows/Microsoft Store alias and could not run; the user executed the experiment manually. [chunk_015]

## Unresolved questions

- The final compact terminal schema still needs implementation: the user requested capacity and item count, heuristic outcomes, GA, and `tGA`, fewer other printed fields, and one more decimal digit for timing. It is unclear exactly which heuristic time columns, if any, should remain. [chunk_015]
- The chunk does not show a complete 30-instance run, generated plot results, aggregate statistics, repeated-run variance, or a fixed random seed; final thesis conclusions cannot be drawn from the partial console excerpts. [chunk_015]
- The mapping claims for 1,255/1,263 physical files and the eight Falkenauer container files need direct verification from parser output or files before being treated as confirmed evidence. [chunk_015]
- The text encoding appears corrupted (`WÃ¤scher`), while code checks both `Waescher` and the corrupted folder spelling inconsistently; the canonical dataset/folder spelling and robust matching behavior remain uncertain. [chunk_015]
- It remains unclear whether the Hard count of 55 equals 10 capacity-based Scholl 3 instances plus 17 Waescher plus 28 Hard28 without overlap; that decomposition is implied but not demonstrated. [chunk_015]
- `RUNS_PER_INSTANCE` is unused, and the methodology does not yet explain whether stochastic GA comparisons will use multiple independent runs, fixed seeds, means, standard deviations, or confidence intervals. [chunk_015]
