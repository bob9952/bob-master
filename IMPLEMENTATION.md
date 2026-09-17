# Transcript-Derived Implementation Record

This document describes only what can be reconstructed from the 16 transcript summaries. It is not a source-code audit. No project source, benchmark file, workbook, generated artifact, or Git metadata was inspected while preparing it.

Evidence labels used below:

- **Observed**: console output or an error was pasted by the user.
- **Shown**: code appeared in the conversation, but the current file was not verified.
- **Claimed edit**: the assistant said a file was changed; no file/diff evidence was provided.
- **Proposed**: design or code was suggested but not demonstrated as saved or run.
- **Stale**: a snippet was superseded or contradicted later.

## Repository and component model

| Area | Transcript-derived role | Evidence state |
|---|---|---|
| `project/data/` | Local benchmark tree containing Falkenauer U/T aggregate files, Scholl sets, Hard28/Schoenfield, and later Waescher-family files; `Solutions.xlsx` is the reference workbook. | Physical layout is user-described and reflected in runs, not inspected here. [chunk_004] [chunk_014] |
| `project/src/parser.py` | Common `parse_instance_file` entry point intended to detect Falkenauer multi-instance files versus BPPLIB single-instance files and return normalized instance dictionaries. | **Shown/claimed edit**, with real parser failures and later successful aggregate-instance outputs. [chunk_003] [chunk_006] |
| `project/src/solution_manager.py` | Loads workbook metadata and resolves a parsed instance name to a reference value. | **Observed** message reports 6,195 loaded entries; exact LB/UB/status handling is unverified. [chunk_004] [chunk_014] |
| `project/src/heuristic.py` | Holds base constructive heuristics and later lookup, counting-sort, and priority-queue variants. | Multiple **shown/claimed** versions; no current-source audit or parity test. [chunk_005] [chunk_013] |
| `project/src/chromosome.py` | Holds a permutation, decoded bins, fitness/cost, bin count, mutation reevaluation, feasibility/output/visualization behavior. | Early modular design is **proposed/shown**; current exact contract is unverified. [chunk_001] [chunk_002] |
| `project/src/ga.py` | Initializes a population, selects parents, crosses/mutates permutations, applies elitism, records convergence history, and returns a best solution. | Behavior is reconstructed from several snippets; competing fitness/selection descriptions remain. [chunk_002] [chunk_012] |
| `project/run_experiments.py` | Discovers and categorizes instances, samples a test set, runs heuristics and GA, prints progress, exports detailed results, and generates per-instance plots. | Later console runs demonstrate an operational version, but many near-duplicate snippets make the exact current version uncertain. [chunk_013] [chunk_016] |
| `project/plot_results.py` | Reads the experiment workbook, computes per-method gaps, aggregates by category, and writes comparison charts. | **Observed** command once reported two saved plots; later expanded algorithm lists are **claimed edits**. [chunk_011] [chunk_012] |
| `project/results/` | Intended home of `experiment_results.xlsx`, `experiment_results.txt`, comparison plots, bin-layout images, and convergence plots. | Output paths were printed in runs; contents were not inspected here. [chunk_012] [chunk_016] |
| External repositories | BPPLIB, Metaheuristic-Algorithms, 1Dbin, bin-packing, bin-packing-heuristics, and binpacking-genetic-algorithm are intended as Git submodules. | A successful `git submodule add` sequence was reported, but final gitlinks/fresh-clone behavior was not verified. [chunk_012] |

## End-to-end data flow

```text
data/**/*.txt
    -> parse_instance_file
       -> one normalized instance (single-instance BPP)
       -> many normalized instances (Falkenauer aggregate file)
    -> attach source folder/file metadata
    -> determine reference value
       -> embedded best_known, else SolutionManager/Solutions.xlsx
    -> classify into Easy / Medium / Hard
    -> sample up to 10 per category
    -> run heuristic variants and time them
    -> run one GA and retain best solution/history
    -> print compact console row
    -> append detailed TXT record
    -> accumulate XLSX row
    -> save bin-layout and convergence images
    -> plot category-level gap/runtime summaries from XLSX
```

This is the latest shown flow, not a guarantee of current repository behavior. Sampling is unseeded, the declared repeat count is unused, and Excel appears to be written only after the full loop. [chunk_007] [chunk_015] [chunk_016]

## Parser and instance contract

