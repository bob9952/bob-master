# Genetic algorithm evidence and open design

## Method identity

The implemented/proposed method is a permutation genetic algorithm: a chromosome orders item identifiers, and a constructive decoder turns that order into a packing. It is not Falkenauer's Grouping Genetic Algorithm (GGA), whose genes/operators act on groups or bins. [chunk_001] [chunk_002]

This distinction is central to the thesis. The permutation GA searches orderings and delegates feasibility to First Fit (or a proposed alternative decoder); GGA directly represents groups and uses group-aware crossover/mutation. Describing the current method as an implementation of Falkenauer's GGA would therefore be inaccurate. [chunk_001] [chunk_012]

## Current/proposed pipeline

| Stage | Evidence from the summaries | Status and unresolved point |
|---|---|---|
| Representation | A chromosome is a permutation of 1-based item IDs. [chunk_001] [chunk_002] | This is consistently described, but the current repository implementation was not audited in the summaries. [chunk_016]
| Initialization | Generate a population of random permutations. [chunk_001] [chunk_002] | No seed policy, duplicate-individual policy, or constructive/seeding strategy is fixed. [chunk_008] [chunk_016]
| Decoding | Process genes in permutation order and place each item with First Fit into the first feasible bin; open a new bin only if none fits. [chunk_001] [chunk_002] | A Best Fit decoder comparison is desired, but its interface and controlled comparison protocol are not finalized. [chunk_011]
| Feasibility | A valid permutation plus the constructive decoder produces a capacity-feasible packing; historical code also checked capacity, missing/extra IDs, and duplicates. [chunk_001] | Genetic operators still need invariant tests, especially for duplicate/missing genes and decimal capacity tolerance. [chunk_001] [chunk_003]
| Evaluation | Multiple incompatible objectives appear; see the fitness section below. [chunk_001] [chunk_002] [chunk_012] | One authoritative minimized/maximized definition must be selected and documented before convergence plots or comparisons are interpretable. [chunk_012] [chunk_016]
| Parent selection | Tournament selection is repeatedly proposed. [chunk_001] [chunk_002] | Two incompatible implementations are reported: sampling with replacement versus two disjoint groups from 10 unique individuals. [chunk_012]
| Crossover | A one-cut order-preserving duplicate-removal/reinsertion operator is shown. [chunk_001] [chunk_012] | It is not clearly standard OX1 or PMX despite plans naming those operators; either identify it precisely or replace it and test permutation validity. [chunk_001]
| Mutation | With probability `p_m`, swap two randomly selected permutation positions, then re-evaluate. [chunk_002] [chunk_012] | Early notebook code mutated the permutation without recomputing bins/fitness; later modular proposals re-evaluate. The actual code path needs verification. [chunk_001] [chunk_002]
| Repair | No separate packing repair is required after decoding a valid permutation. [chunk_001] | There is no documented chromosome repair for an invalid permutation; current crossover/mutation are expected to preserve validity but need tests. [chunk_001] [chunk_012]
| Local improvement | No implemented local-search or bin-level improvement step is established. [chunk_001] [chunk_016] | The word "hybrid" should not imply an unimplemented local improvement; the constructive decoder is the only established hybrid component. [chunk_001]
| Survivor selection / elitism | Generational replacement with elitism is proposed. [chunk_001] [chunk_002] | One version retains 10% elites and fills from offspring; another carries one elite; another combines old/new populations, keeps an elite fraction, then fills from offspring. These are not reconciled. [chunk_001] [chunk_002] [chunk_012]
| Termination | Stop after a fixed generation limit. [chunk_001] [chunk_002] | No stagnation criterion, target-optimum stop, evaluation budget, or rationale for the generation count is fixed. [chunk_002] [chunk_016]

## Fitness definitions recorded in the material

The summaries contain three related but non-identical formulas. They must not be silently merged. [chunk_001] [chunk_002] [chunk_012]

1. Falkenauer-style fullness score, described as maximized:

\[
F = \frac{1}{N}\sum_{i=1}^{N}\left(\frac{u_i}{C}\right)^k,
\qquad k>1,
\]

where `N` is the number of used bins and `u_i` is used capacity in bin `i`; examples `k=2` and `k=4` appear. [chunk_001] [chunk_002]

