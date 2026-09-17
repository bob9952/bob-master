## Important thesis facts

- The user is studying one-dimensional bin packing and wants a benchmark structure that can later be refined into a strong thesis experiment suite. [chunk_004]
- The user reorganized the benchmark data into three top-level collections: `Falkenauer`, `Schoenfield`, and `Scholl`; `Falkenauer` is split into `U` and `T`, `Scholl` into `set_1`, `set_2`, and `set_3`, and Schoenfield contains a `Hard28` folder whose provenance and format the user said they did not yet understand. [chunk_004]
- Falkenauer contains eight aggregate data files: `binpack1`-`binpack4` are uniform instances with item sizes uniformly distributed in `(20,100)` and bin capacity 150, while `binpack5`-`binpack8` are triplet instances with item sizes from `(25,50)` and bin capacity 100. [chunk_004]
- Falkenauer files encode the number of problems, then for every problem its identifier, capacity, item count, best-known bin count, and the item sizes. [chunk_004]
- For Falkenauer uniform instances, the recorded value is generally a proven optimum except for `u120_08`, `u120_19`, `u250_07`, `u250_12`, and `u250_13`; for triplet instances, the constructed optimum is `n/3`, with exactly three items per bin. [chunk_004]
- The supplied Scholl-related literature excerpt describes three categories with more than 1,210 instances: Dataset 1/easy with capacity 100, Dataset 2/medium with capacity 1,000, and Dataset 3/hard with capacity 100,000; the user likewise described `set_1`, `set_2`, and `set_3` as easy, medium, and hard. [chunk_004]
- The Munien study excerpt compares FA, FAH, ACSA, CSGA, ABC, and GA, each with best-fit and better-fit underlying heuristics, using 30 selected instances and 10 runs per metaheuristic/heuristic combination. [chunk_004]
- The user explicitly liked the detailed LP/IP solution-output format shown for `N1C1W1_A.txt`, including initial and last LP solutions, objective/pattern rows, timing, and the best integer solution. [chunk_004]

## Decisions and rationale

- User decision: retain the physical dataset organization `data/Falkenauer/U`, `data/Falkenauer/T`, `data/Scholl/set_1`, `data/Scholl/set_2`, `data/Scholl/set_3`, plus the Schoenfield/Hard28 collection, and make scripts conform to it. [chunk_004]
- User correction: optimal values must come from `Solutions.xlsx`, with sheets corresponding to the dataset folders, rather than the obsolete `solutions.csv` path. [chunk_004]
- User correction: scripts are commonly launched from inside the project folder, so hard-coded paths beginning with `project/` are wrong in that execution context. [chunk_004]
- Assistant proposal: derive `script_dir` from `os.path.abspath(__file__)` and build data/output paths relative to the script, making execution independent of the current working directory. [chunk_004]
- Assistant proposal: use one universal `parse_instance_file` entry point throughout, replacing the obsolete `parse_falkenauer_file` import that caused an observed `ImportError`. [chunk_004]
- Assistant proposal: compare FFD and the GA on representative samples, capture bin count and runtime, calculate gaps against known optima, and export CSV suitable for later tables and charts. [chunk_004]
- Assistant proposal: sample three files per discovered leaf folder initially to avoid running thousands of instances, while leaving the sample count and repeated-run count configurable. [chunk_004]
- Assistant proposal, not validated in this chunk: treat the experiment CSV as the basis for the thesis results chapter and later visualize `Gap_FFD` versus `Gap_GA`; the stronger claim that this alone is scientifically valid or completes the experimental work is not supported by the evidence shown. [chunk_004]

## Algorithms/formulas

