## Important thesis facts

- **Fact from the user-provided PDF excerpt:** the naming scheme includes MR, MR+, FF, FF+, FF++, FFD, FFD+, FFD++, NF, NFD, NFD+, and BF. [chunk_012]
- **Fact from the excerpt:** MR+ is Max-Rest implemented with a priority queue; FF+ removes “almost full” bins using an STL vector; FF++ uses an STL map/lookup structure; FFD uses Heapsort; FFD+ combines FF+ with Counting Sort; FFD++ combines FF++ with Counting Sort; and NFD+ uses Counting Sort. [chunk_012]
- **Reported implementation status, not independently verified in this chunk:** MR, MR+, FF, FFD, NF, NFD, and BF were said to be implemented; FF+, FF++, FFD+, FFD++, and NFD+ were said to be missing. [chunk_012]
- **Reported implementation status:** additional tested variants included BFD, MRD, and MRD+, although those names were not in the supplied PDF table excerpt. [chunk_012]
- **Fact from the shown experiment driver:** instances were classified by bin capacity: Easy for capacity below 1,000; Medium for capacity from 1,000 through 99,999; and Hard for capacity at least 100,000. [chunk_012]
- **Fact from the shown code:** each result row records category, dataset, instance, item count, capacity, known optimum, bin count and runtime for each heuristic, plus the GA result, runtime, and GA gap. [chunk_012]
- **Fact from user preference:** the user does not want the agent to keep attempting Python execution until the Conda interpreter is configured for the agent. [chunk_012]

## Decisions and rationale

- **User decision:** the six external repositories should remain Git submodules linked to their original GitHub repositories, not be converted into ordinary tracked directories; the rationale is to preserve links to the upstream projects. [chunk_012]
- **Implemented/reported decision:** `plot_results.py` was expanded to include MR+ and MRD+ in gap and runtime comparisons so the optimized variants appear in generated charts. [chunk_012]
- **Implemented/reported decision:** the experiment driver compares FF/FFD, BF/BFD, NF/NFD, MR/MRD, MR+/MRD+, and GA on the same sampled instances. [chunk_012]
- **User scope preference, still tentative:** implementing the PDF’s non-`++` heuristics is acceptable, including NFD+; segment-tree/BST work for `++` variants should be deferred until later. [chunk_012]
- **Proposed decision:** retain bin-layout and convergence visualizations because the user considers them useful and visually appealing; necessity for the thesis remains undecided. [chunk_012]
- **Assistant recommendation, not a user decision:** a segment-tree-based First-Fit was suggested as a future FF++ implementation with logarithmic bin lookup. [chunk_012]

## Algorithms/formulas

- **Shown formula:** the original chromosome objective was `1 - (1/N) * sum((used_i / capacity)^z)` with `z = 2`, minimized over the population. [chunk_012]
- **Proposed replacement formula:** the later GA snippet uses the cost `N - (1/N) * sum((used_i / capacity)^2)`, so fewer bins dominate and fill quality breaks ties among solutions with the same bin count; this appeared in proposed code and was not verified against the repository. [chunk_012]
- **Shown decoding approach:** a chromosome is a permutation of item IDs and is decoded into bins with First-Fit. [chunk_012]
- **Shown mutation:** swap two randomly selected chromosome positions when a mutation-probability test succeeds, then re-evaluate the chromosome. [chunk_012]
- **Reported tournament selection logic, not independently inspected:** sample 10 unique individuals with `random.sample`, split them into two disjoint groups of five, and choose the best individual from each group; this guarantees distinct parent objects if the population has at least 10 members. [chunk_012]
- **Shown alternative selection in pasted external code:** `random.choices(population, k=5)` samples with replacement and returns the two best sampled chromosomes, so the same individual can occur more than once. [chunk_012]
- **Shown crossover:** choose one cut point, combine a left prefix from one parent with non-duplicate genes from the other parent’s right portion, then append any missing genes from the complement to preserve a full permutation. [chunk_012]
- **Shown survival selection:** combine old and new populations, retain an elite fraction ranked by fitness, then fill the remaining generation from the new population. [chunk_012]
- **Formula used in reporting:** `Gap_GA = GA_bins - optimal_bins` when an optimum is available; otherwise the shown code records zero. [chunk_012]
- **Complexity claim from the discussion, not verified from the PDF:** the current ordinary First-Fit scan is quadratic in the worst case, while a segment tree or balanced search tree could support an FF++-style lookup in logarithmic time per item; Counting Sort was proposed for integer-size decreasing variants instead of Python’s general-purpose Timsort. [chunk_012]

