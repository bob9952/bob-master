## Important thesis facts

- The experiment compares eight constructive heuristic variants—FF, FFD, BF, BFD, NF, NFD, MR, and MRD—with a genetic algorithm (GA), using the known optimum as the common quality reference. [chunk_008]
- Instance difficulty is classified solely by bin capacity in this script: Easy for capacity below 1,000, Medium for capacity from 1,000 through 99,999, and Hard for capacity at least 100,000; this is an implementation-defined grouping rather than a validated theoretical difficulty measure. [chunk_008]
- The current experiment sample is random and unseeded: up to ten instances are selected independently from each capacity category, so repeated runs can use different Easy and Medium instances; all ten available Hard instances are selected. [chunk_008]
- The recorded instance descriptors are dataset/folder, instance name, item count, capacity, and known optimum; the recorded algorithm measures are bin count and elapsed time for every heuristic and GA, plus the GA gap. [chunk_008]
- The code constants shown for the quick runs are `SAMPLES_PER_FOLDER = 10`, `POP_SIZE = 40`, `GENERATIONS = 50`, and `RUNS_PER_INSTANCE = 1`, although `RUNS_PER_INSTANCE` is not actually used in the displayed execution loop. [chunk_008]

## Decisions and rationale

- Decision: report each algorithm's result and runtime in separate, compact console columns such as `FF` and `tFF`, rather than embedding time in parentheses, so result quality and execution time can be compared directly. [chunk_008]
- Decision: add `Itm` and `Cap` to the console table, rename the ambiguous final `Gap` heading to `GapGA`, and format heuristic times with six fixed decimal places to avoid scientific notation such as `4.00543E-05`. [chunk_008]
- Decision: widen the console layout for a 2K monitor and retain a single wide table covering all heuristics and GA. [chunk_008]
- Proposal, not confirmed as implemented in this chunk: increase the final-thesis GA settings beyond the quick-run values, with `POP_SIZE=100` and `GENERATIONS=500` offered only as examples; these settings require an explicit experimental-design decision and rerun. [chunk_008]
- User-approved direction at the end: the overall output was considered good, with only full instance names and right-aligned capacity still requested. [chunk_008]

## Algorithms/formulas

- `solve_heuristic` optionally sorts item keys by descending item size, runs the supplied packing function, and returns `(number_of_bins, elapsed_seconds)`; FF, BF, NF, and MR use original key order, while FFD, BFD, NFD, and MRD use descending order. [chunk_008]
- GA is instantiated as `GeneticAlgorithm(items, capacity, pop_size=40, generations=50, mutation_prob=0.2)` in the shown quick-run code, and its solution quality is `best_sol.num_bins`. [chunk_008]
- The implemented gap formula is `Gap_GA = GA_bins - optimal_bins` when an optimum is available; otherwise it is forced to zero, which can conflate “unknown optimum” with an exact GA result. [chunk_008]
- Known optimum is taken first from the parsed instance's `best_known` value and otherwise looked up through `SolutionManager.get_optimal(name)`. [chunk_008]

## Implementation details

- Code shown for `project/run_experiments.py` recursively scans `data` for `.txt` files, parses every file with `parse_instance_file`, attaches source folder/file metadata, samples instances by capacity category, runs all algorithms, and writes results under `results`. [chunk_008]
- The results dictionary uses paired fields such as `FF`/`FF_Time` through `MRD`/`MRD_Time`, plus `GA`, `GA_Time`, and `Gap_GA`; pandas writes the accumulated rows to `experiment_results.xlsx`. [chunk_008]
- A readable text report is also written to `experiment_results.txt` and flushed after each instance, but its three-line format remains narrower and still labels the final gap generically as `Gap`; the displayed changes primarily target console output. [chunk_008]
- The latest shown console formatter uses `:.6f` for heuristic times and `:.2f` for GA time, so GA timing has lower displayed precision than heuristic timing. [chunk_008]
- The latest shown name formatter truncates names longer than 20 characters to the first 18 characters plus `..`, producing values such as `Falkenauer_t249_13..`; removing this truncation was requested but no implementation is shown after that request. [chunk_008]
- The latest shown capacity formatter is left-aligned (`{capacity:<6g}`); right alignment was requested at the end but is not shown as implemented. [chunk_008]
- The separator is hard-coded as 260 hyphens rather than derived from the actual formatted header width, and earlier iterations used 300 hyphens; the user considered the separator excessive. [chunk_008]

## Experiments/results

