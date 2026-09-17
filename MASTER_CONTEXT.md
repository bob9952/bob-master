# Master Context

## Purpose and evidence boundary

This file is a restart brief synthesized from the validated transcript summaries `summaries/chunk_001.md` through `chunk_016.md`. It records what the user accepted, what assistants proposed or claimed to edit, and what command output was actually observed. It is not a verification of the current repository. Before relying on any implementation or generated artifact, inspect the current files and rerun focused checks in Conda environment `ai`. [chunk_001] [chunk_003] [chunk_016]

## Thesis objective and scope

The approved topic is *Rešavanje jednodimenzionalnog problema pakovanja u kutije korišćenjem genetskog algoritma* (solving the one-dimensional bin-packing problem with a genetic algorithm). The application identifies Nikola Subotić as the student and Miroslav Marić as mentor. The problem is to assign items of varying weights to the minimum number of identical fixed-capacity bins without exceeding capacity; the thesis brief frames it as NP-hard and motivates heuristic/metaheuristic treatment. [chunk_001] [chunk_016]

The stated comparison scope is a genetic algorithm versus First Fit, Best Fit, Next Fit, and Max Rest, including decreasing/sorted variants. The primary evaluation criteria are bin count/solution quality and execution time. The application also mentions logistics, industrial packing, resource allocation, and memory allocation as application areas. [chunk_005] [chunk_016]

The working GA direction is a permutation of item IDs decoded into a feasible packing by a constructive heuristic. First Fit is the established working decoder in the transcript; comparing a First-Fit decoder with a Best-Fit decoder was later endorsed by the user but not shown as implemented or evaluated. This is a permutation GA, not a faithful implementation of Falkenauer's Grouping Genetic Algorithm (GGA). [chunk_002] [chunk_011] [chunk_012]

## User preferences and accepted choices

The user chose Python and named Conda environment `ai`; every experiment command must activate that environment in the same shell invocation. The user later asked agents not to keep trying arbitrary Python executables until the Conda interpreter was configured. [chunk_002] [chunk_012]

The user chose a modular project rather than continuing only in the notebook. The intended separation is parsing, chromosome/GA logic, heuristics, solution metadata, experiment orchestration, and plotting. The user also wants benchmark data organized by source/family and wants the official `Solutions.xlsx` copied into the project rather than referenced through a machine-specific path. [chunk_002] [chunk_003] [chunk_004]

The accepted comparison set grew from FF/FFD and GA to FF, FFD, BF, BFD, NF, NFD, MR, MRD, and GA. Later runs/proposals also include FFL, FFD+, BFL, NFD+, MR+, and MRD+. The user requires all available algorithms to remain in detailed results; the exact names and fidelity of the optimized variants still require source comparison. [chunk_005] [chunk_013] [chunk_016]

The user wants detailed machine-usable and readable outputs. The settled presentation direction is detailed Excel and TXT files retaining every algorithm's bin count and runtime, while the live console emphasizes category, full instance name, item count, capacity, reference value, heuristic bin counts, GA bin count, and GA runtime. The earlier ultra-wide console with every heuristic time was rejected as too crowded. [chunk_006] [chunk_015] [chunk_016]

The user approved Easy/Medium/Hard grouping as an experiment presentation device, but the meaning of these labels is not academically settled. The later implemented/proposed rule marks an instance Hard if capacity is at least 100000 or it belongs to Waescher/Hard28, Medium if capacity is at least 1000, and Easy otherwise. Treat this as project stratification, not a general hardness theorem. [chunk_011] [chunk_015] [chunk_016]

The user decided that six imported external projects should remain Git submodules linked to their upstream repositories, not be flattened into ordinary directories. The transcript reports successful `git submodule add` operations, but the final gitlink state was not fully verified. [chunk_012]

The user prefers incremental improvement and honest interpretation: GA results that are worse than FFD/BFD are valid findings, not failures to hide. The user also wants the existing C++ implementations and the supplied heuristic-analysis PDF inspected before Python variants are claimed equivalent. [chunk_005] [chunk_011] [chunk_013]

## Settled, proposed, and superseded choices

