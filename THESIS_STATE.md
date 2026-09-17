# Thesis State Ledger

## Evidence convention

This ledger is transcript-derived from validated summaries, not a live repository audit. `Confirmed` means accepted user direction or stable thesis scope; `Observed` means console/command output appeared in the transcript; `Claimed` means an assistant or user said an edit/artifact exists without current verification; `Proposed` means it remains a design option. Every item still needs current-code verification where applicable. [chunk_001] [chunk_010] [chunk_016]

## Confirmed

- **Topic and evaluation:** Serbian-language master's thesis on solving 1D bin packing with a GA; compare solution quality/bin count and execution time against classical heuristics. [chunk_001] [chunk_016]
- **Named baseline scope:** FF, BF, NF, and Max Rest, with decreasing variants including FFD and NFD; later accepted experiment scope includes FF, FFD, BF, BFD, NF, NFD, MR, MRD, and GA. [chunk_005] [chunk_016]
- **Implementation language/environment:** Python in Conda environment `ai`; experiment commands must activate `ai` in the same shell invocation. [chunk_002] [chunk_012]
- **Project style:** modular files for parser, GA/chromosome, heuristics, solution lookup, experiment runner, and plots rather than notebook-only work. [chunk_002] [chunk_016]
- **Data organization:** keep benchmark families separated and keep the official `Solutions.xlsx` inside the project for portable lookup. [chunk_003] [chunk_004]
- **Required datasets:** Falkenauer U and T must be included; Scholl and Hard28 are already central, with Waescher added to later Hard classification. [chunk_005] [chunk_014] [chunk_016]
- **Reporting:** retain detailed Excel and TXT outputs with all results/timings; keep console output narrower and focused on metadata, bin counts, GA, and GA time. [chunk_006] [chunk_015] [chunk_016]
- **Research posture:** mixed or negative GA results are legitimate; do not suppress cases where deterministic heuristics win. [chunk_005]
- **Source fidelity:** inspect the supplied heuristic PDF and existing C++ implementations before claiming Python variants match them. [chunk_013] [chunk_016]
- **Repository imports:** six external projects should remain Git submodules linked to upstream repositories. [chunk_012]

## Implemented or observed

- **Observed parser evolution:** the integer-only Falkenauer parser failed on `100.0 60 20`; later experiment outputs show decimal triplet instances being parsed and executed. Current parser correctness is still unverified. [chunk_003] [chunk_006]
- **Observed workbook load:** `SolutionManager` repeatedly printed that it loaded 6,195 entries from Excel. A separate verifier observed nine sheet counts summing to 6,195 unique names. It did not prove that all rows are solved optima. [chunk_004] [chunk_014]
- **Observed logical pool:** a later run reported 1,415 instances: 880 Easy, 480 Medium, and 55 Hard, then selected 10 per category. [chunk_015] [chunk_016]
- **Observed early Falkenauer result:** for the first five `binpack5` triplet instances, reference count 20, FFD used 23/23/23/23/24, and GA used 21 on each. Single-run evidence only. [chunk_003] [chunk_004]
- **Observed Scholl result:** `N1C1W1_A.txt` reported reference/FFD/GA all equal to 25. [chunk_004]
- **Observed development experiment:** multiple 30-instance tables were run with population 40, 50 generations, mutation 0.2, unseeded sampling, and one effective GA run per instance. Some runs were interrupted; later transcript output reported saved XLSX/TXT and plots. [chunk_007] [chunk_011] [chunk_012]
- **Observed sample outcomes:** one run reported GA optimum hits of 5/10 Easy, 6/10 Medium, and 0/10 Hard, mean absolute gap 1.5 overall; a different unseeded sample reported GA optimum on 13/30 versus at least one classical heuristic on 24/30. [chunk_012] [chunk_016]
- **Observed timing pattern:** deterministic heuristics generally took microseconds to milliseconds, while GA took roughly 0.1–19 seconds in displayed runs. These timings lack platform controls and repetition. [chunk_011] [chunk_016]
- **Observed optimized-MR behavior:** MR+ matched MR bin counts and MRD+ matched MRD throughout one displayed run; some rows showed lower MR+ times. General parity/speedup is not proven. [chunk_012]
- **Observed anomalies:** descending variants sometimes used more bins than original-order variants on Falkenauer instances; this requires correctness and data-order investigation. [chunk_011] [chunk_016]
- **Observed output generation:** `python run_experiments.py` was reported to generate table/result files, and `python plot_results.py` reported saving gap and time PNGs. Current files and contents have not been audited here. [chunk_011]
- **Claimed implementation:** transcript code listings include FF/FFD, FFL, FFD+, BF/BFD, BFL, NF/NFD, NFD+, MR/MRD, MR+/MRD+, and GA result columns, plus bin and convergence plots. Multiple near-duplicate listings exist, so the saved version is uncertain. [chunk_013] [chunk_015] [chunk_016]
- **Observed Git operation:** six external repositories were reportedly added as submodules and `.gitmodules` was staged; complete gitlink/fresh-clone verification was not shown. [chunk_012]

