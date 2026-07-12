# Master Thesis Plan: Solving One-Dimensional Bin Packing Problem using Genetic Algorithms

## 1. Introduction
- **Problem Description**: Define the One-Dimensional Bin Packing Problem (1D-BPP).
  - Goal: Minimize number of bins used for a set of items with specific weights.
  - Constraints: Bin capacity $C$.
  - Complexity: NP-Hard.
- **Motivation**:
  - Practical applications (logistics, cutting stock, memory allocation).
  - Why Genetic Algorithms? (Global search capability vs local greedy heuristics).
- **Thesis Goal**:
  - Implement a Permutation-based Genetic Algorithm (GA).
  - Hybridize it with the First Fit (FF) heuristic.
  - Compare performance against classical heuristics (FF, BF, NF, Max-Rest, and their decreasing variants FFD, NFD, BFD) and literature benchmarks (Falkenauer).

## 2. Theoretical Background
- **Classical Heuristics** (based on `1Dbin/README.md`):
  - **First Fit (FF)**: Place item in the first bin that fits.
  - **Best Fit (BF)**: Place item in the bin with min residual space.
  - **Next Fit (NF)**: Place item in the current open bin if it fits; otherwise close it and open a new bin. Only ever checks the single most recently opened bin.
  - **Max-Rest / Worst Fit (MR)**: Place item in the bin with the *maximum* residual space (if it fits at all).
  - **Decreasing Variants (FFD, BFD, NFD)**: Sort items $size_{desc}$ before packing. Strong performance on uniform data.
- **Metaheuristics**:
  - Overview of Evolutionary Computation.
  - **Grouping GA (GGA)**: Discuss Falkenauer's approach (group-based encoding) as the "heavyweight" alternative (referencing `binpacking-genetic-algorithm/`).
  - **Ant Colony Optimization (ACO)**: Discuss Rajacic's work as a comparable hybrid approach.

## 3. Methodology (The Proposed Algorithm)
- **Algorithm Architecture**: **Hybrid Genetic Algorithm**.
  - **Encoding**: Permutation Encoding (Chromosome = list of Item IDs).
  - **Decoder**: **First Fit Heuristic**.
    - *Crucial difference*: The GA evolves the *order*, the Decoder handles the *packing*.
    - This allows the GA to search for item orderings that lead the First-Fit decoder toward near-optimal packings (e.g., presenting large items together with the complementary small items that fill the same bin).
- **Genetic Operators**:
  - **Selection**: Tournament Selection ($k=2$ or $k=5$).
  - **Crossover**: Order Crossover (OX1) or Partially Mapped Crossover (PMX) to respect permutation constraints.
  - **Mutation**: Swap Mutation (exchange two items) or Inversion.
  - **Fitness Function**: Falkenauer's $k$-power objective function ($F = \sum (fill\_ratio)^k / N$).
    - Favors full bins over half-full bins, guiding the search better than just "number of bins".
- **Initialization (Heuristic Seeding)**: the initial population is not purely random. It is seeded with the packings produced by the classical heuristics — the natural (unsorted) First-Fit order, the First-Fit-Decreasing order, and a Best-Fit-Decreasing grouping — with the remainder generated randomly.
  - Combined with elitism, this **guarantees the GA can never return a solution worse than the best of its seed heuristics**; evolution can only improve on them. This is the standard hybrid/memetic-GA construction (cf. Falkenauer 1996, Reeves 1996).
  - The unsorted First-Fit order is included as a seed specifically because on triplet (Falkenauer *T*) instances, size-sorting *degrades* the packing (FFD uses more bins than plain FF), so seeding FFD alone would not guarantee dominating plain First-Fit.

## 4. Implementation details
- **Language**: Python (Jupyter Notebook).
- **Data Structures**:
  - Chromosome class.
  - Visualization using Matplotlib (already implemented).
- **Modification**: Upgrading `construct_bins` from Next Fit to First Fit.

## 5. Experimental Results
- **Full Heuristic Suite Tested**: FF, BF, NF, MR (Max-Rest), plus their decreasing variants FFD, BFD, NFD, MRD, and engineered lookup/priority-queue implementations (FFL, BFL, MR+) used purely for runtime efficiency at scale — same algorithms as above, not additional baselines.
- **Datasets**:
  - **Uniform**: `u120`, `u250` (Standard tests).
  - **Triplets**: `t60`, `t120` (Hard tests where FFD fails).
- **Metrics**:
  - Optimal Gap % (Distance from lower bound).
  - Convergence Speed (Generations to best solution).
  - Comparison table:
    | Instance | FFD (Heuristic) | Permutation GA (This Work) | GGA (Literature) |
    | :--- | :--- | :--- | :--- |
    | u120_01 | 49 | 48 | 48 |
    | t60_01  | 22 | 20 | 20 |

## 6. Conclusion
- The heuristic-seeded Permutation GA + First-Fit decoder is, by construction (seeding + elitism), guaranteed never to use more bins than the best of the classical heuristics it is seeded with — so it **dominates** First-Fit, FFD, and BFD rather than merely competing with them.
- On the validation instances tested so far, it matched plain First-Fit on the hard triplet instances (where First-Fit is already near-optimal — both reached the optimum) and improved on First-Fit on the uniform instances, reaching or coming within one bin of the optimum. *(Full-benchmark results across all instance sets still to be run to confirm these trends.)*
- The trade-off is runtime: the classical heuristics run in milliseconds, whereas the population-based GA takes on the order of seconds to a minute per instance. The GA's contribution is therefore **solution quality on harder instances, not speed** — an inherent property of any population metaheuristic, not a defect of this implementation.
- It is simpler to implement than a full Grouping GA (GGA) while, through seeding, still guaranteeing heuristic-dominant results.

## 7. References
- Falkenauer, E. (1996). *A hybrid grouping genetic algorithm for bin packing*. Journal of Heuristics, 2(1), 5–30.
- Rajacic, J. (2013). *Rešavanje jednodimenzionog problema pakovanja kombinovanjem optimizacionih metoda*.
- Munien, C. et al. (2020). *Metaheuristic Approaches for One-Dimensional Bin Packing Problem*.
- Scholl, A., Klein, R., & Jürgens, C. (1997). *BISON: A fast hybrid procedure for exactly solving the one-dimensional bin packing problem*. Computers & Operations Research, 24(7), 627–645.
- Delorme, M., Iori, M., & Martello, S. (2018). *BPPLIB: A library for bin packing and cutting stock problems*. Optimization Letters, 12(2), 235–250. (Source of the Falkenauer, Scholl, Wäscher, and Schoenfield benchmark instances and solutions used in this thesis.)
- Wäscher, G., & Gau, T. (1996). *Heuristics for the integer one-dimensional cutting stock problem: a computational study*. OR Spectrum, 18(3), 131–144.
- Schoenfield, J. E. (2002). *Fast, exact solution of open bin packing problems without linear programming*. Technical report, US Army Space and Missile Defense Command, Huntsville, Alabama, USA.
- Martello, S., & Toth, P. (1990). *Knapsack Problems: Algorithms and Computer Implementations*. John Wiley & Sons, Chichester.
