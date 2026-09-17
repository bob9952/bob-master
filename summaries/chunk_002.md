## Important thesis facts

- The thesis concerns one-dimensional bin packing: assign (n) items of weights (w_j) to the minimum number of identical bins of capacity (c), without exceeding capacity in any bin. [chunk_002]
- BPPLIB is presented as the benchmark library maintained by Delorme, Iori, and Martello; its BPP single-instance format is item count, bin capacity, then one weight per item, while its solution workbook supplies best lower bound (LB), best upper bound (UB), and status. [chunk_002]
- An instance is proven solved when `Best LB = Best UB`; that common value is the optimal bin count. The pasted BPPLIB solution table marks all listed Falkenauer U and T instances as solved. [chunk_002]
- Falkenauer has two 80-instance classes: U has uniformly distributed sizes, (n=120\ldots1000), and BPPLIB capacity 150; T consists of constructed triplets, (n=60\ldots501), and BPPLIB capacity 1000. [chunk_002]
- The original OR-Library distribution uses eight multi-instance files: `binpack1`-`binpack4` for uniform cases and `binpack5`-`binpack8` for triplets. Each instance records identifier, capacity, item count, current best-known bin count, and its item sizes. [chunk_002]
- The original triplet description uses item sizes 25-50 and capacity 100, whereas the BPPLIB description uses capacity 1000; the chunk does not explain whether BPPLIB scales the original data. [chunk_002]
- Falkenauer T instances were constructed with guaranteed optimum (n/3), exactly three items per bin; the idea of such instances was first suggested to Falkenauer by Andre van Vliet. [chunk_002]
- In the original uniform files, Falkenauer's reported best-known count was also the proven optimum except for `u120_08`, `u120_19`, `u250_07`, `u250_12`, and `u250_13`; the later BPPLIB table shown in the conversation reports solved LB=UB values for the listed U instances, so historical “best known” and current proven optimum must be labeled separately. [chunk_002]
- The user chose Python, citing faster and easier implementation than C++, and specified the existing Anaconda environment `ai`. [chunk_002]

## Decisions and rationale

- The user decided to start from the original Falkenauer text files because their provenance and embedded best-known values are understandable and can guide implementation, project structure, and thesis writing. [chunk_002]
- The agreed project direction was a permutation-based GA decoded by First Fit, benchmarked against First Fit Decreasing (FFD) and the embedded/reference optimum. [chunk_002]
- The proposed structure separates `data/`, `src/parser.py`, `src/chromosome.py`, `src/ga.py`, `src/heuristic.py`, `main.py`, and `comparison.py` to keep parsing, representation, search, heuristics, and experiment entry points distinct. [chunk_002]
- Initial experiments were proposed on U instances (`binpack1`) and T instances (`binpack5`), with triplets treated as the main hard-case comparison; this was a plan, not a validated thesis result. [chunk_002]
- The assistant first suggested deriving T optima as (n/3), then corrected the provenance point after the user showed that the original files explicitly include the current best-known count and document the constructed optimum. [chunk_002]

## Algorithms/formulas

- Representation: a chromosome is a permutation of item IDs; phenotype decoding processes that order with First Fit, placing each item in the first feasible existing bin or opening a new bin. [chunk_002]
- Baseline FFD sorts item IDs by nonincreasing weight and applies the same First Fit packing procedure. [chunk_002]
- Falkenauer's proposed fill-quality metric is (rac{1}{N}\sum_{i=1}^{N}(fill_i/C)^k), with (k>1) (examples (k=2) or (4)); fuller bins receive disproportionate reward. [chunk_002]
- The notebook version minimized (1-\frac{1}{N}\sum_i(fill_i/C)^z); the later modular proposal instead minimized (N-\frac{1}{N}\sum_i(fill_i/C)^2), making fewer bins dominant and fill quality a same-bin-count tie-breaker. [chunk_002]
- Proposed GA operators were tournament selection (shown with two tournaments of size 5), a one-cut order-preserving crossover that removes duplicates, swap mutation, and generational replacement with elitism. [chunk_002]
- For triplet instances, the guaranteed optimum is (OPT=n/3), giving 20, 40, 83, and 167 bins for (n=60,120,249,501), matching the pasted BPPLIB LB/UB table. [chunk_002]

## Implementation details