### Formats

- Falkenauer aggregate files begin with a problem count. Each logical problem then has a name, metadata (`capacity`, item count, best-known count), and exactly that many item values. Local triplet evidence contains decimal values such as capacity `100.0`, so capacity and item weights cannot be parsed as integers unconditionally. [chunk_002] [chunk_003]
- BPPLIB BPP single-instance files are described as item count, capacity, then one item weight per line. They do not embed a best-known value, so reference metadata must come from the workbook. [chunk_002] [chunk_003]
- The broader benchmark description also contains CSP files with `(weight, demand)` pairs, but no transcript evidence demonstrates CSP support in the parser. [chunk_014]

### Normalized record

The proposed parser returns at least `name`, `capacity`, `num_items`, `best_known`, and `items_dict`, with 1-based item IDs. Later collection code adds `_folder` and `_file`. [chunk_003] [chunk_006]

### Detection and naming

- Proposed auto-detection treats a numeric first line followed by a nonnumeric second line as a Falkenauer aggregate; otherwise it treats the file as a single BPP instance. This rule was shown but not independently tested. [chunk_003]
- Proposed normalization maps embedded names such as `u120_00` to workbook-style keys such as `Falkenauer_u120_00.txt`; ordinary single-instance files retain their basename. Later runs display normalized Falkenauer names, which supports but does not fully prove this behavior. [chunk_003] [chunk_008]
- A verifier matched 1,255 of 1,263 physical `.txt` filenames. The eight unmatched names were `binpack1.txt` through `binpack8.txt`; the assistant explained that they are containers whose 160 internal instance names, rather than container filenames, appear in Excel. That explanation remains unverified against parser output/workbook rows in this task. [chunk_014] [chunk_015]

### Numeric policy

First Fit comparisons were shown with `EPSILON = 1e-6` for decimal data. It remains unresolved whether the decimal Falkenauer files are scaled versions of integer BPPLIB data and should instead be rescaled exactly. [chunk_003] [chunk_005]

## Reference-solution behavior

- The workbook reportedly has nine sheets and 6,195 rows/names: Falkenauer 160, Scholl 1,210, Waescher 17, Schwerin 200, Schoenfield Hard28 28, Randomly Generated 3,840, Augmented Non-IRUP 250, Augmented IRUP 250, and GI 240. The counts sum to 6,195 and were printed by a verifier. [chunk_014]
- `SolutionManager` is described as reading all sheets through pandas/openpyxl and resolving exact names or names with `.txt` appended. Actual runs repeatedly printed `Successfully loaded 6195 optimal solutions`. [chunk_003] [chunk_004]
- The phrase “optimal solutions” is not yet safe. The workbook contains `Best LB`, `Best UB`, and `Status`; only `LB == UB` or `Status == Solved` proves an optimum. Current behavior may flatten names and use `Best UB` without retaining proof status. [chunk_003] [chunk_014]
- The runner prefers an instance's embedded `best_known` and falls back to workbook lookup. This can mix historical best-known values with later proven optima unless provenance and status are preserved. [chunk_002] [chunk_016]
- Shown code computes `Gap_GA = ga_bins - optimal` only when the reference is truthy and otherwise stores zero. This is a correctness/reporting defect because missing data becomes indistinguishable from a proven zero gap. [chunk_007] [chunk_010] [chunk_016]

## Solution representation and constructive heuristics

Bins are consistently shown as dictionaries with `used` and `items`; items are generally `(item_id, item_size)` pairs. One visualization draft instead expects raw IDs, so the current bin-item contract must be checked before trusting visualization code. [chunk_002] [chunk_012]

### Base behavior

| Method | Shown behavior | Notes |
|---|---|---|
| FF | Scan bins in creation order; place in the first feasible bin; otherwise open a bin. | Uses epsilon in shown decimal-safe versions. [chunk_005] |
| NF | Check only the current/last bin; open a new one on failure. | Included as a baseline and is often much worse in observed runs. [chunk_005] [chunk_016] |
| BF | Scan feasible bins and choose the one with least residual space. | Tie-breaking is not formally documented. [chunk_005] |
| MR | Scan feasible bins and choose the one with greatest residual space. | Treated as Worst Fit, but fidelity to the requested PDF/C++ “Max Rest” definition was never demonstrated. [chunk_005] |