**Accepted user decisions:** use Python/Conda `ai`; use a modular project; keep source-oriented dataset folders and local `Solutions.xlsx`; compare the classical heuristic families and GA; include Falkenauer U and T; retain detailed XLSX/TXT output; keep external repositories as submodules; inspect C++ implementations before claiming parity; and keep terminal output compact while retaining detailed timings in files. [chunk_002] [chunk_004] [chunk_006] [chunk_012] [chunk_013] [chunk_016]

**Assistant proposals that are not final methodology:** random sampling of 10 instances per category, capacity/family-based category rules, GA settings such as population 40 and 50 generations for quick runs or 100 and 500 for a possible final run, ten repeated runs inspired by Munien et al., GA-with-BF, fitness exponent experiments, MR+ and other optimized heuristic variants, and per-instance convergence/bin plots. These require explicit confirmation or validation before being treated as thesis design. [chunk_003] [chunk_007] [chunk_008] [chunk_011] [chunk_016]

**Superseded or rejected directions:** C++ as the primary implementation language; notebook-only development; `solutions.csv`; hard-coded machine paths; assuming one instance per file; excluding `binpack*.txt`; sampling physical files before parsing logical instances; CSV/Markdown as the main result formats; and the ultra-wide console containing every timing column. [chunk_002] [chunk_003] [chunk_004] [chunk_006] [chunk_016]

**Not settled:** whether GGA should remain literature/future work or be implemented; whether GA-FF and GA-BF will both be evaluated; the authoritative fitness formula; final GA parameters and stopping rule; fixed instance set versus stratified sample; number of independent GA runs; category semantics; and which optimized heuristic variants belong in the final comparison. [chunk_001] [chunk_011] [chunk_012] [chunk_016]

## Working architecture and data flow

The transcript's intended code map is `project/src/parser.py` for instance ingestion, `project/src/chromosome.py` and `project/src/ga.py` for GA representation/search, `project/src/heuristic.py` for constructive methods, `project/src/solution_manager.py` for Excel reference lookup, `project/run_experiments.py` for orchestration, and `project/plot_results.py` for aggregate plots. These paths were repeatedly shown or named, but current contents must be inspected because many transcript entries are assistant code proposals rather than verified edits. [chunk_002] [chunk_010] [chunk_016]

The intended ingestion flow is: recursively find `.txt` files under script-relative `project/data`; detect Falkenauer aggregate files versus single-instance BPP files; parse every logical instance; attach source folder/file metadata; and only then categorize and sample. Falkenauer aggregate containers must yield all internal instances, rather than only `instances[0]`. [chunk_003] [chunk_006] [chunk_014]

Falkenauer aggregate parsing is expected to read a problem count, then for each logical instance its name, capacity, item count, embedded best-known count, and exactly that many weights. Single-instance BPP parsing is expected to read item count, capacity, and weights, leaving the reference value to `SolutionManager`. Decimal Falkenauer T values require float-aware parsing and either a documented epsilon or exact rescaling policy. CSP weight-demand input was described in benchmark documentation but parser support was not demonstrated. [chunk_003] [chunk_014]

Reference lookup is intended to use an embedded `best_known` value first and `SolutionManager.get_optimal(name)` as fallback. Workbook matching must normalize internal Falkenauer names such as `u120_00` to workbook names such as `Falkenauer_u120_00.txt` while handling ordinary filenames directly. The current logic must be checked to ensure it loads all sheets, preserves LB/UB/status, and does not call every upper bound an optimum. [chunk_003] [chunk_014] [chunk_016]

For deterministic methods, `solve_heuristic` copies the item order, optionally sorts descending (ordinary sort or counting sort), executes the packing function, and records bin count and wall-clock time. The base semantics are: FF chooses the first feasible bin, BF the feasible bin with least residual space, NF only the current bin, and MR/Worst Fit the feasible bin with greatest residual space. MR+ uses a priority queue. [chunk_005] [chunk_011] [chunk_016]

The GA chromosome is intended to be a permutation of item IDs. Decoding walks that order and applies First Fit, producing feasible bins for a valid permutation. The discussed pipeline is random initialization, tournament selection, order-preserving crossover, swap mutation with reevaluation, elitist survival, and a generation limit. Actual `ga.py` behavior—including parent uniqueness, crossover identity, reevaluation, and history semantics—remains to be audited. [chunk_001] [chunk_002] [chunk_012]