## Proposed

- **GA decoder comparison:** evaluate otherwise matched GA variants using First Fit and Best Fit decoders. User endorsed the direction; implementation/results were not shown. [chunk_011]
- **Final statistical protocol:** use fixed seeds or a fixed instance manifest, multiple independent GA runs, a separate parameter-tuning set, and distributional summaries. Ten runs per configuration is literature-inspired, not yet accepted as the final rule. [chunk_003] [chunk_011] [chunk_016]
- **Metrics:** report absolute and relative gaps, optimum-hit rate, best/mean/median/std, runtime distribution, and paired category/family comparisons rather than only `Gap_GA`. [chunk_011] [chunk_016]
- **Reference semantics:** preserve LB, UB, and status and label each target as proven optimum, best known, or unknown. [chunk_003] [chunk_014]
- **Restartability:** record seed/configuration/instance manifest and checkpoint structured result rows so interruptions do not lose Excel-equivalent data. [chunk_007] [chunk_016]
- **Visualization policy:** retain selected bin-layout and convergence figures as thesis/debugging aids, but choose a documented representative subset instead of automatically plotting every instance. [chunk_012] [chunk_016]
- **Algorithm extensions:** FF+/FF++/FFD+/FFD++/NFD+ and lookup/counting-sort variants remain candidates, subject to PDF/C++ fidelity tests and explicit scope. [chunk_012] [chunk_013]
- **GGA positioning:** describe Falkenauer GGA as literature context/future work unless the user explicitly expands scope to implement it. This remains an assistant recommendation, not a final user decision. [chunk_001]

## Unverified

- **Current source state:** actual contents of `project/src/*.py`, `project/run_experiments.py`, and `project/plot_results.py`; many edits exist only as conversational claims/code blocks. [chunk_003] [chunk_010] [chunk_013]
- **GA mechanics:** authoritative fitness, decoder, tournament behavior, crossover identity/correctness, mutation reevaluation, elitism, population-size edge cases, and convergence history meaning. [chunk_001] [chunk_012] [chunk_016]
- **Heuristic fidelity:** whether MR exactly matches the intended Max-Rest definition; whether FFL/BFL correspond to PDF FF+/FF++; whether counting-sort and priority-queue versions preserve source semantics; whether BFL belongs in the cited comparison set. [chunk_005] [chunk_013] [chunk_014]
- **Parser coverage:** strict count validation, decimal/scaling policy, CSP demand support, Falkenauer logical-name normalization, and behavior on all family formats. [chunk_003] [chunk_014]
- **Workbook semantics:** all-sheet loading in the actual `SolutionManager`, duplicate normalization, which bound is returned, solved/open filtering, and whether the 6,195 values are all proven optima. [chunk_014] [chunk_016]
- **Falkenauer scaling:** original/local T capacity 100 with decimals versus BPPLIB capacity 1000. [chunk_002] [chunk_003]
- **Physical/logical coverage:** the explanation that eight unmatched `binpack*.txt` files map completely through 160 internal instance names. [chunk_014] [chunk_015]
- **Category correctness:** whether the 55 Hard pool is exactly Scholl set 3 + Waescher + Hard28 and whether that grouping is academically defensible. [chunk_015] [chunk_016]
- **Generated artifacts:** current existence, completeness, schema, and provenance of result workbooks, TXT reports, and plots. [chunk_009] [chunk_016]
- **Submodule state:** `.gitmodules`, gitlinks, working-tree cleanliness, and fresh-clone initialization. [chunk_011] [chunk_012]
- **Literature details:** exact bibliographic metadata/page references and interpretation of Falkenauer, Munien, Rieck, Rajacic, and encoding-damaged excerpts. [chunk_001] [chunk_011] [chunk_016]

## Blocked or unresolved

- **Authoritative plan:** `THESIS_PLAN.md` and `IMPLEMENTATION_PLAN.md` overlap; the newer/authoritative document is unidentified. [chunk_016]
- **Final GA design:** permutation GA + FF is the working direction, but GA-BF, GGA scope, final objective, parameters, and stopping criteria are not settled. [chunk_001] [chunk_011] [chunk_012]
- **Final experiment design:** exact benchmark manifest, category rationale, number of instances, number of GA runs/seeds, tuning/evaluation separation, and statistical tests are unresolved. [chunk_011] [chunk_015] [chunk_016]
- **Reference naming:** the current `Opt` label may mix proven optima and best-known values; unknown values may be recorded as zero gap. [chunk_014] [chunk_016]
- **Correctness anomaly:** descending variants can be worse than base variants on reported Falkenauer cases; no diagnosis distinguishes valid order effects from implementation/data defects. [chunk_011] [chunk_016]
- **Runtime methodology:** machine specification, package versions, timer, warm-up, process isolation, and variability protocol are absent. [chunk_016]
- **Plot scope:** whether bin/convergence plots are deliverables, representative illustrations, or debugging artifacts. [chunk_012] [chunk_016]
- **CSP scope:** benchmark documentation describes CSP input, but inclusion and parser support are not decided. [chunk_014]
- **Current execution access:** exact activation/invocation for Conda `ai` must be confirmed before automated validation. [chunk_012]