## Implementation details

- **Observed Git outcome:** all six external repositories were successfully cloned through `git submodule add`, and `.gitmodules` appeared staged; the captured final `git status` displayed only `.gitmodules`, so the exact staged gitlink state was not independently confirmed in the chunk. [chunk_012]
- **Shown `plot_results.py` behavior:** it reads `results/experiment_results.xlsx`, computes `Gap_<heuristic> = heuristic_bins - Optimal`, and writes category-level gap and log-scale runtime bar charts. [chunk_012]
- **Shown experiment settings:** `SAMPLES_PER_FOLDER = 10`, `POP_SIZE = 40`, `GENERATIONS = 50`, and `RUNS_PER_INSTANCE = 1`; the displayed loop does not use `RUNS_PER_INSTANCE` explicitly. [chunk_012]
- **Shown sampling behavior:** the driver walks `project/data`, parses every `.txt` file, groups parsed instances by capacity category, and uses `random.sample` to choose up to ten per category; no random seed is shown. [chunk_012]
- **Shown optimum lookup:** use an instance’s `best_known` value first, then fall back to `SolutionManager.get_optimal(name)`. [chunk_012]
- **Shown decreasing-variant implementation:** FFD, BFD, NFD, MRD, and MRD+ are obtained by sorting item IDs by descending item size before calling the corresponding base heuristic; this uses Python sorting, not the PDF-specific Heapsort or Counting Sort variants. [chunk_012]
- **Shown output:** detailed results are written to `project/results/experiment_results.xlsx` and `project/results/experiment_results.txt`. [chunk_012]
- **Shown visualization proposal/code:** `Chromosome.visualize_bins` creates stacked item bars, six bins per row, labels sufficiently large items, and saves one PNG per instance under `project/results/plots/bins`. [chunk_012]
- **Shown convergence plotting:** the driver plots `ga.history['best']` and `ga.history['avg']` and saves one convergence PNG per tested instance under `project/results/plots/convergence`. [chunk_012]
- **Potential code inconsistency:** one visualization draft assumes bin items are IDs and looks sizes up in `items_dict`, while a later draft iterates `(item_id, item_size)` pairs; the actual return contract of `first_fit` was not established in the chunk. [chunk_012]
- **Observed pasted-code defect:** `main_loop` is declared with five arguments including `instance_name`, but one call passes only four, producing `TypeError: main_loop() missing 1 required positional argument: 'num_generations'`. [chunk_012]
- **Observed pasted-code defect:** the external loop prints `best_chromosome.bin_size` under the label “best bins count”; this is the capacity, not `len(best_chromosome.bins)`. [chunk_012]

## Experiments/results

- **Actual reported run:** 6,195 optimal solutions were loaded from Excel; 880 Easy, 508 Medium, and 10 Hard instances were available, with 10 randomly selected from each category for 30 tests. [chunk_012]
- **Actual reported result:** GA reached the listed optimum on 5 of 10 Easy instances, 6 of 10 Medium instances, and 0 of 10 Hard instances. [chunk_012]
- **Derived from the reported rows:** GA’s total gap was 45 bins over 30 instances, for an overall mean gap of 1.5 bins; category mean gaps were 1.4 Easy, 0.5 Medium, and 2.6 Hard. [chunk_012]
- **Actual reported result:** on every displayed instance, MR+ used the same number of bins as MR and MRD+ used the same number as MRD. [chunk_012]
- **Actual reported timing example:** on `N3C3W4_I.txt`, MR took 0.0015 s and MR+ took 0.0002 s, approximately 7.5 times faster in that single rounded measurement. [chunk_012]
- **Actual reported result:** on `Falkenauer_u500_13.txt`, the optimum was 196 bins; FFD/BFD/MRD/MRD+ used 198, GA used 203, FF used 208, MR/MR+ used 225, and NF/NFD used 255/274. [chunk_012]
- **Actual reported Hard-set pattern:** GA used 57–60 bins with gaps of 2–3, while FF/FFD/BF/BFD/MR/MRD/MR+/MRD+ used 59–60 and NF/NFD used 63–66 on the ten listed Hard instances. [chunk_012]
- **Actual reported timing pattern:** deterministic heuristics completed in roughly 0.0000–0.0084 s in the printed table, while GA took roughly 0.11–12.43 s; these are single-run values and should not be treated as stable performance estimates. [chunk_012]
- **Actual pasted external-code result:** five loaded solutions were reported feasible, with 27, 29, 457, 23, and 13 bins for instances 1–5; their relation to the main 30-instance benchmark is not established. [chunk_012]
- **Unverified assistant interpretation:** MR+ was described as maintaining MR’s quality while being much faster; equality of bin counts is supported by this one run, but general equivalence and speedup require repeated controlled tests. [chunk_012]