- Observed final displayed run: 6,195 optimal solutions were loaded; the parser found 880 Easy, 508 Medium, and 10 Hard instances, sampled 10 from each category, and ran 30 tests. [chunk_008]
- Observed final displayed run: GA gaps for the ten Easy cases were `0, 0, 0, 5, 0, 4, 1, 1, 0, 0`; for Medium they were `2, 1, 1, 0, 2, 2, 1, 0, 0, 0`; for Hard they were `3, 2, 2, 2, 4, 3, 3, 3, 2, 2`. [chunk_008]
- Observed final displayed run: on `Falkenauer_t249_13...` with 249 items, capacity 100, and optimum 83, FF, BF, NF, and MR reached 83, descending variants returned 96/96/100/96, and GA returned 88 in 2.59 seconds (`GapGA=5`). [chunk_008]
- Observed final displayed run: on `Falkenauer_u250_00...` with optimum 99, FFD returned 100, MRD 101, GA 103 (`GapGA=4`), FF 104, BF 105, MR 115, NF 131, and NFD 137. [chunk_008]
- Observed final displayed run: GA matched the optimum on 5 of 10 Easy instances and 4 of 10 Medium instances, but on none of the 10 Hard instances in that random quick run. [chunk_008]
- Observed final displayed run: heuristic timings were generally tens of microseconds to a few milliseconds, while GA timings ranged from about 0.11 to 5.76 seconds; this timing comparison is based on one run per sampled instance and is not statistically robust. [chunk_008]
- Observed earlier run: execution was manually interrupted during GA crossover/evaluation with `KeyboardInterrupt` after several Easy cases; this is not evidence of a code failure and occurred before the later completed runs. [chunk_008]
- Stale/unverified claim from the assistant: the run finished quickly because population size and generation count had been reduced; this is plausible from the shown constants but was not established by a controlled before/after timing comparison. [chunk_008]

## Sources/references

- The chunk contains no external literature citations, bibliographic records, URLs, or source quotations suitable for thesis citation. [chunk_008]
- Internal evidence consists of the displayed `run_experiments.py` code, console outputs from several executions, optimal values loaded from `data/Solutions.xlsx` through `SolutionManager`, and parsed benchmark instance metadata. [chunk_008]
- Benchmark-style names include Falkenauer instances and `HARD0.txt` through `HARD9.txt`, but the chunk does not document their publication source, provenance, or license. [chunk_008]

## Rejected approaches

- Rejected: formatting each result and time together as text such as `FF(Time)` or `FF:32(0.0002)` in the main comparison table; separate result/time columns were preferred. [chunk_008]
- Rejected by the user: truncating long instance names with trailing dots; the final request is to display names such as `Falkenauer_t249_13...` without added ellipsis. [chunk_008]
- Rejected by the user: excessively long separator rows and cramped column widths; the user preferred using the available 2K monitor width for wider readable columns without surplus dashes. [chunk_008]
- Proposed but deferred by the assistant: adding a gap column for every heuristic, because it would add nine columns and make the table substantially wider; only `GapGA` remained in the shown implementation. [chunk_008]

## Unresolved questions

- Should the final thesis experiment use a fixed random seed or a fixed published instance list so results are reproducible across runs? [chunk_008]
- What population size, generation count, mutation probability, and number of independent GA runs will be used for the final experiment, and how will stochastic variation be summarized? [chunk_008]
- Should quality gaps be stored for every heuristic, as the user suggested, or calculated later from each algorithm's bin count and `Optimal` in the spreadsheet/analysis code? [chunk_008]
- Should gaps be reported as absolute differences, relative percentages, or both, and how should missing optimum values be represented instead of silently assigning a zero gap? [chunk_008]
- Was the final request to remove instance-name truncation and right-align `Cap` subsequently implemented? No evidence of that change appears in this chunk. [chunk_008]
- Does “number of bins” in the user's formatting request mean the known optimum/result columns already shown, or was an additional field intended? The assistant interpreted the request as adding item count (`Itm`) and capacity (`Cap`). [chunk_008]
- Why do descending variants perform markedly worse than their unsorted counterparts on some Falkenauer instances, despite typically expected behavior for FFD/BFD? The chunk reports the outputs but does not validate parser order, heuristic semantics, or correctness. [chunk_008]
- Are capacity thresholds a suitable proxy for Easy/Medium/Hard difficulty in the thesis methodology, or should categories be based on benchmark family, item count, optimum, or empirically measured hardness? [chunk_008]
