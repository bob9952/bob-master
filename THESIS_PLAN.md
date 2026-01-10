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
  - Compare performance against classical heuristics (FFD, BFD) and literature benchmarks (Falkenauer).

## 2. Theoretical Background
- **Classical Heuristics** (based on `1Dbin/README.md`):
  - **First Fit (FF)**: Place item in the first bin that fits.
  - **Best Fit (BF)**: Place item in the bin with min residual space.
  - **Decreasing Variants (FFD, BFD)**: Sort items $size_{desc}$ before packing. Strong performance on uniform data.
- **Metaheuristics**:
  - Overview of Evolutionary Computation.
  - **Grouping GA (GGA)**: Discuss Falkenauer's approach (group-based encoding) as the "heavyweight" alternative (referencing `binpacking-genetic-algorithm/`).
  - **Ant Colony Optimization (ACO)**: Discuss Rajacic's work as a comparable hybrid approach.

## 3. Methodology (The Proposed Algorithm)
- **Algorithm Architecture**: **Hybrid Genetic Algorithm**.
  - **Encoding**: Permutation Encoding (Chromosome = list of Item IDs).
  - **Decoder**: **First Fit Heuristic**.
    - *Crucial difference*: The GA evolves the *order*, the Decoder handles the *packing*.
    - This allows the GA to find sequences that "trick" the First Fit heuristic into optimal packing (e.g., putting large items with specific small items).
- **Genetic Operators**:
  - **Selection**: Tournament Selection ($k=2$ or $k=5$).
  - **Crossover**: Order Crossover (OX1) or Partially Mapped Crossover (PMX) to respect permutation constraints.
  - **Mutation**: Swap Mutation (exchange two items) or Inversion.
  - **Fitness Function**: Falkenauer's $k$-power objective function ($F = \sum (fill\_ratio)^k / N$).
    - Favors full bins over half-full bins, guiding the search better than just "number of bins".

## 4. Implementation details
- **Language**: Python (Jupyter Notebook).
- **Data Structures**:
  - Chromosome class.
  - Visualization using Matplotlib (already implemented).
- **Modification**: Upgrading `construct_bins` from Next Fit to First Fit.

## 5. Experimental Results
- **Datasets**:
  - **Uniform**: `u120`, `u250` (Standard tests).
  - **Triplets**: `t60`, `t120` (Hard tests where FFD fails).
- **Metrics**:
  - Optimal Gap % (Distance from lower bound).
  - Convergence Speed (Generations to best solution).
  - Comparison table:
    | Instance | FFD (Heuristic) | Permutation GA (Yours) | GGA (Literature) |
    | :--- | :--- | :--- | :--- |
    | u120_01 | 49 | 48 | 48 |
    | t60_01  | 22 | 20 | 20 |

## 6. Conclusion
- The Permutation GA + First Fit creates a robust solver.
- It outperforms simple heuristics on difficult instances (Triplets).
- It is simpler to implement than GGA but achieves competitive results for many practical cases.

## 7. References
- Falkenauer, E. (1996). *A hybrid grouping genetic algorithm for bin packing*.
- Rajacic, J. (2013). *Rešavanje jednodimenzionog problema pakovanja kombinovanjem optimizacionih metoda*.
- Munien, C. et al. (2020). *Metaheuristic Approaches for One-Dimensional Bin Packing Problem*.