Two incompatible fitness definitions appear in the transcript: minimize `1 - mean((fill_i/C)^2)`, and minimize `N - mean((fill_i/C)^2)` so bin count dominates and fullness breaks ties. The authoritative implementation and thesis formula must be established from current code and justified consistently. [chunk_001] [chunk_002] [chunk_012]

The intended result flow is one row per logical instance containing source metadata, items, capacity, reference value, bin count and timing for every heuristic, GA result/timing, and gap fields. Detailed TXT is flushed incrementally; Excel is written from accumulated rows. Bin-layout and convergence PNGs were proposed/generated per instance, but their thesis role and generation frequency are unresolved. [chunk_007] [chunk_012] [chunk_016]

## Datasets and reference values

Falkenauer consists of 160 instances: 80 uniform instances and 80 constructed triplet instances. The original aggregate distribution uses `binpack1`-`binpack4` for uniform instances (20–100 item sizes, capacity 150) and `binpack5`-`binpack8` for triplets. Triplet optima are constructed as `n/3`, exactly three items per bin. The transcript contains a scale conflict: original triplet descriptions/local evidence use capacity 100 and decimal weights, while BPPLIB documentation is reported as capacity 1000. Do not mix these representations without verifying whether one is a scaling of the other. [chunk_002] [chunk_003] [chunk_014]

The original Falkenauer uniform metadata historically treated its best-known counts as proven optima except for `u120_08`, `u120_19`, `u250_07`, `u250_12`, and `u250_13`. A later BPPLIB workbook view reportedly marks the listed Falkenauer instances solved with LB=UB. The thesis must distinguish historical best-known values from later proven optima and cite provenance/date. [chunk_001] [chunk_002]

Scholl contains 1,210 instances split into sets of 720, 480, and 10, with capacities roughly 100–150, 1000, and 100000. The transcript also identifies Waescher (17), Schwerin (200), Schoenfield Hard28 (28), Randomly Generated (3,840), Augmented Non-IRUP (250), Augmented IRUP (250), and GI (240) workbook rows. These nine sheet counts sum to 6,195. [chunk_003] [chunk_014]

Observed workbook verification loaded 6,195 unique names and matched 1,255 of 1,263 local physical `.txt` files by filename. The eight unmatched files were the Falkenauer `binpack1`-`binpack8` containers; an assistant explained that their parsed internal instance names, not container filenames, correspond to workbook rows. That explanation is plausible but was not directly verified in the summary evidence. [chunk_014] [chunk_015]

The later category run discovered 1,415 logical instances: 880 Easy, 480 Medium, and 55 Hard. The 55 Hard count is consistent with—but does not prove—the intended combination of Scholl set 3 (10), Waescher (17), and Hard28 (28). [chunk_015] [chunk_016]

## Literature and provenance map

Core benchmark/method sources named in the transcript are Falkenauer's *A Hybrid Grouping Genetic Algorithm for Bin Packing* (1994 working paper versus 1996 *Journal of Heuristics* publication; reconcile the citation), Delorme–Iori–Martello's BPPLIB paper (2018) and exact-method survey (2016), Scholl–Klein–Jürgens' BISON paper (1997), Schoenfield's Hard28 report (2002), Waescher–Gau (1996), and Schwerin–Waescher (1997). [chunk_001] [chunk_002] [chunk_014]

Munien et al. (2020) is the main comparative-methodology reference in the transcript. Its reported design selected 30 instances across three categories and ran each metaheuristic/decoder combination ten times. Its claims and results are literature evidence only, not local experiment results, and exact pages/bibliographic details must be checked before citation. [chunk_003] [chunk_004] [chunk_006]

`BASIC ANALYSIS OF BIN-PACKING HEURISTICS.pdf` (attributed in the conversation to Bastian Rieck) is the named source for MR/MR+, FF/FF+/FF++, FFD/FFD+/FFD++, NF/NFD/NFD+, and BF naming and implementation ideas. The excerpts were encoding-damaged; formulas, data structures, complexity claims, and bibliography must be checked in the original PDF and against `bin-packing-heuristics` C++ code. [chunk_011] [chunk_012] [chunk_013]

`RajacicJasna.pdf` is considered by the user a strong related master's-thesis model. The assistant interpreted it as support for a metaheuristic that supplies an ordering followed by constructive packing, but that interpretation was not source-verified and must not be cited until checked. [chunk_001] [chunk_016]

