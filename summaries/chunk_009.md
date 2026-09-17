## Important thesis facts

- The experiment runner compares eight heuristic variants (FF, FFD, BF, BFD, NF, NFD, MR, and MRD) with a genetic algorithm (GA) on one-dimensional bin-packing instances. Each result includes the number of bins and an execution time. [chunk_009]
- Instances are classified by capacity: `Easy` for capacity below 1,000, `Medium` for capacity from 1,000 through 99,999, and `Hard` for capacity at least 100,000. [chunk_009]
- The shown sampling scheme selects up to 10 random instances from each category; the real runs reported 880 Easy, 508 Medium, and 10 Hard instances available, producing 30 selected tests. [chunk_009]
- The solution manager reported successfully loading 6,195 optimal solutions from `Solutions.xlsx`; an instance's embedded `best_known` value is used first, with the manager lookup as fallback. [chunk_009]

## Decisions and rationale

- User choice: preserve the existing table because the user already liked it and make only small formatting tweaks. [chunk_009]
- User choice: retain the `Itm` and `Cap` columns, retain the full instance name, remove unwanted extra dashed separators, and make `Opt` left-aligned rather than right-aligned. [chunk_009]
- Assistant proposal: stop truncating console instance names and place a timing column beside every algorithm result to improve readability and screenshot usefulness. [chunk_009]
- Assistant proposal: replace a whole header-and-loop block to avoid patch-context failures from earlier partial edits; this was a proposed editing tactic, not a user-approved architectural change. [chunk_009]
- Assistant correction: after acknowledging that an older print layout had accidentally removed `Itm` and `Cap`, the assistant restored them in the displayed code and reduced the proposed separator width from 300 to 235 characters. [chunk_009]

## Algorithms/formulas

- `solve_heuristic` optionally sorts item identifiers by descending item size, calls the chosen heuristic with the ordered keys, item dictionary, and bin capacity, then returns `len(bins)` and elapsed wall-clock time. [chunk_009]
- The non-decreasing variants FF, BF, NF, and MR use the original item-key order; FFD, BFD, NFD, and MRD use descending item-size order. [chunk_009]
- The GA is instantiated with population size 40, 50 generations, and mutation probability 0.2; its reported objective is `best_sol.num_bins`. [chunk_009]
- GA gap is computed as `ga_res - optimal` when an optimum is available, otherwise zero; thus a zero in the no-optimum case would not prove optimality. [chunk_009]

## Implementation details

- Code shown imports `parse_instance_file`, `GeneticAlgorithm`, four heuristic functions, `SolutionManager`, pandas, and standard modules; it walks `project/data` recursively and parses every `.txt` file. [chunk_009]
- Parsed instances are augmented with `_folder` and `_file` metadata, while result rows store category, dataset, instance, item count, capacity, optimum, every algorithm's bin count and time, and `Gap_GA`. [chunk_009]
- Code shown writes detailed text output to `results/experiment_results.txt` with flushing after every instance and writes the complete result table to `results/experiment_results.xlsx`. [chunk_009]
- The console formatter uses a helper `p(val, t)` with four decimal places for heuristic times, two decimal places for GA time, and a 30-character minimum field for the untruncated instance name. [chunk_009]
- In the latest displayed implementation, `Itm` and `Cap` were printed as `{num_items:<5}` and `{capacity:<8g}`, while `Opt` remained `{optimal:>4}`; the user's final request is therefore an unimplemented or at least unverified change to left-align `Opt`. [chunk_009]
- Although the assistant spoke as if it had updated `project/run_experiments.py`, this chunk only proves that code was shown in chat; it does not contain tool evidence confirming a file edit. [chunk_009]

## Experiments/results

- Real output from the first run loaded 6,195 optima, selected 10 instances per category, and began a 30-instance experiment. [chunk_009]
- In the first run, `N4C1W1_K.txt` had optimum 253; FF, FFD, BF, BFD, MR, and MRD returned 253, NF and NFD returned 322, and GA returned 260 in 12.24 seconds, for gap 7. [chunk_009]
- In the first run, `N3C1W2_M.txt` had optimum 136; FF, FFD, BF, BFD, MR, MRD, and GA returned 136, NF and NFD returned 161, and GA took 2.94 seconds, for gap 0. [chunk_009]
- In the first run, `Falkenauer_u120_18.txt` had optimum 49; FF returned 52, FFD 50, BF 51, BFD 50, NF 64, NFD 66, MR 54, MRD 50, and GA 51 in 0.88 seconds, for gap 2. [chunk_009]
- Real output from the second run showed the restored `Itm` and `Cap` columns. For `N4C2W1_C.txt`, 500 items and capacity 120 had optimum 213; FF, FFD, BF, and BFD returned 213, NF and NFD 290, MR and MRD 214, and GA 218 in 10.76 seconds, for gap 5. [chunk_009]
- Both pasted executions ended with `Traceback (most recent call last):` before the actual exception text, so neither run is demonstrated to have completed or produced final Excel/TXT artifacts. [chunk_009]

## Sources/references

- `project/data/Solutions.xlsx` is the stated source of known optimal solutions, accessed through `SolutionManager`; no bibliographic source or dataset publication is identified in this chunk. [chunk_009]
- Instance examples shown in output include `N4C1W1_K.txt`, `N3C1W2_M.txt`, `Falkenauer_u120_18.txt`, and `N4C2W1_C.txt`. [chunk_009]
- The intended generated artifacts are `project/results/experiment_results.xlsx` and `project/results/experiment_results.txt`, followed by graphs from `project/plot_results.py`; successful generation was not shown. [chunk_009]

## Rejected approaches

- The user rejected the assistant's 300-character-wide output with extra dashed separator lines as an unwanted visual regression. [chunk_009]
- The user rejected the accidental removal of `Itm` and `Cap` and objected to changes beyond the requested small polish. [chunk_009]
- The user rejected right alignment for `Opt` in the latest output and explicitly requested left alignment. [chunk_009]
- Truncating console instance names with ellipses was rejected in favor of displaying the full name; however, the shown TXT writer still truncates names with `name[:23]`, and the user did not explicitly address that separate file format in this chunk. [chunk_009]

## Unresolved questions

- The actual exception causing each traceback is unknown because the traceback body was not pasted; the assistant's claim that the reset logic should work was therefore unverified. [chunk_009]
- It is unresolved whether the user's complaint about "number of bins" refers only to restoring per-algorithm bin-count columns, to a separate total-bin field, or to another missing label. [chunk_009]
- The exact desired separator behavior remains slightly ambiguous: the user objected to "extra" dashed lines, but did not specify whether all separators or only redundant ones should be removed. [chunk_009]
- The final requested `Opt` left alignment still needs a minimal formatting change and a rerun, but no successful corrected output appears in this chunk. [chunk_009]
- Random sampling is not seeded in the shown code, so repeated runs select different Easy and Medium instances; the implications for reproducibility were not discussed. [chunk_009]