## Artifact map

| Artifact | Transcript role | State |
|---|---|---|
| `THESIS_PLAN.md` | Thesis/experiment plan | Exists by claim; authority relative to implementation plan unresolved. [chunk_001] [chunk_016] |
| `IMPLEMENTATION_PLAN.md` | Implementation plan | Exists by claim; overlaps thesis plan. [chunk_016] |
| `project/src/parser.py` | Multi/single-instance parsing | Repeatedly claimed/shown; current behavior unverified. [chunk_003] [chunk_016] |
| `project/src/chromosome.py` | Permutation, decoded bins, fitness, visualization | Proposed/claimed; current contract unverified. [chunk_002] [chunk_012] |
| `project/src/ga.py` | Selection, crossover, mutation, elitism, history | Proposed/claimed; needs audit. [chunk_002] [chunk_016] |
| `project/src/heuristic.py` | Base and optimized heuristics | Multiple claimed versions; needs C++ parity tests. [chunk_011] [chunk_013] |
| `project/src/solution_manager.py` | Excel reference lookup | Observed load message; semantics unverified. [chunk_004] [chunk_014] |
| `project/run_experiments.py` | Discovery, categorization, sampling, execution, export | Repeatedly shown and run; saved version/configuration uncertain. [chunk_013] [chunk_016] |
| `project/plot_results.py` | Gap/time charts | Reported to save PNGs; current algorithm list/scale unverified. [chunk_011] [chunk_012] |
| `project/data/Solutions.xlsx` | LB/UB/status catalogue for nine families | 6,195 rows/names observed; reference semantics need validation. [chunk_014] |
| `project/results/experiment_results.xlsx` | Detailed structured results | Reported written; current completeness/provenance unverified. [chunk_011] [chunk_016] |
| `project/results/experiment_results.txt` | Incremental readable report | Reported written; schema/version unverified. [chunk_009] [chunk_016] |
| `project/results/plots/` | Aggregate, bin-layout, convergence plots | Reported/proposed; thesis selection policy unresolved. [chunk_012] [chunk_016] |
| `BASIC ANALYSIS OF BIN-PACKING HEURISTICS.pdf` | Heuristic definitions/implementation reference | Must be checked directly; excerpts were damaged. [chunk_011] [chunk_012] |
| `RajacicJasna.pdf` | Related Serbian thesis/model | User-endorsed source; not yet reviewed in this evidence set. [chunk_001] [chunk_016] |
| `bin-packing-heuristics/` | C++ parity reference | User requires inspection; no completed audit shown. [chunk_013] [chunk_016] |
| `.gitmodules` and six external directories | Upstream source links | Submodule addition reported; final state unverified. [chunk_012] |

## Immediate checklist

- [ ] Inspect current Git status, `.gitmodules`, and only the thesis project files; preserve user changes. [chunk_011] [chunk_012]
- [ ] Read and reconcile `THESIS_PLAN.md` and `IMPLEMENTATION_PLAN.md`; select the authority with the user. [chunk_016]
- [ ] Confirm the exact Conda `ai` activation command before running Python. [chunk_002] [chunk_012]
- [ ] Audit parser contracts with one file from each family plus all eight Falkenauer containers; verify logical-instance counts and item totals. [chunk_003] [chunk_014]
- [ ] Audit `SolutionManager` across all sheets; retain LB, UB, status, and reference type; make unknown gap missing, never zero. [chunk_003] [chunk_014] [chunk_016]
- [ ] Audit heuristic names/semantics against the PDF and C++ sources; add controlled parity fixtures. [chunk_013] [chunk_014]
- [ ] Audit GA representation, objective, operators, reevaluation, feasibility, and seed handling; resolve the two fitness formulas. [chunk_001] [chunk_012]
- [ ] Reproduce and diagnose a descending-order anomaly before trusting full experiments. [chunk_011] [chunk_016]
- [ ] Agree a fixed pilot manifest and repeated-seed protocol with the user; do not change the current parameters silently. [chunk_007] [chunk_015]
- [ ] Make result rows checkpointable and record configuration, seed, environment, and reference provenance. [chunk_007] [chunk_016]
- [ ] Run a small pilot, validate artifacts, then approve the costly final experiment. [chunk_006] [chunk_016]
- [ ] Verify primary literature and bibliography before writing thesis claims or quotations. [chunk_001] [chunk_011] [chunk_016]