- The original notebook parser reads BPPLIB split single-instance files as line 0 item count, line 1 capacity, and subsequent lines item sizes; those split files do not embed best-known values. [chunk_002]
- The proposed original-format parser strips blank lines, reads the first value as number of problems, then for each problem reads its name, assumes the next line contains three whitespace-separated metadata values (`capacity`, `num_items`, `best_known`), and reads `num_items` weights into a 1-based `items_dict`. [chunk_002]
- The proposed `first_fit` returns bins shaped as `{'used': int, 'items': [(id, size), ...]}`. [chunk_002]
- The proposed `Chromosome` evaluates immediately, stores decoded bins and cost, exposes `num_bins`, and reevaluates after swap mutation. [chunk_002]
- The proposed `GeneticAlgorithm` initializes random permutations, selects parents by tournament, clones or crosses them, mutates children, carries one elite, records best/average fitness history, and returns the best chromosome. [chunk_002]
- `main.py` was proposed to run the first five `binpack1` instances with population 50 and 100 generations; `comparison.py` was proposed to run the first five `binpack5` instances with population 50 and 150 generations and print optimal, FFD, GA, and GA gap. [chunk_002]
- Cursor claimed the modular files had been created, but the chunk provides no successful file inspection or test run confirming their exact on-disk contents; the final user execution instead exposed a parser failure. [chunk_002]
- Earlier notebook code has defects visible in the transcript: `main_loop` was called without its required `instance_name`, and its status print labeled `best_chromosome.bin_size` as “best bins count” instead of printing the number of bins. [chunk_002]

## Experiments/results

- The only demonstrated notebook result loaded five previously saved outputs and reported feasible packings using 27, 29, 457, 23, and 13 bins for instances `1`-`5`; no optimum/baseline comparison is supplied, so these do not establish GA quality. [chunk_002]
- A notebook run failed with `TypeError: main_loop() missing 1 required positional argument: 'num_generations'` because the call omitted the leading `instance_name` argument. [chunk_002]
- The assistant predicted that FFD would often use about 22 bins on `t60` while the GA would reach 20, and even displayed a sample table with such values, but explicitly lacked a working Python run; these values are predictions/examples, not measured results. [chunk_002]
- The user's actual `python comparison.py` run ended with `Error reading metadata for problem t60_00` followed by `No instances found. Check data directory.`; therefore no current FFD or GA benchmark result was produced. [chunk_002]

## Sources/references

- Primary benchmark/algorithm source: E. Falkenauer, “A Hybrid Grouping Genetic Algorithm for Bin Packing,” cited in the original distribution as a 1994 CRIF working paper and by BPPLIB as *Journal of Heuristics* 2(1):5-30, 1996. [chunk_002]
- BPPLIB citation requested by its README: M. Delorme, M. Iori, and S. Martello, “BPPLIB: A library for bin packing and cutting stock problems,” *Optimization Letters* 12(2):235-250, 2018. [chunk_002]
- Survey/exact-method reference highlighted by BPPLIB: M. Delorme, M. Iori, and S. Martello, “Bin Packing and Cutting Stock Problems: Mathematical Models and Exact Algorithms,” *European Journal of Operational Research* 255(1):1-20, 2016. [chunk_002]
- Benchmark provenance also includes the OR-Library distribution and its format note for Falkenauer's `binpack1`-`binpack8` files. [chunk_002]
- Other BPPLIB benchmark families mentioned for possible context are Scholl, Waescher, Schwerin, Hard28, randomly generated, ANI/AI, and GI, but no decision was made to include them in the thesis experiments. [chunk_002]

## Rejected approaches

- Using only BPPLIB's split files plus manual (n/3) calculation or a separate Excel lookup was displaced by the user's preference for the original multi-instance files, which embed the historical best-known value and document its meaning. [chunk_002]
- Continuing implementation solely inside `GA-1D-BPP.ipynb` was rejected in favor of a modular `project/` directory. [chunk_002]
- C++ was rejected for this project in favor of Python because the user expects faster, easier development. [chunk_002]
- Treating the assistant's displayed `t60` comparison table as evidence is rejected: it was a forecast/example generated without a successful execution. [chunk_002]

## Unresolved questions

- The actual line/token layout of the user's `binpack5.txt` must be inspected; the parser's assumption that capacity, item count, and best-known value share one line is inconsistent with the observed metadata parse error. [chunk_002]
- It remains to determine whether the file uses separate metadata lines, unexpected delimiters/encoding, or another variant, and then update the parser with strict count validation rather than silently returning no instances. [chunk_002]
- No successful run has yet established FFD or GA performance on any Falkenauer triplet instance, so the central claim that this GA beats FFD remains untested. [chunk_002]
- The experiment protocol is incomplete: random seeds, number of independent runs, stopping criteria, parameter grid, runtime reporting, success rate, mean/variance, and statistical comparison are not defined. [chunk_002]
- It is unresolved whether the final thesis should report the original files' historical best-known values, BPPLIB's later proven LB=UB optima, or both with dates/provenance; for the five named U exceptions, this distinction is essential. [chunk_002]
- The capacity scaling difference between original triplets (100) and BPPLIB triplets (1000) needs verification before mixing datasets or results. [chunk_002]
- The proposed fitness, crossover, mutation rate, and elitism need validation against the intended Falkenauer method; the current proposal is a permutation GA with First Fit, not necessarily a faithful implementation of Falkenauer's grouping GA. [chunk_002]