## Experiment evidence actually observed

Early observed runs established that the parser initially failed on decimal Falkenauer metadata, then later runs on the first five `binpack5` triplet instances reported optimum 20, FFD 23/23/23/23/24, and GA 21 for all five. These were single outcomes without seeds, runtimes, or repeated-run distributions. [chunk_003] [chunk_004]

An observed Scholl run for `N1C1W1_A.txt` reported capacity 100, 50 items, and optimum/FFD/GA all equal to 25. A later 12-instance sample showed mixed behavior: GA lost to simple heuristics on some Scholl set-1 cases, improved on them without reaching optimum on `N4W2B1R3` and three Scholl set-3 HARD cases, and was much slower. [chunk_004] [chunk_005]

Several 30-instance development runs were observed. They used unseeded random samples, one GA execution per instance, population 40, 50 generations, and mutation probability 0.2. Some runs were interrupted; at least one completed-looking run generated Excel/TXT and plots, but exact artifact state must be checked. [chunk_007] [chunk_011] [chunk_012]

One reported 30-instance run found GA optimal on 5/10 Easy, 6/10 Medium, and 0/10 Hard, with total gap 45 and mean gap 1.5; another unseeded sample derived in the final summary found GA optimal on 13/30, while at least one classical heuristic was optimal on 24/30. These results are not contradictory because samples/runs were unseeded, but neither is thesis-grade evidence. [chunk_012] [chunk_016]

Across reported runs, deterministic heuristics usually took microseconds to a few milliseconds, while GA ranged roughly from tenths of a second to about 19 seconds and grew slow on larger 500-item instances. Hardware, timing protocol, warm-up, seeds, and repeated-run variance were not recorded, so only the qualitative runtime gap is presently defensible. [chunk_011] [chunk_012] [chunk_016]

Observed results consistently show that GA is not universally dominant. It sometimes improved on all displayed heuristics and hit the reference value, particularly in selected medium/hard instances, but often lost to FF/BF/FFD/BFD and never hit the reference on some Hard samples. NF/NFD were commonly much worse. This mixed result should drive analysis rather than be smoothed into a superiority claim. [chunk_005] [chunk_011] [chunk_016]

MR+ and MRD+ matched MR and MRD bin counts throughout one displayed run, with individual examples suggesting faster execution. This is encouraging development evidence, not proof of general equivalence or speedup; controlled parity tests and repeated timings are still needed. [chunk_012]

Descending variants sometimes performed markedly worse than original-order variants on Falkenauer instances, for example FF reaching 40 while FFD reached 45/46 in reported triplet rows. This may be valid order sensitivity, a format/scaling issue, or an implementation defect; it must be investigated before interpretation. [chunk_011] [chunk_016]

## Known risks, contradictions, and gaps

**Repository-state risk:** transcript summaries repeatedly contain pasted code and assistant claims that files were created or changed without a diff, syntax check, or post-change run. Current code, data, results, and submodule state must be treated as unknown until inspected. [chunk_003] [chunk_010] [chunk_013]

**Reference-value risk:** the console calls values `Opt`, but the lookup may be using `Best UB` without checking `Best LB == Best UB` or `Status == Solved`. Embedded Falkenauer values may be historical best-known counts. Unknown references are sometimes converted to gap zero, falsely implying optimality. [chunk_003] [chunk_014] [chunk_016]

**Methodology risk:** the current development protocol is an unseeded random sample of at most 10 per category and one GA run. `RUNS_PER_INSTANCE` is declared but unused. There is no fixed evaluation set, repeated-run distribution, parameter-tuning split, statistical comparison, or recorded platform/timing protocol. [chunk_007] [chunk_015] [chunk_016]

**Category risk:** capacity thresholds were initially presented as Easy/Medium/Hard despite not being a validated hardness measure. Later family overrides move Waescher and Hard28 to Hard. The final methodology must define whether categories mean source family, capacity scale, or empirical difficulty and cite/justify the rule. [chunk_006] [chunk_014] [chunk_016]

**Algorithm-fidelity risk:** Max Rest was initially assumed equivalent to Worst Fit; FFL/BFL labels may not match the PDF's FF+/FF++ scheme; BFL is not established by the supplied naming table; counting-sort variants fall back on floats; and current Python behavior has not been compared with C++ fixtures. [chunk_005] [chunk_013] [chunk_014]

