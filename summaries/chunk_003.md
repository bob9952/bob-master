## Important thesis facts

- The thesis concerns one-dimensional bin packing: pack all items of weights \(w_j\) into the minimum number of identical bins of capacity \(c\), with no bin exceeding capacity; the related cutting-stock problem uses item types and demands and can be transformed to or from a BPP instance. [chunk_003]
- The user has Falkenauer `binpack1`-`binpack8`, Scholl sets 1-3, Hard28, and BPPLIB's `Solutions.xlsx`, and wants instance ingestion organized before implementing further genetic-algorithm variants. [chunk_003]
- Falkenauer U consists of 80 uniform instances with \(n=120,250,500,1000\), 20 instances at each size, item weights in `[20,100]`, and capacity 150; Falkenauer T consists of 80 triplet instances in which an optimal packing groups one large and two small items, with \(n\) from 60 to 501. [chunk_003]
- The supplied local `binpack5.txt` evidence uses decimal-scaled triplet data such as capacity `100.0` and item weights such as `36.6` and `26.8`, although the quoted BPPLIB description states Falkenauer T capacity 1000; this scaling discrepancy needs explicit documentation. [chunk_003]
- Scholl set 1 contains 720 instances across \(n\in\{50,100,200,500\}\), \(c\in\{100,120,150\}\), and three uniform weight ranges; set 2 contains 480 instances with capacity 1000 and designed averages of 3, 5, 7, or 9 items per bin; set 3 contains 10 difficult instances with \(n=200\), capacity 100,000, and weights in `[20,000,35,000]`. [chunk_003]
- The quoted Scholl/BISON paper says the three Scholl sets total 1,210 instances, with an optimum known for 1,184 at that time; specifically 704/720, 477/480, and 3/10 were solved for sets 1, 2, and 3. [chunk_003]
- Hard28 is attributed by BPPLIB to J. E. Schoenfield and contains 28 instances with 160-200 items, capacity 1000, and weights reported as `[1,800]`. [chunk_003]
- BPPLIB's workbook reportedly covers 6,195 instances and stores, per category sheet, `Name`, `Best LB`, `Best UB`, `Status`, optional `Comment`, and `Selected`; `Solved` means LB equals UB, while `Open` means they differ. [chunk_003]

## Decisions and rationale

- User preference: mirror BPPLIB's modular dataset organization, including `1_Falkenauer`, `2_Scholl`, and a Hard28/Schoenfield area, so datasets and their provenance remain clear. [chunk_003]
- User preference: use the official `Solutions.xlsx` copied into the project's data folder, making the experiment project self-contained instead of relying on a machine-specific absolute BPPLIB path. [chunk_003]
- Proposed design: normalize Falkenauer embedded names such as `u120_00` to workbook keys such as `Falkenauer_u120_00.txt`, while preserving ordinary filenames for one-instance BPPLIB files. [chunk_003]
- Proposed design: separate instance parsing from solution metadata lookup because Falkenauer aggregate files include a best-known value in their headers, whereas Scholl/Hard28 single-instance files contain only item count, capacity, and weights. [chunk_003]
- Proposed experimental practice from the quoted Munien 2020 methodology: select varied instances across easy, medium, and hard categories and run each metaheuristic/underlying-heuristic combination 10 times; this is source-derived guidance, not yet a confirmed local protocol. [chunk_003]
- The assistant proposed stronger GA settings (`pop_size=100`, `generations=500`, `mutation_prob=0.2`) after the first fast triplet run, but earlier prose also suggested mutation 0.3; the code proposal settled on 0.2 without a documented tuning study. [chunk_003]

## Algorithms/formulas

- First Fit places each item in the first existing bin satisfying `used + item_size <= capacity`; First Fit Decreasing (FFD) first sorts item identifiers by descending weight and then applies First Fit. [chunk_003]
- For decimal-valued instances, the proposed feasibility comparison is `used + item_size <= capacity + EPSILON` with `EPSILON = 1e-6`, preventing harmless binary floating-point error from rejecting a mathematically exact fit. [chunk_003]
- The reported GA quality measure is absolute bin gap, `GA bins - best known/optimal bins`; the Scholl paper also defines absolute deviation as \(|x-y|\) and relative deviation as \(|x-y|/y\times100\%\). [chunk_003]
- Assistant interpretation, not demonstrated diagnosis: the GA's 21-bin triplet solutions may be local optima because reaching 20 requires exact large-plus-two-small triplets, and a missed grouping can create spillover. [chunk_003]
- Referenced comparison context includes GA, Firefly Algorithm, Firefly Hybrid, Adaptive Cuckoo Search, Cuckoo Search-GA Hybrid, and Artificial Bee Colony, each tested with best-fit and better-fit decoding in the quoted Munien study. [chunk_003]

## Implementation details