- FFD is implemented by sorting item identifiers in descending order of item size, passing that order to `first_fit`, and returning the number of resulting bins. [chunk_004]
- The GA is instantiated in the single-instance and triplet-comparison examples with population size 100, 500 generations, and mutation probability 0.2. [chunk_004]
- The proposed batch experiment uses population size 50, 100 generations, mutation probability 0.2, and declares `RUNS_PER_INSTANCE = 1`; the shown loop does not actually use `RUNS_PER_INSTANCE`. [chunk_004]
- Absolute solution gaps are computed as `algorithm_bins - optimal`; when an optimum is unavailable, the batch proposal records `N/A`. [chunk_004]
- For Falkenauer triplet instances, the known optimum formula is `n/3`. [chunk_004]
- The displayed exact-solver record for `N1C1W1_A.txt` reports LP value 24.75, lower bound 25, and best integer solution 25, with both LP and IP times shown as zero in that record. [chunk_004]

## Implementation details

- Shown `run_scholl.py` flow: parse one instance, read its name/capacity/items, initialize `SolutionManager()`, prefer the instance's embedded `best_known` value and otherwise call `get_optimal(name)`, run FFD and GA, and print the gap. [chunk_004]
- The corrected `run_scholl.py` path logic derives `data_dir` from the script directory and checks `data/Scholl/set_1/N1C1W1_A.txt`, with a fallback to `data/N1C1W1_A.txt`. [chunk_004]
- Shown `comparison.py` targets `data/Falkenauer/T/binpack5.txt`, parses the aggregate file, and runs FFD and GA on its first five triplet instances. [chunk_004]
- The comparison table needs a 25-character `Instance` field in both header and data rows and a 75-character separator to keep long names aligned. [chunk_004]
- The final shown `comparison.py` revision uses script-relative paths and a flat-data fallback, but its title still refers to undefined variable `triplet_file` instead of `triplet_file_path`; therefore that exact pasted revision is internally inconsistent and was not shown running. [chunk_004]
- Shown `run_experiments.py` recursively walks `data`, selects `.txt` files except names containing `binpack`, samples up to three files per directory, parses only the first returned instance from each file, runs FFD and GA, flushes after every CSV row, and writes `Dataset`, `Instance`, `Items`, `Capacity`, `Optimal`, bin counts, runtimes, and gaps. [chunk_004]
- Excluding filenames containing `binpack` avoids duplicate aggregate Falkenauer inputs only if individual Falkenauer instance files exist; the chunk does not confirm that this assumption holds in the current tree. [chunk_004]
- The batch script labels a dataset with only the immediate parent directory name, which may lose the distinction between higher-level collections if leaf folder names overlap. [chunk_004]
- An earlier `main.py` example called removed function `parse_falkenauer_file`; a later shown version switches to `parse_instance_file` and targets `Falkenauer/U/binpack1.txt` with script-relative pathing. [chunk_004]
- Assistant statements that files were created or updated are conversation claims only; this chunk provides pasted code and observed console output but no repository diff or syntax/test evidence confirming every claimed edit. [chunk_004]

## Experiments/results

- Observed user run of `run_scholl.py`: `SolutionManager` loaded 6,195 optimal solutions from Excel; `N1C1W1_A.txt` had capacity 100.0 and 50 items; the known optimum, FFD result, and GA result were all 25, so the reported GA gap was 0. [chunk_004]
- Observed user run of `comparison.py` on the first five instances in `Falkenauer/T/binpack5.txt`: every instance had optimum 20; FFD returned 23 for `t60_00` through `t60_03` and 24 for `t60_04`; GA returned 21 for all five, giving GA gap 1 each time. [chunk_004]
- Those five triplet results show the tested GA outperforming FFD by two bins on four instances and three bins on one, but they are single displayed outcomes without repeated-run statistics, seeds, runtimes, or variability, so broader performance claims remain unsupported. [chunk_004]
- Munien Dataset 1 excerpt: better fit reached the optimum for every tested algorithm; with best fit, FAH and GA were one bin above optimum; ABC was generally fastest, and the time differences for smaller cases were negligible. [chunk_004]
- Munien Dataset 2 excerpt: better fit reached optimum across the metaheuristics except on one 500-item instance; the gap between best fit and better fit increased with complexity, and ACSA, CSGA, and GA were reported substantially slower than FA, FAH, and ABC under better fit. [chunk_004]
- Munien Dataset 3 excerpt: best fit struggled on the high-capacity hard instances; GA alone reached optimum in one highlighted case, while better fit found optimal solutions with the other heuristics in the remaining discussed cases; ACSA, CSGA, and GA slightly outperformed others for `HARD5`. [chunk_004]
- No completed `run_experiments.py` execution or generated `experiment_results.csv` is shown in the chunk. [chunk_004]