**GA-validity risk:** the exact fitness, selection, crossover, mutation reevaluation, decoder, elitism, and edge-case handling are not yet verified from current code. Earlier notebook code visibly had a missing argument, printed bin capacity as bin count, and could mutate a permutation without reevaluating. [chunk_001] [chunk_012] [chunk_016]

**Data-format risk:** Falkenauer T has conflicting capacity/scale descriptions; decimal feasibility uses an unvalidated epsilon; CSP demand parsing is unproven; aggregate container naming differs from workbook keys; and Waescher spelling/encoding is inconsistent. [chunk_003] [chunk_014] [chunk_015]

**Output risk:** Excel may be written only at the end while TXT is incremental, so interruption can lose structured partial results. Per-instance plots are generated despite comments suggesting selective plots, potentially adding runtime/storage noise. Sorting sampled lists after extending the final test set does not reorder the combined list. [chunk_007] [chunk_014] [chunk_016]

## Current priorities

1. Verify the current repository and establish the actual implementation baseline before accepting any transcript claim. Inspect the named project modules, submodule metadata, data layout, result artifacts, and both planning documents. [chunk_012] [chunk_016]
2. Audit correctness and contracts: parser formats/counts, workbook lookup and solved/open semantics, heuristic parity against C++, and GA representation/operators/fitness/reevaluation. [chunk_014] [chunk_016]
3. Freeze a reproducible experimental protocol: fixed instance manifest or seed, explicit family/category policy, multiple GA seeds/runs, final parameters, hardware/software record, timing method, and metrics. [chunk_011] [chunk_015] [chunk_016]
4. Run a small validated pilot before a full benchmark. Use it to prove feasibility, reference lookup, deterministic heuristic parity, GA reproducibility, checkpointing, and output schemas. [chunk_003] [chunk_012] [chunk_016]
5. Only then run the final study and write claims from generated evidence, labeling proven optimum versus best known and separating literature results from local results. [chunk_001] [chunk_014] [chunk_016]

## Recommended next actions

1. Read `THESIS_PLAN.md`, `IMPLEMENTATION_PLAN.md`, and the actual modules under `project/`; decide which plan is authoritative and record a narrow implementation gap list. Do not rewrite architecture before following current patterns. [chunk_016]
2. Confirm the Conda `ai` invocation, then run syntax/import checks and focused unit fixtures rather than a full experiment. Every Python command should activate `ai` in the same shell command. [chunk_002] [chunk_012]
3. Validate `SolutionManager` against all nine workbook sheets. Store `Best LB`, `Best UB`, and `Status`; expose a reference label (`optimal`, `best-known`, `unknown`); never map unknown to zero gap. [chunk_003] [chunk_014] [chunk_016]
4. Validate parsing by family, including every Falkenauer internal instance, decimals/scaling, exact item counts, and at least one CSP-format file if CSP is in scope. Produce a deterministic coverage report based on logical instances, not only physical filenames. [chunk_003] [chunk_014] [chunk_015]
5. Compare Python heuristics with the C++ reference on controlled fixtures and real instances. Rename or remove variants that do not faithfully correspond to the cited methods; investigate descending-order anomalies. [chunk_013] [chunk_014] [chunk_016]
6. Audit GA code and document chromosome, decoder, objective, tournament selection, crossover, mutation, elitism, termination, and seed handling. Add invariants for permutation validity, capacity feasibility, item completeness/uniqueness, and reevaluation after mutation. [chunk_001] [chunk_012] [chunk_016]
7. Agree the final experiment protocol with the user before costly runs. A defensible candidate is a fixed, published manifest stratified by benchmark family; a separate tuning subset; at least 10 independent GA seeds per evaluation instance; and reporting best/mean/median/std, optimum-hit rate, absolute/relative gap, and runtime. This is a recommendation, not an accepted design. [chunk_003] [chunk_011] [chunk_016]
8. Make runs restartable by recording configuration/seed/instance manifest and checkpointing structured rows. Generate representative plots deliberately rather than for every instance by default. [chunk_007] [chunk_016]
9. Recheck primary PDFs and bibliographic metadata before thesis prose. Do not quote mojibake excerpts or reuse assistant interpretations as citations. [chunk_001] [chunk_011] [chunk_016]