FFD, BFD, NFD, and MRD are produced by sorting item IDs by nonincreasing weight before calling the corresponding base method. This uses Python sorting in ordinary variants. [chunk_004] [chunk_012]

### Optimized or additional variants

- `max_rest_pq` (MR+/MRD+) uses `heapq` keyed by negative remaining capacity. One 30-instance run reported identical bin counts between MR and MR+, and between MRD and MRD+, but this does not prove general equivalence. [chunk_011] [chunk_012]
- `counting_sort` reconstructs integer-valued items by descending weight; FFD+ and NFD+ fall back to normal sorting when any value is non-integral. [chunk_013] [chunk_016]
- `first_fit_lookup` (FFL) stores a starting bin index by item size and resumes scanning there. Its equivalence to the cited paper's FF+ or FF++ is unverified. [chunk_013] [chunk_014]
- `best_fit_lookup` (BFL) indexes bins by integer residual capacity and searches upward. It is not established as part of the cited paper, may allocate `capacity + 1` buckets, and may truncate non-integral item values because only integral capacity is checked. [chunk_013] [chunk_014]
- The cited PDF distinguishes FF+, FF++, FFD+, FFD++, and NFD+ by specific STL/vector/map and sorting choices. Current Python labels and implementations do not yet have a proven one-to-one mapping. [chunk_011] [chunk_013]

## Genetic algorithm behavior

### Representation and decoding

The working chromosome is a permutation of item IDs. Decoding iterates through that order and applies First Fit, producing a feasible packing when the permutation itself is valid. A GA with Best Fit decoding was endorsed as a future comparison but is not shown as implemented. [chunk_001] [chunk_002] [chunk_011]

### Fitness/cost

Two incompatible definitions appear:

1. Original notebook: minimize `1 - mean((used_i / capacity)^z)`, commonly with `z = 2`. [chunk_001] [chunk_012]
2. Later modular proposal: minimize `N - mean((used_i / capacity)^2)`, making bin count primary and fullness a within-count tie-breaker. [chunk_002] [chunk_012]

The summaries do not establish which formula is in the current `ga.py`/`chromosome.py`.

### Operators

- Initialization uses random permutations. [chunk_001]
- Selection is inconsistent across snippets: one samples five with replacement and takes two best; another reportedly samples ten unique individuals, splits them into two groups of five, and chooses one from each. [chunk_001] [chunk_012]
- Crossover is a custom one-cut duplicate-removal/reinsertion procedure that preserves a permutation, but it is not clearly standard OX1 or PMX. [chunk_001] [chunk_012]
- Mutation swaps two positions with a probability shown as 0.8 in the notebook and 0.2 in later experiment construction. The modular proposal reevaluates after mutation; the notebook mutation visibly failed to recompute bins/fitness. [chunk_001] [chunk_002]
- Survival uses elitism and offspring to form the next generation. The notebook's pairwise offspring addition can overshoot an odd population size. [chunk_001]
- Later GA objects expose `history['best']` and `history['avg']` for convergence plots. [chunk_012]

### Development settings

Later runs use population 40, 50 generations, mutation probability 0.2, and one effective run per selected instance. Earlier proposals/runs used 50/100 or 100/500. The latest constants are explicitly quick-run settings, not final thesis parameters. [chunk_004] [chunk_008] [chunk_015]

## Experiment runner and output behavior

### Discovery, classification, and sampling

- The runner recursively walks all `.txt` files, parses every logical instance, and adds folder/file metadata. This superseded filtering out `binpack` and consuming only the first parsed record. [chunk_006]
- Early classification used capacity alone: Easy `<1000`, Medium `1000..99999`, Hard `>=100000`. It yielded 880 Easy, 508 Medium, and only 10 Hard. [chunk_006] [chunk_008]
- Later classification adds Waescher and Hard28 to Hard by name/folder. A partial run then reported 880 Easy, 480 Medium, and 55 Hard, consistent with but not directly proving `10 + 17 + 28`. [chunk_014] [chunk_015]
- Up to 10 instances are selected from each category with `random.sample`. No seed or persisted sample manifest is shown. Sorting each local sample after extending the combined list does not reorder `final_test_set`. [chunk_010] [chunk_016]

### Timing

`solve_heuristic` measures wall-clock time with `time.time()` around ordering plus the heuristic call. GA time covers construction and `run()`. The hardware, warm-up, timer policy, and repetition policy are absent. [chunk_005] [chunk_015] [chunk_016]