2. Original notebook cost, described as minimized:

\[
f_1 = 1-\frac{1}{N}\sum_{i=1}^{N}\left(\frac{u_i}{C}\right)^z,
\qquad z=2\text{ by default}.
\]

This reverses the direction of the fullness score, but its treatment of different `N` values must be analyzed rather than assumed equivalent across all packings. [chunk_001] [chunk_012]

3. Later modular proposal, described as minimized:

\[
f_2 = N-\frac{1}{N}\sum_{i=1}^{N}\left(\frac{u_i}{C}\right)^2.
\]

This explicitly makes fewer bins dominant and uses fullness as a same-bin-count refinement, but it is a proposed replacement rather than a repository-verified final objective. [chunk_002] [chunk_012]

The thesis must state the optimization direction, exponent, handling of `N`, and whether bin count is lexicographically dominant. Parameter ideas such as `k=3` or `k=4` were suggested but not tested in the summarized evidence. [chunk_011] [chunk_012]

## Selection, crossover, and mutation conflicts

One selection version samples five individuals with replacement and returns the two lowest-fitness candidates; because sampling is with replacement, the same individual can appear multiple times. [chunk_001] [chunk_012]

Another reported version samples ten unique individuals, splits them into two groups of five, and selects the best from each group, guaranteeing distinct parent objects when population size is at least ten. [chunk_012]

The shown crossover selects a cut, takes a prefix from one parent, adds non-duplicate genes from a portion of the other parent, and appends missing genes. Although it preserves a permutation if implemented correctly, the summaries explicitly say it is not clearly standard OX1 or PMX. [chunk_001] [chunk_012]

Swap mutation is the only consistently described mutation; inversion is mentioned as an option in the plan but not established as implemented. Mutation probabilities vary between an early notebook default of `0.8`, a proposal of `0.3`, and later experiment code using `0.2`. [chunk_001] [chunk_003] [chunk_004]

## Parameters and experimental protocol

| Context | Population | Generations | Mutation | Runs | Evidence status |
|---|---:|---:|---:|---:|---|
| Early notebook/default discussion | Not fixed in the algorithm summary; one attempted run used population 100 and 200 generations. [chunk_001] | 200 in the failed call. [chunk_001] | `0.8` in the shown mutation default. [chunk_001] | Not established. [chunk_001] | The run failed before producing convergence evidence because arguments were missing. [chunk_001]
| Initial modular examples | 50 [chunk_002] | 100 for `main.py`, 150 for triplet comparison. [chunk_002] | Not consistently stated in that example. [chunk_002] | One displayed outcome per instance. [chunk_002] | Proposed configuration, not a tuning study. [chunk_002]
| Stronger triplet proposal | 100 [chunk_003] | 500 [chunk_003] | `0.2` in code, while prose also mentioned `0.3`. [chunk_003] | Not repeated. [chunk_003] | The same five 21-bin outcomes were reported; seeds/times were absent. [chunk_003]
| Early batch proposal | 50 [chunk_004] | 100 [chunk_004] | `0.2` [chunk_004] | `RUNS_PER_INSTANCE=1`, but unused. [chunk_004] | Development experiment. [chunk_004]
| Quick/reduced runs | 40 [chunk_008] | 50 [chunk_008] | `0.2` [chunk_008] | `RUNS_PER_INSTANCE=1`, but unused. [chunk_008] | Explicitly reduced for speed and not justified as final thesis settings. [chunk_015] [chunk_016]
| Literature-inspired protocol | Not fixed locally. [chunk_003] | Not fixed locally. [chunk_003] | Not fixed locally. [chunk_003] | Ten runs per method/decoder in the cited Munien setup. [chunk_003] [chunk_006] | Source-derived guidance, not an adopted or implemented local protocol. [chunk_003]

No parameter-tuning design separates training/tuning instances from final evaluation instances. Random benchmark sampling and GA behavior are unseeded in the shown scripts, and repeated-run statistics are absent. [chunk_008] [chunk_016]

## Observed behavior

The first five reported `t60` runs used optimum/best-known 20; FFD returned 23,23,23,23,24 and GA returned 21 on all five. These were single displayed outcomes without seeds, elapsed times, packing layouts, or repeated-run distributions. [chunk_003]

