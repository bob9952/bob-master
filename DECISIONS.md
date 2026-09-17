# Decision Log

This log records decisions visible in the transcript summaries. Status is deliberately strict:

- **Accepted** means the user explicitly chose or approved the direction.
- **Tentative** means it is the current working direction or appears in executed code, but is not a finalized thesis-method decision.
- **Proposed** means it was suggested, usually by the assistant, without clear user acceptance.
- **Rejected** means the user rejected it or later evidence superseded it.
- **Unresolved** means a decision is still needed.

Assistant suggestions are not promoted to accepted decisions merely because code was pasted or an edit was claimed.

## Accepted decisions

| Decision | Rationale | Alternatives and consequences | Evidence |
|---|---|---|---|
| Implement the thesis project in Python and use the existing Conda environment `ai`. | Python was chosen as faster and easier to develop than C++ for this project. | C++ was considered but rejected for the main implementation. Every Python experiment command must activate `ai` in the same shell invocation. | [chunk_002] |
| Move the working implementation out of a notebook into a modular project structure. | Parsing, representations, search, heuristics, and experiment entry points need separate responsibilities. | Continuing only in `GA-1D-BPP.ipynb` would preserve notebook defects and make experiments harder to reproduce. | [chunk_002] |
| Keep benchmark data organized by provenance and family, including Falkenauer `U`/`T`, Scholl `set_1`/`set_2`/`set_3`, and Schoenfield/Hard28. | The user wanted scripts to conform to the physical dataset organization and retain provenance. | Flattening all files would simplify paths but obscure dataset identity and make family-specific handling harder. | [chunk_003] [chunk_004] |
| Include Falkenauer U and T instances and handle their aggregate, multi-instance file format. | Falkenauer is central to the thesis comparison, and each `binpack` file contains many logical instances. | Excluding `binpack*.txt`, sampling files before parsing, or reading only `instances[0]` omits Falkenauer or most contained instances. | [chunk_006] |
| Use the official `Solutions.xlsx` inside the project data area as the reference-metadata source. | A copied workbook makes the project portable and avoids a machine-specific BPPLIB path. | `solutions.csv`, hard-coded optima, the Excel lock file `~$Solutions.xlsx`, and an absolute BPPLIB path were displaced. The workbook still needs status/bound validation before every value is called an optimum. | [chunk_003] [chunk_004] |
| Compare the GA with FF, FFD, BF, BFD, NF, NFD, MR, and MRD, and retain result and timing data. | These methods align with the thesis application, which evaluates bin count/solution quality and execution time. | Reporting only FFD and GA would not match the approved scope. Optimized variants may be added, but they do not replace the named baselines. | [chunk_005] [chunk_016] |
| Treat a GA result that is worse than a constructive heuristic as valid evidence. | The thesis should analyze where the GA succeeds or fails rather than suppressing inconvenient results. | Assuming or presenting universal GA superiority would contradict observed runs. | [chunk_005] [chunk_011] |
| Store detailed results under `project/results/` as XLSX plus a readable TXT report. | Excel is easier to inspect and analyze; TXT provides a readable incremental log. | CSV and Markdown were superseded as the primary result formats, though CSV remains suitable in principle for analysis. | [chunk_006] [chunk_007] |
| Keep detailed per-method timings in Excel/TXT, but use a compact live console focused on category, instance, item count, capacity, reference value, heuristic bin counts, GA bin count, and GA time. | The full result/time table did not fit the available monitor, while detailed files preserve the data. Remaining displayed time values should use greater precision. | Earlier requirements to print every algorithm time in separate console columns, and later to print every available algorithm, were superseded by the compact-console request. | [chunk_007] [chunk_008] [chunk_013] [chunk_015] [chunk_016] |
| Keep full instance names where the chosen output layout permits and preserve `Itm` and `Cap`. | Truncation and removal of these fields made output harder to identify and interpret. | Ellipsis-truncated names and accidental removal of item/capacity columns were rejected. Console width may still require a deliberate compact schema. | [chunk_008] [chunk_009] |
| Use Easy, Medium, and Hard groups for comparative reporting. | The user found category-based reporting clear and similar to the cited experimental presentation. | Pure folder sampling was displaced. The exact classification rule remains tentative because capacity alone was inadequate. | [chunk_006] [chunk_011] |
| Keep the six external projects as Git submodules linked to their upstream repositories. | The user explicitly wanted to preserve upstream links. | Flattening the projects into ordinary tracked directories was rejected. | [chunk_012] |
| Avoid repeated attempts to execute Python until the agent knows the correct Conda `ai` invocation. | Earlier attempts resolved to an unsuitable Windows/Microsoft Store Python alias. | The user can run manually, or automation can resume once the exact environment activation command is established. | [chunk_012] [chunk_015] |

## Tentative working decisions