### Outputs

- The latest console design prints instance metadata, reference value, all heuristic bin counts, GA bin count, and GA time, omitting heuristic times to reduce width. Earlier snippets showing all result/time pairs are stale. [chunk_015] [chunk_016]
- Detailed TXT output is opened incrementally and flushed after each instance. [chunk_007] [chunk_009]
- XLSX rows include metadata, every method's bin count and time, GA time, and `Gap_GA`; the workbook is written after result accumulation, so interruption may lose structured partial data. [chunk_007] [chunk_016]
- Bin packing visualizations are saved per tested instance, six bins per row in a shown draft. Convergence plots show best and average fitness and are currently generated for every instance despite comments suggesting a subset. [chunk_012] [chunk_016]
- `plot_results.py` reads XLSX, computes algorithm-minus-reference gaps, groups averages by category, and writes gap/runtime bar charts. One observed invocation reported `comparison_gap.png` and `comparison_time.png`; later algorithm expansion and scale choices were not revalidated. [chunk_011] [chunk_012]

## Known shown changes and their confidence

| Change | Confidence | Notes |
|---|---|---|
| Notebook decoder changed from Next Fit to First Fit; `THESIS_PLAN.md` created. | **Claimed edit only** | No current file inspection; notebook still had visible call, print, and mutation-state defects. [chunk_001] |
| Modular `parser.py`, `chromosome.py`, `ga.py`, `heuristic.py`, `main.py`, and `comparison.py` created. | **Claimed edit**, partly supported by later runs | Early parser run failed on decimals; later experiment runs imply some modular implementation exists. [chunk_002] [chunk_003] |
| Parser generalized to aggregate and single-instance inputs with decimal support. | **Shown/claimed**, operationally plausible | Later Falkenauer logical instance names appear in run output; strict count and scaling checks remain unknown. [chunk_003] [chunk_008] |
| Script-relative path fixes applied to runners. | **Shown/claimed** | Earlier paths failed; later scripts found organized data. A pasted `comparison.py` revision still used undefined `triplet_file`. [chunk_004] |
| Eight baseline heuristics and timing wrapper added. | **Shown/claimed**, supported by output | Observed tables contain their results and timings. Fidelity to PDF/C++ semantics is not proven. [chunk_005] |
| XLSX/TXT output and category sampling added. | **Observed operational behavior** | Several runs printed category counts and output paths; artifact contents were not inspected here. [chunk_008] [chunk_016] |
| MR+/MRD+, FFL/BFL, FFD+/NFD+ added to runner/plots. | **Shown/claimed**, partially supported by later output | Later rows include these result columns, but no source audit or parity suite exists. [chunk_012] [chunk_015] |
| Hard classification expanded to Waescher and Hard28. | **Supported by observed counts**, exact code unverified | Pool changed from 10 to 55; string normalization remains fragile. [chunk_014] [chunk_015] |
| All six external projects converted/re-added as submodules. | **Observed command outcome, final state unverified** | `.gitmodules` appeared staged; gitlink entries and fresh clone were not checked. [chunk_012] |
| Console compacted to omit heuristic timings while preserving detailed files. | **Shown latest version / user-approved requirement** | Latest code listing matches the requirement; current saved file was not inspected. [chunk_016] |

## Actual observed execution state

These are transcript observations, not newly reproduced results.

