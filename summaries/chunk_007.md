## Important thesis facts

- **Confirmed context:** The experiment compares nine methods for one-dimensional bin packing: FF, FFD, BF, BFD, NF, NFD, MR, MRD, and a genetic algorithm (GA). [chunk_007]
- **Confirmed context:** Benchmark instances are drawn from Scholl, Hard28, and Falkenauer data found under `project/data`; known optima are loaded through `SolutionManager`, whose run-time message reports 6,195 solutions loaded from Excel. [chunk_007]
- **Confirmed observed dataset distribution:** Runs reported 880 Easy, 508 Medium, and 10 Hard instances, with 10 randomly selected from each category (30 total). [chunk_007]
- **Uncertain/proposed classification:** The shown script classifies instances solely by bin capacity: Easy for capacity below 1,000, Medium for 1,000 through 99,999, and Hard for at least 100,000. A comment attributes this grouping to "Munien 2020," but the chunk gives no bibliographic evidence and observed Falkenauer `t` instances were labeled Easy despite an earlier comment assigning Falkenauer T to Medium. [chunk_007]

## Decisions and rationale

- **User-decided:** Preserve the earlier compact, single-line console table because the user finds it clearer and has enough screen width for a very wide table. [chunk_007]
- **User-decided:** Display every execution time as its own console column - `T_FF`, `T_FFD`, `T_BF`, `T_BFD`, `T_NF`, `T_NFD`, `T_MR`, `T_MRD`, and `T_GA` - rather than showing only `T_FFD` and `T_GA` or embedding times in parentheses beside results. The rationale is easier direct comparison by column. [chunk_007]
- **User-decided:** Do not format result and time as `value(time)`; bin counts and times must remain separate columns. [chunk_007]
- **Proposed by assistant, not confirmed as final:** Replace CSV/Markdown output with `project/results/experiment_results.xlsx` plus a readable `project/results/experiment_results.txt`, and place plots under `project/results/plots/`. [chunk_007]
- **Proposed by assistant, not explicitly approved:** Reduce GA population from 50 to 40 and generations from 100 to 50 for faster trial runs, with the suggestion that final thesis parameters could later be restored. This conflicts with preserving experiment parameters unless explicitly changed and should not be treated as a settled thesis setting. [chunk_007]

## Algorithms/formulas

- **Confirmed code behavior:** Each basic heuristic runs on original item-key order; its descending variant first sorts keys by item size descending. Thus FFD, BFD, NFD, and MRD are implemented as descending-order calls to FF, BF, NF, and MR respectively. [chunk_007]
- **Confirmed code behavior:** `solve_heuristic` measures wall-clock duration using `time.time()` and returns `(number_of_bins, duration)`. [chunk_007]
- **Confirmed code behavior:** GA is instantiated as `GeneticAlgorithm(items, capacity, pop_size=POP_SIZE, generations=GENERATIONS, mutation_prob=0.2)` and its result is `best_sol.num_bins`. [chunk_007]
- **Confirmed formula:** The GA absolute gap is calculated as `GA bins - optimal bins`; proposed code uses zero when no optimum is available, while an earlier version used `"N/A"`, so missing-optimum handling is unsettled. [chunk_007]
- **Proposed plotting formulas:** For every method `h`, compute `Gap_h = result_h - Optimal`; aggregate mean gaps and mean run times by category, and use a logarithmic y-axis for time because GA is much slower than the heuristics. [chunk_007]

## Implementation details

- **Proposed code:** `run_experiments.py` recursively scans all `.txt` files below `project/data`, parses every file with `parse_instance_file`, and adds `_folder` and `_file` metadata to each parsed instance. [chunk_007]
- **Proposed code:** The script randomly samples up to `SAMPLES_PER_FOLDER = 10` instances per Easy/Medium/Hard category without setting a random seed; repeated runs therefore need not use the same instances. [chunk_007]
- **Proposed code:** Results are accumulated as dictionaries with metadata, result, and timing columns, converted to a Pandas DataFrame, and written with `df.to_excel(output_xlsx, index=False)`; `pandas` and `openpyxl` were stated to be installed, but no installation evidence appears in this chunk. [chunk_007]
- **Proposed result schema:** `Category`, `Dataset`, `Instance`, `Items`, `Capacity`, `Optimal`, result/time pairs for all eight heuristics, `GA`, `GA_Time`, and `Gap_GA`. [chunk_007]
- **Proposed pipeline:** `plot_results.py` reads `project/results/experiment_results.xlsx`, calculates all method gaps, and writes `comparison_gap.png` and `comparison_time.png` under `project/results/plots/`. [chunk_007]
- **Unresolved implementation mismatch:** The latest shown console code still prints combined `FF(Time)`-style cells, whereas the final user request requires distinct result columns followed by distinct time columns. No final code satisfying that request appears in this chunk. [chunk_007]
- **Reliability concern:** Excel is written only after the entire loop completes, while the text log is flushed after each instance. A manual interruption therefore appears likely to lose the accumulated Excel rows even though partial text output may survive. [chunk_007]
- **Unused setting:** `RUNS_PER_INSTANCE = 1` is declared in the proposed scripts but not used to control repeated GA runs. [chunk_007]

