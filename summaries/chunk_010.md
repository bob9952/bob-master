## Important thesis facts

- [Code snapshot] The experiment runner compares a genetic algorithm (GA) with eight heuristic variants: FF, FFD, BF, BFD, NF, NFD, MR, and MRD; each result includes a bin count and elapsed time. [chunk_010]
- [Code snapshot] Instances are divided by bin capacity into Easy (`capacity < 1000`), Medium (`1000 <= capacity < 100000`), and Hard (`capacity >= 100000`) categories. [chunk_010]
- [Code snapshot] The runner samples up to ten instances from each category, producing at most 30 tests per invocation. [chunk_010]
- [Code snapshot] The report records category, dataset/folder, instance name, item count, capacity, known optimum, all heuristic results and times, the GA result and time, and the GA gap. [chunk_010]

## Decisions and rationale

- [Requested presentation choice] Keep item count (`Itm`) and capacity (`Cap`) in the console output; the user had objected when these fields disappeared. [chunk_010]
- [Requested presentation choice] Left-align the `Opt` heading and displayed optimum using the `<4` format specification. [chunk_010]
- [Proposed robustness choice] Build the console separator with `"-" * len(header)` so its width follows the actual header rather than a fixed guessed value such as 235 or 240. [chunk_010]
- [Proposed robustness choice] Convert the optimum to `opt_str = str(optimal) if optimal is not None else "-"` before formatting, intended to avoid formatting failures for a missing optimum. [chunk_010]
- [Scope choice] A fixed random seed was considered for reproducibility but explicitly not added, to keep the change limited to the user's formatting and crash concerns. [chunk_010]

## Algorithms/formulas

- [Code snapshot] The heuristic wrapper optionally sorts item keys by descending item weight, invokes the selected packing function, and returns `len(bins)` together with elapsed wall-clock time. [chunk_010]
- [Code snapshot] FFD, BFD, NFD, and MRD are produced by running the corresponding base heuristic with descending item order; FF, BF, NF, and MR use the original order. [chunk_010]
- [Code snapshot] The GA is instantiated with population size 40, 50 generations, and mutation probability 0.2; its reported objective is `best_sol.num_bins`. [chunk_010]
- [Code snapshot] The GA absolute gap is calculated as `ga_res - optimal` when `optimal` is truthy, otherwise as `0`; this fallback can misleadingly represent an unknown optimum as zero gap. [chunk_010]

## Implementation details

- [Code snapshot] `project/run_experiments.py` recursively scans its script-relative `data` directory for `.txt` files, parses them with `parse_instance_file`, and annotates each parsed instance with its source folder and filename. [chunk_010]
- [Code snapshot] The known optimum is taken first from `instance['best_known']`; if that value is falsy, the code calls `SolutionManager.get_optimal(name)`, whose default source is described as `data/Solutions.xlsx`. [chunk_010]
- [Code snapshot] Results are accumulated as dictionaries, converted to a pandas DataFrame, and written to `results/experiment_results.xlsx`; a human-readable log is written to `results/experiment_results.txt`. [chunk_010]
- [Proposed/claimed edit] The shown final code replaces fixed-width console separators with a computed header length, uses `opt_str` in console and TXT rows, and left-aligns `Opt` in both headers. The chunk contains no file-edit tool result or post-change syntax/run evidence confirming that this code was actually saved. [chunk_010]
- [Code issue] `selected.sort(...)` occurs after `final_test_set.extend(selected)`, so the final combined list retains the pre-sort order; sorting the selected list at that point does not reorder the already-extended test set. [chunk_010]
- [Code issue] `RUNS_PER_INSTANCE = 1` is declared but is not used in the shown execution loop. [chunk_010]

## Experiments/results

- [User-reported partial run] One displayed row for `N4C2W1_C.txt` had 500 items, capacity 120, known optimum 213, GA result 218, GA gap 5, and GA time about 10.76 seconds; the run then printed `Traceback`, but the actual exception message and stack frames are absent. [chunk_010]
- [Stale conversational claim] The assistant recalled an earlier successful run with 30 instances and known optimum values, but no complete output or reproducible evidence is included in this chunk. [chunk_010]
- [Not verified] No experiment was run after the proposed formatting/`opt_str` changes, so the claim that the runner now completes without errors is unsupported by this chunk. [chunk_010]

## Sources/references

- [Internal code references] The discussion refers to `project/run_experiments.py`, `src/solution_manager.py`, `src/parser.py`, `src/ga.py`, `src/heuristic.py`, and `data/Solutions.xlsx`. [chunk_010]
- [No external sources] The chunk contains no papers, bibliographic citations, URLs, quotations, or page references suitable for thesis citation. [chunk_010]

## Rejected approaches

- [Rejected] Hard-coding the console separator to 235 or 240 dashes was abandoned in favor of deriving its length from the rendered header. [chunk_010]
- [Rejected] Adding a random seed was deliberately skipped because the user had asked for restrained changes, although the lack of a seed leaves sampled instances non-reproducible across runs. [chunk_010]
- [Rejected diagnosis paths] File encoding, `txtfile.write`, `ga_time`, manual edits, and a GA failure were considered but not established as causes because the full traceback was unavailable. [chunk_010]

## Unresolved questions

- [Unresolved] What was the exact traceback type, message, and failing line? Without it, the missing-optimum explanation remains a hypothesis. [chunk_010]
- [Unresolved] Was the proposed code actually written to `project/run_experiments.py`, and does it pass a syntax check and a complete experiment run? [chunk_010]
- [Unresolved] Do any sampled instances genuinely lack both `best_known` and a `SolutionManager` optimum, or was the crash caused elsewhere in the second iteration? [chunk_010]
- [Unresolved] Should an unknown optimum produce `Gap = "-"` rather than `0` to avoid presenting missing benchmark data as an exact match? [chunk_010]
- [Unresolved] Should sampling be seeded and should sorting occur before extending `final_test_set` to make experiment selection and reporting order reproducible? [chunk_010]