Several 30-instance quick samples show mixed behavior: GA sometimes reaches the reference or improves on all displayed constructive heuristics, sometimes loses to FF/BF/FFD/BFD, and is consistently far slower than constructive heuristics in the shown timings. [chunk_011] [chunk_015] [chunk_016]

One reported run gave GA optimum-hit counts of 5/10 Easy, 6/10 Medium, and 0/10 Hard, with an overall mean signed gap of 1.5 bins; another sample derived from a later table had GA matching the listed optimum on 13/30 instances while at least one classical heuristic matched on 24/30. These are different unseeded samples/settings and should not be combined as one experiment. [chunk_012] [chunk_016]

On one Hard-set run, GA improved the common FF/FFD/BF/BFD/MR/MRD result by one bin in 9/10 cases but still missed the listed optimum by roughly 2-3 bins; on Easy examples, simple heuristics often matched the reference while GA did not. [chunk_011]

Displayed constructive-heuristic times were generally microseconds to milliseconds, while GA times ranged from fractions of a second to roughly 19 seconds in quick runs. These are single wall-clock readings without controlled hardware/protocol documentation. [chunk_008] [chunk_016]

Repeated `KeyboardInterrupt` events occurred while chromosomes were being evaluated through First Fit, including population initialization and crossover. They show practical slowness under the then-current settings, not a functional algorithm exception. [chunk_006] [chunk_007]

## Permutation GA versus Grouping GA

| Aspect | Permutation GA in this project | Falkenauer-style GGA as discussed |
|---|---|---|
| Gene meaning | One item identifier at each position; the chromosome is an ordering. [chunk_001] | A gene/group corresponds to a bin or item group rather than an item position. [chunk_001]
| Phenotype construction | First Fit decodes the permutation into bins. [chunk_002] | Operators act on groups and require group-aware insertion/repair rules. [chunk_001]
| Feasibility | A valid permutation plus constructive decoding naturally yields a feasible packing. [chunk_001] | Group crossover/mutation can require specialized handling of duplicated/unassigned items; exact rules were not resolved in the summaries. [chunk_001]
| Fitness emphasis | Competing proposals combine bin count and/or average powered fill ratio. [chunk_002] [chunk_012] | Falkenauer-style fullness score rewards fuller groups; exact source pages and complete GGA mechanics still need verification. [chunk_001]
| Implementation status | Proposed and experimentally exercised in Python, though current code details still need audit. [chunk_003] [chunk_016] | Discussed as a more complex literature alternative/future work; no local GGA implementation is established. [chunk_001]
| Thesis wording | May be described as a hybrid permutation GA with a constructive decoder if the method is documented precisely. [chunk_001] | Must not be claimed as implemented unless group representation and group-aware operators are actually built and validated. [chunk_001]

## Unresolved design choices before final experiments

1. Select and document one fitness function, optimization direction, exponent, and tie behavior; ensure convergence plots use that same scale. [chunk_012] [chunk_016]
2. Decide whether the thesis evaluates GA+FF only or matched GA+FF and GA+BF variants with identical initial populations, seeds, parameters, budgets, and instances. [chunk_011]
3. Standardize tournament sampling, parent distinctness, crossover identity, elitism, offspring population sizing, and re-evaluation after mutation. [chunk_001] [chunk_012]
4. Add focused invariant tests for permutation completeness/uniqueness, decoded capacity feasibility, stable fitness after mutation, and odd population sizes. [chunk_001]
5. Fix a reproducible protocol: benchmark manifest or seed, multiple independent GA runs, recorded seeds, stopping rule, best/mean/median/std, optimum-hit rate, relative and absolute gaps, and timing environment. [chunk_003] [chunk_016]
6. Decide whether decoder output is a list of item IDs or `(item_id, item_size)` pairs; visualization drafts assume both contracts. [chunk_012]
7. Treat bin visualization and per-instance convergence plots as either documented thesis figures, selected diagnostics, or optional artifacts; current comments and implementation disagree about generating them for every instance. [chunk_012] [chunk_016]
8. Validate reference labels so an open/best-known value is not called an optimum and missing references never become zero gap. [chunk_003] [chunk_016]