## Sources/references

- E. Falkenauer, 1994, “A Hybrid Grouping Genetic Algorithm for Bin Packing,” CRIF working paper; cited by the supplied benchmark documentation as the source of the eight Falkenauer data files and their known/best-known solutions. [chunk_004]
- Andre van Vliet is credited in the benchmark documentation with first suggesting the known-optimum triplet-instance idea, while the generation procedure is attributed to Falkenauer. [chunk_004]
- C. Munien et al., “Metaheuristic Approaches for One-Dimensional Bin Packing Problem: A Comparative Performance Study,” Volume 8, 2020; the user explicitly asked that `munien2020.pdf` be read for examples of using Scholl instances. [chunk_004]
- The Munien excerpt refers to dataset source `[62]`, but the bibliographic entry for `[62]` is not included in this chunk. [chunk_004]
- `Solutions.xlsx` is treated as the local source of 6,195 known optimal solutions, but its sheet names, provenance, and lookup-normalization rules are not shown here. [chunk_004]

## Rejected approaches

- Rejected after observed failure: importing `parse_falkenauer_file` from `src.parser`, because that function was no longer available after the parser was generalized. [chunk_004]
- Rejected after user correction: using `solutions.csv`; the required source is `Solutions.xlsx` with dataset-corresponding sheets. [chunk_004]
- Rejected after observed failures: looking for Scholl instances directly under `project/data` or using `project/data/...` when the script is already run from the project directory. [chunk_004]
- Rejected after observed failure: looking for `binpack5.txt` at `data/binpack5.txt`; its organized location is `data/Falkenauer/T/binpack5.txt`. [chunk_004]
- Rejected as insufficient formatting: widening only the comparison data row to 25 characters while leaving the header at 15; header and rows must use the same width. [chunk_004]
- The assistant chose sampled execution rather than immediately running every available instance because the full collection was described as large and potentially time-consuming; this was an assistant proposal, not a confirmed user decision. [chunk_004]

## Unresolved questions

- What exactly is the Schoenfield `Hard28` format, provenance, known-optimum source, and parser behavior? The user explicitly said they did not know much about it, and the chunk contains no resolution. [chunk_004]
- Does `SolutionManager` actually choose or reconcile workbook sheets according to `Scholl/set_1`, `set_2`, `set_3`, Falkenauer, and Hard28, or does it flatten all 6,195 names into one lookup? [chunk_004]
- Are Falkenauer instances stored only in aggregate `binpack1`-`binpack8` files or also as individual `.txt` files? The batch script skips aggregate filenames and could therefore omit Falkenauer entirely. [chunk_004]
- How should reproducible random sampling be achieved? No random seed or persisted sample manifest is shown. [chunk_004]
- How many independent GA runs per instance are required for thesis-quality reporting, and which statistics should be reported? The literature uses 10 runs, while the proposed script declares only one and does not implement a repeated-run loop. [chunk_004]
- Should the experiment runner use all instances, a fixed representative subset, or random samples per leaf folder, and how should that sampling be justified academically? [chunk_004]
- Should result reporting include best, mean, standard deviation, success rate, relative gap, utilization/waste, and convergence history in addition to one bin count and wall-clock time? [chunk_004]
- Were `run_experiments.py`, `comparison.py`, and `main.py` actually updated and validated after the final path changes? The chunk ends with assistant claims but no subsequent user run, and the last shown comparison revision contains an undefined name. [chunk_004]
- The Munien excerpt inconsistently names one Dataset 1 example as `N2C1W2_N` in one place and `N2C1W1_N` in a figure caption; the correct instance identifier needs verification from the PDF. [chunk_004]
- The assistant stated that Scholl and Hard28 together contain all three Munien difficulty categories, but the chunk does not demonstrate that mapping; it should be verified against the actual files and source literature. [chunk_004]