1. **Early notebook state:** five saved solutions reloaded as feasible with 27, 29, 457, 23, and 13 bins, but instance definitions and baseline comparisons were absent. A later call failed because `main_loop` omitted the leading `instance_name`, producing a positional-argument `TypeError`; the print label also used bin capacity as “best bins count.” [chunk_001] [chunk_002]
2. **Initial Falkenauer parser failure:** `comparison.py` failed on metadata `100.0 60 20` because the parser used `int()` for capacity. [chunk_003]
3. **First five triplets:** after later changes, `t60_00` through `t60_04` each had reference 20; FFD returned 23, 23, 23, 23, and 24; GA returned 21 for all five. The same results appeared after stronger proposed settings. These were single runs without seeds or timing distributions. [chunk_003] [chunk_004]
4. **Single Scholl case:** a run reported 6,195 workbook entries, `N1C1W1_A.txt` with 50 items and capacity 100, and reference/FFD/GA all equal to 25. [chunk_004]
5. **Twelve-instance sampled run:** Hard28, Scholl set 1/2/3 samples showed GA worse than simple heuristics on some cases and better on several set-2/set-3 cases; GA times reached about 37 seconds while FFD stayed in milliseconds. The sample was unseeded and single-run. [chunk_005]
6. **Interrupted 30-test attempts:** multiple runs were stopped with `KeyboardInterrupt` during chromosome evaluation/First Fit, showing practical slowness rather than an algorithmic exception. [chunk_006] [chunk_007]
7. **Completed quick 30-instance run under capacity-only categories:** 880 Easy, 508 Medium, and 10 Hard were discovered, 10 selected from each; GA matched 5/10 Easy, 4/10 Medium, and 0/10 Hard in one run. [chunk_008]
8. **Later 30-instance run with MR+ variants:** GA reportedly reached the reference on 5 Easy, 6 Medium, and 0 Hard cases; mean GA gap was derived as 1.5 bins overall. MR/MR+ and MRD/MRD+ bin counts matched on all displayed cases. [chunk_012]
9. **Revised hard-pool run:** the latest reported discovery count is 1,415 logical instances: 880 Easy, 480 Medium, and 55 Hard, with 30 sampled tests. A pasted sample had GA match the listed reference on 13 instances, while at least one classical heuristic did so on 24. GA time ranged from 0.126 to 19.062 seconds. Outputs were reported written to the results XLSX/TXT paths. [chunk_016]

No observed run in the summaries provides a seeded, repeated, final-parameter experiment with variance or confidence reporting. Therefore none of the above supports a general claim that the GA outperforms the heuristic baselines. [chunk_003] [chunk_011] [chunk_016]

## Suspected bugs, contradictions, and stale snippets

### High-risk correctness/reporting issues

- Missing reference values become zero gap in shown code. They must remain missing, not imply optimality. [chunk_007] [chunk_016]
- `Solutions.xlsx` rows are called optima without demonstrated enforcement of `LB == UB` or `Status == Solved`. [chunk_014]
- The authoritative GA fitness is unknown because notebook and modular formulas differ. [chunk_012]
- Selection behavior differs across snippets, and the custom crossover lacks a formal operator identity and invariant tests. [chunk_001] [chunk_012]
- Notebook mutation changed the permutation without recomputing bins/fitness; the modular proposal fixes this, but current code is unverified. [chunk_001] [chunk_002]
- The parser's Falkenauer capacity scaling (100 decimal versus BPPLIB 1000 integer) is unexplained. [chunk_002] [chunk_003]
- CSP demand records may be misread as ordinary BPP weights or ignored because support is not shown. [chunk_014]
- `best_fit_lookup` may truncate non-integral values and has questionable memory/time behavior for capacity 100,000. [chunk_013]

### Experiment-design issues

- Sampling and the GA are unseeded; `RUNS_PER_INSTANCE` is unused; one stochastic result per instance is not enough for inference. [chunk_007] [chunk_016]
- The final parameters are development shortcuts, not tuned or justified settings. [chunk_015]
- Easy/Medium/Hard mixes capacity and family identity, so the labels do not have one consistent definition. [chunk_016]
- Wall-clock timing uses single very short measurements for heuristics, making timer noise material; the environment and hardware are not recorded. [chunk_011] [chunk_016]
- Structured Excel output may be lost on interruption because it is written after the loop, although TXT is flushed. [chunk_007]

### Implementation and presentation issues

- `selected.sort(...)` is called after `final_test_set.extend(selected)`, so it does not change final execution order. [chunk_010] [chunk_016]
- Visualization code disagrees on whether `bin['items']` contains IDs or `(id, size)` pairs. [chunk_012]
- The comment says convergence plots should be selective, while code generates one for every instance. [chunk_013] [chunk_016]
- Waescher detection mixes normalized and mojibake spellings and may be brittle. [chunk_014] [chunk_015]
- One pasted `comparison.py` uses undefined `triplet_file` rather than `triplet_file_path`. [chunk_004]
- Old `main.py` imported removed `parse_falkenauer_file`; later snippets use `parse_instance_file`. [chunk_004]
- A histogram bin-count expression in the notebook can become zero if every solution has the same bin count. [chunk_001]
- Multiple console layouts, GA settings, and runner listings are stale. The latest stated requirement is the compact console in [chunk_016], not the ultra-wide all-times layouts in [chunk_007] or the reduced “best of class” display in [chunk_013].