| Working decision | Why it is tentative | Alternatives and consequences | Evidence |
|---|---|---|---|
| Use a permutation chromosome decoded by First Fit. | It became the agreed working implementation direction and appears throughout the shown code, but the original discussion did not close the academic choice between a permutation GA and Falkenauer-style Grouping GA. | A true Grouping GA would be more faithful to Falkenauer but materially more complex; a GA with a Best Fit decoder is also under consideration. | [chunk_001] [chunk_002] [chunk_011] |
| Use the objective `N - mean((fill_i / C)^2)` so bin count dominates and fullness breaks ties. | This formula appeared in later proposed modular code, while the original notebook used `1 - mean((fill_i / C)^z)`. The authoritative repository implementation was not verified. | Retaining the original fill-only cost can compare solutions with different bin counts ambiguously; other exponents or lexicographic objectives need evaluation. | [chunk_002] [chunk_012] |
| For development runs, sample up to 10 instances per category and use population 40, 50 generations, mutation probability 0.2, and one GA execution per instance. | These values were explicitly described as reduced, quick-run settings rather than final thesis parameters; `RUNS_PER_INSTANCE` is declared but unused. | Final settings may require larger populations/generations, multiple seeds, and a fixed benchmark manifest. | [chunk_008] [chunk_015] [chunk_016] |
| Classify Hard as capacity at least 100,000 or membership in Waescher/Hard28; classify remaining capacity-at-least-1,000 cases as Medium and the rest as Easy. | This rule corrected the 10-case hard pool to a reported 55, but it mixes capacity and family identity and has not been academically justified. | Capacity-only classification misclassifies known hard families; family-only or empirical-hardness stratification may be more defensible. | [chunk_014] [chunk_015] [chunk_016] |
| Retain lookup/counting-sort/priority-queue variants alongside base heuristics. | Runs and code listings include FFL, BFL, FFD+, NFD+, MR+, and MRD+, but names and behavioral equivalence to the cited C++/PDF algorithms are not yet verified. | Remove or relabel variants that cannot be mapped faithfully; retain them as implementation experiments if clearly distinguished from literature algorithms. | [chunk_012] [chunk_013] [chunk_016] |
| Retain bin-layout and convergence plots as useful artifacts. | The user liked them, but their status as thesis deliverables versus debugging aids was not finalized, and code appears to generate them for every instance despite comments suggesting selective output. | Generate representative plots only, or keep all plots outside the formal thesis results. | [chunk_012] [chunk_016] |

## Proposed decisions not yet accepted

| Proposal | Rationale offered | Alternatives and consequences | Evidence |
|---|---|---|---|
| Compare otherwise identical GA variants using First Fit and Best Fit decoders. | This would isolate decoder influence and directly test a user-endorsed idea. | It requires shared seeds/populations/stopping conditions for a fair paired comparison and increases experiment cost. | [chunk_011] |
| Use fixed, representative samples or a fixed seed, with multiple independent GA runs per instance. | Reproducibility and stochastic variability cannot be assessed from unseeded single runs. | Full-set execution avoids sampling uncertainty but costs more; a published manifest offers a reproducible middle ground. | [chunk_003] [chunk_008] |
| Report absolute and relative gaps, optimum-hit rate, mean/median, standard deviation or confidence intervals, and runtime distributions. | One raw bin count and one wall-clock time are insufficient for thesis-grade stochastic comparison. | Minimal reporting is simpler but cannot support robust conclusions. | [chunk_005] [chunk_011] [chunk_016] |
| Load and validate all workbook sheets, retain LB/UB/status, and distinguish proven optimum from best known. | `Best UB` alone does not establish optimality; `LB == UB` or `Status == Solved` does. | Flattening only names and upper bounds is convenient but can mislabel open instances. | [chunk_003] [chunk_014] |
| Use script-relative paths throughout. | Scripts were commonly launched from inside the project folder, so paths prefixed with `project/` failed depending on the working directory. | Working-directory-relative paths are simpler but fragile. | [chunk_004] |
| Check MR+ against MR and MRD+ against MRD on controlled fixtures and retain both if runtime differences are useful. | The observed run showed equal bin counts and some apparent speedups, but one run does not prove equivalence. | Keep only the priority-queue variant if equivalence is proven, or label behavior differences explicitly. | [chunk_011] [chunk_012] |
| Defer FF++/FFD++ tree or map structures until simpler `+` variants and source mappings are verified. | Correct reproduction is more delicate, and capacity-indexed structures may be poor on capacity-100,000 cases. | Implementing everything immediately expands scope and risks mislabeling non-equivalent algorithms. | [chunk_011] [chunk_012] |
| Checkpoint structured output after every instance. | TXT is flushed incrementally, but Excel is written only after the full loop, so interruptions can lose structured partial results. | Periodic XLSX writes cost extra time; append-safe CSV/JSONL checkpoints could be another implementation. | [chunk_007] |

## Rejected or superseded decisions