## Experiments/results

- **Observed output, partial only:** Several attempted 30-instance runs were manually interrupted during GA execution, so none is evidence of a completed experiment set or final aggregate thesis result. [chunk_007]
- **Observed output:** GA time grew substantially on larger Easy instances: examples include 0.24 s for optimum/result 27/27, 2.57 s for 122/123, 10.94 s for 201/208, 11.19 s for Falkenauer U500 optimum/result 207/215, and an earlier run showed 45.56 s for optimum/result 359/361. These are single stochastic observations, not stable averages. [chunk_007]
- **Observed output:** In the longest displayed partial run, many FF/BF variants matched known optima, NF/NFD often used considerably more bins, and GA gaps ranged from 0 to 8 among the shown instances. The sample is incomplete and randomly selected, so no general performance conclusion is justified. [chunk_007]
- **Observed output:** One displayed Falkenauer instance showed ordering-sensitive behavior: `Falkenauer_u500_06.txt` produced FF 220 versus FFD 210, BF 217 versus BFD 210, NF 273 versus NFD 292, MR 235 versus MRD 210, GA 215, and optimum 207. [chunk_007]
- **Observed failure mode:** All reported terminations were `KeyboardInterrupt` raised while GA-created chromosomes were being evaluated via `first_fit`, including during population initialization or crossover. This demonstrates slow execution at the point of interruption, but it is not evidence of a functional exception in the algorithm. [chunk_007]

## Sources/references

- **Internal data source:** `project/data/Solutions.xlsx` is the stated source of known optimal values through `SolutionManager`. [chunk_007]
- **Internal benchmark sources:** Scholl, Hard28, and Falkenauer instance files are referenced by dataset/folder and file names, but the chunk provides no formal citations or provenance records for them. [chunk_007]
- **Unverified reference:** "Munien 2020" appears only in a code comment supporting Easy/Medium/Hard categories; no title, authorship details, page, DOI, or quoted definition is supplied, so it must be verified before use in the thesis. [chunk_007]

## Rejected approaches

- **Rejected by user:** Multi-line console output with a GA summary line followed by heuristic detail lines; the user preferred the earlier single-line table. [chunk_007]
- **Rejected by user:** Showing only `T_FFD` and `T_GA` in the console. [chunk_007]
- **Rejected by user:** Compact `value(time)` formatting such as `113(0.0012s)` and headings such as `FF(Time)`; times must be separate columns. [chunk_007]
- **Superseded proposal:** CSV plus Markdown result files were proposed initially, then replaced in later proposals by Excel plus plain text. [chunk_007]

## Unresolved questions

- What exact final console widths, precision, and ordering should be used for the separate `T_FF` through `T_GA` columns? The required column identities are clear, but the chunk ends before an implementation is shown. [chunk_007]
- Should GA remain at the original population 50 and 100 generations, or use the assistant-proposed 40 and 50? No explicit user decision authorizes changing these thesis experiment parameters. [chunk_007]
- How many independent GA runs per instance are required, and how should stochastic results be summarized? `RUNS_PER_INSTANCE` exists but is unused, and all shown results appear to be single runs. [chunk_007]
- Should sampling be reproducible through a fixed random seed, and should the exact sampled instance list be recorded for thesis repeatability? [chunk_007]
- Is capacity-only Easy/Medium/Hard categorization valid for all included benchmark families, especially Falkenauer T, given the inconsistency between the comment and observed labels? [chunk_007]
- Should partial results be checkpointed to Excel after each instance so manual interruption does not discard accumulated structured data? [chunk_007]
- How should missing known optima be represented and excluded from gap statistics: zero, `N/A`, or missing data? [chunk_007]
- Is GA performance to be optimized, profiled, or simply allowed to complete? The repeated interruptions establish practical slowness but do not diagnose its cause beyond frequent `first_fit` evaluations. [chunk_007]