## Prioritized verification and implementation backlog

### P0 — establish a trustworthy baseline

1. **Verify the actual repository state** for the parser, solution manager, heuristic module, chromosome/GA modules, runner, plotter, result artifacts, and submodule gitlinks. Record which transcript snippets are stale. [chunk_003] [chunk_012] [chunk_016]
2. **Document and validate the Conda `ai` invocation**, then run focused syntax/import checks through that environment. Do not alter experiment parameters during validation. [chunk_002] [chunk_012]
3. **Make reference metadata explicit:** load `Best LB`, `Best UB`, and `Status`; distinguish optimum, best-known UB, and missing; never map missing to gap zero. [chunk_003] [chunk_014] [chunk_016]
4. **Build parser contract tests** for a decimal Falkenauer aggregate, an integer single-instance BPP file, malformed count/metadata cases, and any CSP file the project intends to include. Verify 160 internal Falkenauer names against workbook rows. [chunk_003] [chunk_014] [chunk_015]
5. **Freeze and test the GA definition:** representation, decoder, fitness, selection, crossover, mutation reevaluation, elitism, population-size invariants, feasibility, and deterministic seeded behavior. [chunk_001] [chunk_012]

### P1 — validate algorithm correctness

6. **Cross-check FF, BF, NF, and MR against hand-worked fixtures**, including tie cases, exact fits, decimal values, and stable bin order. [chunk_005] [chunk_013]
7. **Audit decreasing variants** and explain observed cases where descending order performs worse. Confirm this is legitimate behavior for the data/order rather than a sorting or parser bug. [chunk_008] [chunk_016]
8. **Compare Python variants against the cited C++ implementations** on identical fixtures. Establish which of FFL, BFL, FFD+, NFD+, MR+, and MRD+ are behaviorally equivalent and rename or remove unsupported labels. [chunk_013] [chunk_014]
9. **Test MR/MR+ and MRD/MRD+ equivalence** across randomized fixtures and compare runtime only after correctness is established. [chunk_011] [chunk_012]
10. **Resolve numeric scaling:** verify whether decimal Falkenauer T data are scaled integer instances; select documented integer normalization or a consistent tolerance policy. [chunk_002] [chunk_003]

### P2 — finalize the research method

11. **Choose the implemented GA claim:** permutation GA + FF, FF/BF decoder comparison, or Grouping GA. Describe Falkenauer GGA only as literature/future work unless it is actually implemented. [chunk_001] [chunk_011]
12. **Separate tuning from evaluation.** Select a tuning subset, parameter grid or rationale, final fixed settings, and untouched evaluation set. [chunk_003] [chunk_016]
13. **Create a reproducible experiment manifest:** fixed instance names, category rationale, random seeds, repeated GA runs, and stopping criteria. Use `RUNS_PER_INSTANCE` or remove it. [chunk_006] [chunk_016]
14. **Define statistics:** best/mean/median bin count, standard deviation, optimum-hit rate, absolute and percentage gaps, runtime summaries, and paired comparisons. [chunk_005] [chunk_011]
15. **Record the runtime environment:** hardware, OS, Python and package versions, timer, warm-up/repetition method, and whether plotting/output time is excluded. [chunk_006] [chunk_016]

### P3 — harden execution and reporting

16. **Checkpoint structured results per instance or per batch** so an interruption preserves machine-readable rows; include seed, run number, parameters, reference status, and source path in every record. [chunk_007]
17. **Make classification explicit and defensible.** If categories are benchmark strata rather than measured hardness, rename/document them accordingly and normalize dataset names robustly. [chunk_014] [chunk_016]
18. **Align console, TXT, XLSX, and plot schemas.** Keep the accepted compact console, detailed file timings, missing-value semantics, full algorithm inventory, and consistent names. [chunk_013] [chunk_016]
19. **Limit plots intentionally.** Generate bin/convergence plots for a documented representative subset or make per-instance plotting configurable. Confirm convergence values match the finalized fitness definition. [chunk_012] [chunk_016]
20. **Run the final protocol from a clean checkout with initialized submodules** and archive the manifest, raw results, summary tables, plots, and exact commit identifiers. [chunk_012] [chunk_016]