## Sources/references

- **User-supplied source:** `BASIC ANALYSIS OF BIN-PACKING HEURISTICS.pdf`; only a naming-table excerpt was present, so the full set of algorithms, definitions, assumptions, and citations was not reviewed. [chunk_012]
- **External repository:** `git@github.com:mdelorme2/BPPLIB.git`. [chunk_012]
- **External repository:** `git@github.com:itsatefe/Metaheuristic-Algorithms.git`. [chunk_012]
- **External repository:** `git@github.com:richardf/1Dbin.git`. [chunk_012]
- **External repository:** `git@github.com:Pseudomanifold/bin-packing.git`. [chunk_012]
- **External repository:** `git@github.com:Pseudomanifold/bin-packing-heuristics.git`. [chunk_012]
- **External repository:** `git@github.com:neatniets/binpacking-genetic-algorithm.git`. [chunk_012]
- **Project artifacts referenced in the discussion:** `project/src/heuristic.py`, `project/src/ga.py`, `project/run_experiments.py`, `project/plot_results.py`, `project/data/Solutions.xlsx`, and the generated Excel/TXT/PNG outputs. [chunk_012]

## Rejected approaches

- **Rejected:** converting BPPLIB and Metaheuristic-Algorithms into ordinary folders tracked directly by the main repository; the user clarified that all six external projects must be submodules. [chunk_012]
- **Failed approach:** Windows `rmdir /s /q` syntax was run in Git Bash, where it was parsed as Unix `rmdir`; parallel `&` commands also contributed to an `index.lock` conflict. [chunk_012]
- **Abandoned/destructive intermediate approach:** nested `.git` directories were removed to flatten repositories, after which `git submodule add` failed because existing non-repository directories occupied the target paths; the folders were then removed and freshly cloned as submodules. [chunk_012]
- **Deferred by user:** FF++ and FFD++ implementations based on a segment tree, BST, or equivalent map structure; these may be reconsidered later. [chunk_012]
- **Rejected workflow behavior:** repeatedly trying to run Python without knowing how to invoke the user’s Conda interpreter. [chunk_012]

## Unresolved questions

- **Unresolved:** which algorithms are actually contained in the full PDF beyond the pasted naming table, and what exact pseudocode/data structures the paper specifies. [chunk_012]
- **Unresolved:** whether the immediate implementation scope is precisely FF+, FFD+, and NFD+, while leaving FF++ and FFD++ for later. [chunk_012]
- **Unresolved:** whether FF+ should reproduce the paper’s STL-vector behavior exactly or use a Python-equivalent active-bin structure, and how equivalence will be demonstrated. [chunk_012]
- **Unresolved:** whether FFD must specifically use Heapsort to match the paper’s label instead of the currently shown descending Timsort. [chunk_012]
- **Unresolved:** whether the tournament-selection and crossover implementations in the actual `ga.py` match the assistant’s description and preserve valid permutations in all edge cases. [chunk_012]
- **Unresolved:** which GA fitness definition is authoritative: the original `1 - mean(fill_ratio^2)` objective or the proposed `bin_count - mean(fill_ratio^2)` cost. [chunk_012]
- **Unresolved:** whether bin visualizations are thesis deliverables, optional illustrations, or only debugging aids. [chunk_012]
- **Unresolved:** the proper Conda interpreter/environment command for future reproducible experiment execution. [chunk_012]
- **Unresolved:** reproducibility and statistical validity need improvement through a fixed sampling seed, multiple GA runs per instance, variance/confidence reporting, and explicit use of `RUNS_PER_INSTANCE`. [chunk_012]
- **Unresolved:** verify the completed submodule configuration with `.gitmodules`, staged gitlinks, and a fresh clone/submodule-init test before treating repository setup as final. [chunk_012]
- **Unresolved:** the user asked what other improvements are worthwhile; no final prioritized improvement plan was provided in this chunk. [chunk_012]
