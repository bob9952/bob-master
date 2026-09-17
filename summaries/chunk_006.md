## Important thesis facts

- The thesis work compares one-dimensional bin-packing solutions from eight constructive heuristic variants—FF, FFD, BF, BFD, NF, NFD, MR, and MRD—against a genetic algorithm (GA), using known or best-known bin counts as the quality baseline. [chunk_006]
- The Falkenauer benchmark comprises eight aggregate files: `binpack1`–`binpack4` contain uniform instances with item sizes in `(20,100)` and bin capacity 150, while `binpack5`–`binpack8` contain triplet instances with item sizes in `(25,50)` and bin capacity 100. [chunk_006]
- Each Falkenauer aggregate file starts with the number of problems and then stores, for each problem, an identifier, capacity, item count, best-known bin count, and the item sizes; therefore one file can represent many instances rather than one instance. [chunk_006]
- For Falkenauer uniform instances, the recorded best-known count is stated to be a proven optimum except for `u120_08`, `u120_19`, `u250_07`, `u250_12`, and `u250_13`; triplet instances were constructed with a guaranteed optimum of `n/3` bins. [chunk_006]
- The pasted Munien et al. experiment used three capacity-based datasets—easy at capacity 100, medium at 1000, and hard at 100000—with ten selected instances per dataset and ten runs per metaheuristic/underlying-heuristic combination. [chunk_006]
- The Munien excerpt reports that GA is easy to understand and implement and converges quickly, but may require more computation, converge prematurely, and depend strongly on its initial population; these are source claims, not results established by the local implementation. [chunk_006]

## Decisions and rationale

- User decision: include Falkenauer T and U instances in the experiment pool and ensure their multi-instance file format is handled. [chunk_006]
- User decision: organize reporting around Easy, Medium, and Hard sets because this structure is clearer and resembles the cited Munien study; the user also considered a smarter difficulty-uniform sample, but did not settle its exact selection logic. [chunk_006]
- User decision: show execution time for every heuristic in the console, fix poor alignment, and then run the full experiment. [chunk_006]
- User decision: store experiment outputs under the already-created `project/results/` folder, use XLSX instead of CSV for easier inspection, and prefer a TXT report over Markdown. [chunk_006]
- Assistant proposal: scan every `.txt` file, parse all returned instances, attach source-folder/file metadata, and sample after parsing so aggregate Falkenauer files are represented correctly. [chunk_006]
- Assistant proposal: use capacity thresholds (`<1000`, `1000`–`<100000`, and `>=100000`) to assign Easy, Medium, and Hard, then randomly select ten instances per category; the rationale was clearer thesis comparison, but the thresholds only approximate the paper and were not validated as a true difficulty measure. [chunk_006]
- Assistant proposal: replace the wide console row with a multi-line per-instance display so bin counts and timings for all methods remain readable. [chunk_006]
- Assistant proposal: aggregate average optimality gap and average execution time by category and create two PNG bar charts, with the time chart on a logarithmic scale. [chunk_006]

## Algorithms/formulas

- The heuristic wrapper optionally sorts item keys by descending item size, invokes a packing function, and returns `len(bins)` plus elapsed wall-clock time; this yields paired variants such as FF/FFD, BF/BFD, NF/NFD, and MR/MRD. [chunk_006]
- The proposed GA configuration is population size 50, 100 generations, mutation probability 0.2, and one run per instance; GA output is `best_sol.num_bins`. [chunk_006]
- The proposed quality measure is the absolute bin-count gap `Gap_GA = GA_bins - Optimal`; the plotting proposal generalizes this to `Gap_h = h_bins - Optimal` for every heuristic `h`. [chunk_006]
- The proposed category rule is `Hard` when capacity is at least 100000, `Medium` when capacity is at least 1000 but below 100000, and `Easy` otherwise. [chunk_006]
- Falkenauer triplet instances have a known optimum of `n/3` bins, corresponding to exactly three items per bin by construction. [chunk_006]

## Implementation details

- Earlier code explicitly excluded filenames containing `binpack`, which prevented Falkenauer files from being loaded; it also selected only `instances[0]`, incorrectly assuming one instance per file. [chunk_006]
- The assistant-proposed collection code changes the filter to all `.txt` files, calls `parse_instance_file` once per file, iterates over every returned instance, and adds `_folder` and `_file` metadata before sampling. [chunk_006]
- The transcript states that `parser.py` detects the Falkenauer multi-instance form and that `parse_falkenauer_multi` handles it, but no parser source or direct parser test is shown here, so that compatibility remains an assistant assertion. [chunk_006]
- The proposed experiment outputs include category, dataset, instance, item count, capacity, optimum, bin count and time for all eight heuristic variants, GA bin count/time, and GA gap. [chunk_006]
- The proposed multi-line console block truncates names longer than 25 characters and prints GA/optimum on one line followed by four paired heuristic count/time lines. [chunk_006]
- The plotting code is only an assistant proposal: it reads `experiment_results.csv`, computes per-method gaps, groups means by category, and writes `plots/comparison_gap.png` and `plots/comparison_time.png`. [chunk_006]
- The final requested storage change was specified as `project/results/experiment_results.xlsx` plus `project/results/experiment_results.txt`, with directory creation if needed; the chunk ends before code implementing this change is shown. [chunk_006]
- The user's environment output confirms pandas 2.3.2, openpyxl 3.1.5, and matplotlib 3.10.6 were installed in the Conda `ai` environment at that time; this is real command output but may be stale. [chunk_006]