| Rejected approach | Reason and consequence | Evidence |
|---|---|---|
| Use C++ as the main thesis implementation language. | The user selected Python for faster and easier development. C++ remains a reference source. | [chunk_002] |
| Continue solely in the original notebook. | The project needs modular parsing, algorithms, experiments, and reporting; the notebook also contains visible call/printing/state defects. | [chunk_002] |
| Keep Next Fit as the GA decoder by default. | The assistant argued it was too restrictive because it never revisits older bins. This rejection concerns the working decoder, not the inclusion of NF/NFD as baselines. | [chunk_001] |
| Treat a full Grouping GA as already selected. | It was discussed as complex and suitable for literature/future work, but no user decision committed the implementation to it. | [chunk_001] |
| Parse all benchmark files with one physical-format assumption. | Falkenauer aggregate files and BPPLIB single-instance files require distinct readers behind a common interface. | [chunk_003] |
| Parse Falkenauer capacity and weights as integers only. | The observed file contained `100.0` and decimal item values, causing a real parse failure. | [chunk_003] |
| Use `solutions.csv`, hard-coded fallback optima, `~$Solutions.xlsx`, or a machine-specific workbook path. | The project should use the real copied `Solutions.xlsx` and preserve official metadata. | [chunk_003] [chunk_004] |
| Exclude filenames containing `binpack`, sample physical files before parsing, or consume only the first parsed instance. | These choices omit Falkenauer or most logical instances in its containers. | [chunk_006] |
| Define Hard only as `capacity >= 100000`. | That produced only 10 hard cases and excluded Waescher and Hard28. | [chunk_014] [chunk_015] |
| Use a raw CSV as the only readable report, or make Markdown the primary human report. | The user preferred XLSX plus TXT under `results/`. | [chunk_005] [chunk_006] |
| Print an ultra-wide console containing every per-method timing. | It did not fit the monitor; detailed timings remain in files while the console is compact. | [chunk_015] [chunk_016] |
| Convert external repositories to ordinary directories. | The user requires submodules that retain upstream links. | [chunk_012] |
| Present example tables, assistant forecasts, or interrupted/historical notebook outputs as measured thesis results. | They lack a successful matching run, controlled protocol, or clear instance context. | [chunk_001] [chunk_002] |
| Call every workbook upper bound an optimum. | Open rows may have unequal LB and UB; reference status must be retained. | [chunk_003] [chunk_014] |

## Unresolved decisions

| Decision needed | Why it matters | Main options/consequences | Evidence |
|---|---|---|---|
| Finalize the GA method and academic claim. | The project must state whether it implements a permutation GA with a constructive decoder, a true Grouping GA, or a comparison of both. | Permutation GA is simpler and already used; Grouping GA is closer to Falkenauer; implementing both increases scope. | [chunk_001] [chunk_002] |
| Select the authoritative fitness function, selection, crossover, mutation, elitism, and decoder definitions. | Competing snippets use different fitness formulas and selection behavior, and the custom crossover is not clearly standard OX1 or PMX. | Freeze and document one validated operator set, or compare variants through controlled tuning. | [chunk_001] [chunk_012] |
| Define the final experimental protocol. | Current runs are single-run, unseeded, and development-scaled. | Decide fixed instances/seeds, runs per instance, final GA parameters, stopping criteria, timing protocol, tuning/evaluation split, and statistical summaries. | [chunk_003] [chunk_016] |
| Define and justify Easy/Medium/Hard. | The current rule combines capacity thresholds with family names and is not a general hardness definition. | Use benchmark families, source-defined categories, structural measures, or empirically validated hardness; rename categories if they are only strata. | [chunk_006] [chunk_016] |
| Decide the final benchmark coverage. | The thesis scope mentions Falkenauer, Scholl, and Hard28, while the workbook includes nine families and 6,195 rows. | Use all instances, a fixed representative subset, or a justified stratified sample. | [chunk_004] [chunk_014] |
| Decide how to represent proven optimum, best known, LB, UB, and missing references. | `Opt` and zero-gap fallbacks can make unproven or absent references look exact. | Preserve status and bounds, label gaps against UB where appropriate, and use missing values rather than zero. | [chunk_003] [chunk_010] [chunk_016] |
| Resolve Falkenauer scaling and numeric arithmetic. | Original triplets are described with capacity 100 and decimals locally, while BPPLIB documentation reports capacity 1000. | Verify whether data are scaled copies; choose exact integer rescaling or documented epsilon-based floats. | [chunk_002] [chunk_003] |
| Audit heuristic names and equivalence against the source PDF/C++ code. | FFL/BFL and `+`/`++` names may not map faithfully, and `best_fit_lookup` may truncate non-integral data. | Rename custom variants, port the source semantics exactly, or remove unsupported comparisons. | [chunk_013] [chunk_014] |
| Decide whether and how to include CSP files with demands. | The described benchmark library includes BPP and CSP formats, but CSP parsing was not demonstrated. | Exclude CSP explicitly or implement demand expansion/appropriate parsing with provenance. | [chunk_014] |
| Establish the correct Conda command and reproducible environment record. | Automated validation and thesis runtime claims require a known interpreter and package/hardware record. | Document `conda run` or activation plus Python/package versions and hardware. | [chunk_006] [chunk_012] [chunk_016] |
| Reconcile `THESIS_PLAN.md` and `IMPLEMENTATION_PLAN.md`. | The user said they overlap and that a newer plan is better, but did not identify the authoritative document. | Merge into one maintained plan or clearly deprecate the stale version. | [chunk_016] |