- Confirmed failure evidence: the original Falkenauer parser attempted `int(parts[0])` and failed on triplet metadata `100.0 60 20`; capacity and item values therefore need decimal parsing, while item count and best-known bin count remain integers. [chunk_003]
- Proposed parser contract returns dictionaries containing `name`, `capacity`, `num_items`, `best_known`, and an `items_dict` keyed from 1; Falkenauer aggregate parsing reads the number of problems, then name, `capacity count best-known`, and exactly `count` item lines. [chunk_003]
- Proposed universal format detection treats a numeric first line followed by a nonnumeric second line as a Falkenauer multi-instance file; otherwise it treats the file as a single BPP instance with line 1 item count, line 2 capacity, and remaining lines item weights. [chunk_003]
- The proposed single-instance parser sets `best_known=None` and uses the file basename as the instance name, leaving bounds/status lookup to a separate solution manager. [chunk_003]
- Proposed `SolutionManager` reads every Excel sheet with `pandas.read_excel(..., sheet_name=None, engine='openpyxl')`, records rows containing `Name` and `Best UB`, and supports exact names or appending `.txt`. [chunk_003]
- The assistant claimed edits to `parser.py`, `heuristic.py`, `comparison.py`, `run_scholl.py`, and `solution_manager.py`, plus a copied Scholl file, but the chunk contains no repository inspection or diff proving those mutations; treat these as historical assistant claims, not verified implementation state. [chunk_003]
- The workbook path shown once as `~$Solutions.xlsx` is an Excel lock/temporary filename, while later proposals use `Solutions.xlsx`; code should target the real workbook, not the `~$` file. [chunk_003]

## Experiments/results

- Confirmed console output for the first five `binpack5.txt` triplet instances: optimum/best-known was 20 for every instance; FFD used 23 bins for `t60_00` through `t60_03` and 24 for `t60_04`; the GA used 21 for all five, yielding gap 1. [chunk_003]
- The same five results were reported again after the proposed stronger settings, so that run did not improve any instance to 20; no elapsed times, seeds, per-run distributions, or packing contents were reported. [chunk_003]
- On these five observations, GA beat FFD by 2 bins on four instances and 3 bins on one, but the assistant's claim that this alone is thesis-conclusion-worthy is an overstatement without repeated-run statistics and broader sampling. [chunk_003]
- A later `run_scholl.py` attempt failed before solving anything because `project/data/N1W1B2R1.txt` was not found; therefore no Scholl GA result is confirmed in this chunk. [chunk_003]
- The user states `N1W1B2R1` has best known 17, and workbook examples include `N1C1W1_A.txt` with LB=UB=25 and status `Solved`; these are supplied metadata examples, not locally verified workbook reads in this chunk. [chunk_003]

## Sources/references

- Primary benchmark citation requested by BPPLIB: M. Delorme, M. Iori, and S. Martello, “BPPLIB: A library for bin packing and cutting stock problems,” *Optimization Letters*, 12(2):235-250, 2018. [chunk_003]
- General survey cited by BPPLIB: M. Delorme, M. Iori, and S. Martello, “Bin Packing and Cutting Stock Problems: Mathematical Models and Exact Algorithms,” *European Journal of Operational Research*, 255(1):1-20, 2016. [chunk_003]
- Falkenauer benchmark source: E. Falkenauer, “A hybrid grouping genetic algorithm for bin packing,” *Journal of Heuristics*, 2(1):5-30, 1996. [chunk_003]
- Scholl benchmark/source: A. Scholl, R. Klein, and C. Jürgens, “Bison: a fast hybrid procedure for exactly solving the one-dimensional bin packing problem,” *Computers & Operations Research*, 24(7):627-645, 1997. [chunk_003]
- Hard28 source as quoted by BPPLIB: J. E. Schoenfield, “Fast, exact solution of open bin packing problems without linear programming,” technical report, US Army Space and Missile Defense Command, 2002. [chunk_003]
- The user identifies `munien2020.pdf` page 12 as the intended model for dataset selection and repeated evaluation; full bibliographic metadata is absent from this chunk. [chunk_003]
- Using BPPLIB benchmark files and bounds in a thesis requires citation and clear attribution; the chunk supports citing BPPLIB for the library, but original dataset papers should also be cited when describing their construction or historical results. [chunk_003]

## Rejected approaches

- The initial integer-only parser was rejected after it failed on decimal Falkenauer triplet capacity and weights. [chunk_003]
- A hand-maintained `solutions.csv` and hard-coded fallback optimums were proposed, then superseded when the user confirmed `pandas` and `openpyxl` were installed and requested direct use of the official workbook. [chunk_003]
- Hard-coded absolute access to `D:\in5\master\BPPLIB\...\Solutions.xlsx` was rejected in favor of copying the workbook under project data for portability. [chunk_003]
- Treating all benchmark files as having one identical physical format was rejected: the unified interface still needs distinct readers for Falkenauer aggregate files and BPPLIB single-instance files. [chunk_003]

## Unresolved questions

- The actual current repository state is unknown because claimed file edits and copies were not verified; inspect code and data before relying on the proposed parser, epsilon logic, workbook loader, or runners. [chunk_003]
- Decide whether decimal Falkenauer T values are merely values scaled by 0.1 from BPPLIB integers and whether epsilon arithmetic or exact rescaling to integers is preferable for reproducibility. [chunk_003]
- The solution manager must retain `Best LB`, `Best UB`, and `Status`, not label every `Best UB` as “optimal”; only rows with `Status=Solved` or LB=UB establish an optimum, while open rows provide bounds. [chunk_003]
- Validate workbook sheet names, column types, duplicate instance names across sheets, total loaded count, and correct name normalization against the actual non-temporary `Solutions.xlsx`. [chunk_003]
- Define the final benchmark sampling, number of independent runs, random seeds, stopping rules, timing method, output of actual bin assignments, and statistical summaries before drawing thesis conclusions. [chunk_003]
- Clarify whether the intended GA must reproduce the method from `munien2020.pdf` or retain the user's current, different GA; the referenced C example is intended mainly as inspiration for printing solutions and timing. [chunk_003]