## Experiments/results

- Real output from an interrupted run reported 6,195 optimal solutions loaded, 880 Easy candidates with 10 selected, 508 Medium candidates with 10 selected, 10 Hard candidates with all 10 selected, and 30 planned tests. [chunk_006]
- Six Easy instances completed before interruption: `Falkenauer_t60_08.txt` had optimum 20 and GA 21 (gap 1, GA 0.59 s); `N4C1W4_I.txt` had 359 and 361 (gap 2, 45.56 s); `Falkenauer_t249_01.txt` had 83 and 88 (gap 5, 6.49 s). [chunk_006]
- The remaining completed lines were `N4C2W2_P.txt` at optimum 266 and GA 271 (gap 5, 32.88 s), `N4C2W1_H.txt` at 215 and 218 (gap 3, 26.81 s), and `N4C3W4_B.txt` at 215 and 225 (gap 10, 28.99 s). [chunk_006]
- In those six rows, reported FFD time ranged from 0.0001 s to 0.0086 s while GA time ranged from 0.59 s to 45.56 s, supporting only the limited observation that GA was much slower on this partial sample. [chunk_006]
- The run ended with a user-issued `KeyboardInterrupt` while GA population initialization evaluated chromosomes through `first_fit`; this is not evidence of an algorithmic failure, only that the user stopped a long-running computation. [chunk_006]
- No complete 30-instance result set, repeated-run statistics, XLSX output, TXT output, or generated chart is present in this chunk. [chunk_006]

## Sources/references

- User-provided benchmark documentation cites E. Falkenauer (1994), “A Hybrid Grouping Genetic Algorithm for Bin Packing,” Working Paper CRIF Industrial Management and Automation, as the source of the eight Falkenauer data files and their format. [chunk_006]
- The user pasted excerpts from C. Munien et al., “Metaheuristic Approaches for One-Dimensional Bin Packing Problem: A Comparative Performance Study,” Volume 8 (2020), including dataset design, experimental setup, GA advantages/disadvantages, and comparative observations. [chunk_006]
- The pasted Munien setup reports Java/Eclipse execution on a 3.75 GHz AMD Ryzen 7 with 16 GB 2666 MHz memory and more than 1,210 benchmark instances across three categories; this describes the paper, not the local Python experiment. [chunk_006]
- The user specifically directed attention to the Munien PDF from page 10, section “F. GENETIC ALGORITHM,” but the chunk does not contain a fresh full-PDF review or verified page-level citation. [chunk_006]
- The assistant says optimal values are loaded through `SolutionManager` from `data/Solutions.xlsx`; the real run confirms 6,195 entries loaded, but the provenance and correctness of each entry are not independently checked here. [chunk_006]

## Rejected approaches

- The original filename filter that excluded `binpack*.txt` was rejected because it omitted all Falkenauer aggregate files. [chunk_006]
- The one-file/one-instance assumption and use of only `instances[0]` were rejected because Falkenauer files contain multiple problems. [chunk_006]
- Sampling files before parsing was replaced in the assistant proposal by sampling individual parsed instances, preventing an aggregate file from being treated as a single problem. [chunk_006]
- Pure folder-based random sampling was displaced by a balanced Easy/Medium/Hard sample because the user preferred category-level comparison. [chunk_006]
- A single very wide console table showing only FFD and GA times was rejected by the user as poorly aligned and incomplete; the proposed replacement is a multi-line record with all timings. [chunk_006]
- CSV and Markdown were rejected by the user as primary output formats in favor of XLSX and TXT under `project/results/`. [chunk_006]
- The assistant mentioned reducing population size or generation count as an optional speed measure, but the user did not authorize changing the GA parameters in this chunk. [chunk_006]

## Unresolved questions

- The final experiment-selection design remains unsettled: a capacity-threshold split was proposed, but the user also asked whether all instances should be sampled uniformly according to actual difficulty; no validated difficulty metric or stratification rule was chosen. [chunk_006]
- The assistant's narrative classification is internally inconsistent: it once labels Falkenauer T as Medium, while the supplied benchmark documentation gives T capacity 100 and the implemented threshold and real output classify T as Easy. [chunk_006]
- The assistant also describes Easy as including capacities 100, 120, and 150 and links it to the paper, although the pasted Munien description defines its easy dataset at capacity 100; whether this adaptation is academically acceptable needs explicit justification. [chunk_006]
- Random sampling has no stated seed, so the selected benchmark subset is not reproducible as proposed. [chunk_006]
- `RUNS_PER_INSTANCE = 1` is declared but not used to repeat GA runs, whereas the cited Munien study ran each dataset ten times per configuration; the number of repetitions required for the thesis remains unresolved. [chunk_006]
- It is unclear how to treat the five Falkenauer uniform cases whose recorded values are best known but not stated as proven optima when calculating and labeling “optimality gap.” [chunk_006]
- The proposed XLSX/TXT writer, result-folder paths, plot reader migration from CSV to XLSX, and incremental checkpoint strategy were not implemented or demonstrated in this chunk. [chunk_006]
- The expected runtime estimate of 10–20 minutes was an assistant guess contradicted by a partial run already taking tens of seconds for individual GA cases; total runtime remains uncertain and hardware-dependent. [chunk_006]
