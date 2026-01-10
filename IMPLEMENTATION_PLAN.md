# Implementation Plan: Genetic Algorithm for Bin Packing

## 1. Project Goal
Implement a **Permutation-based Genetic Algorithm (GA)** using the **First Fit (FF)** heuristic to solve the One-Dimensional Bin Packing Problem (1D-BPP).
The solution will be tested on Falkenauer's benchmarks (`binpack1.txt` to `binpack8.txt`).

## 2. Data Parsing Strategy
The input files (e.g., `binpack1.txt`) contain multiple problem instances in a specific format.
We need a custom parser to read these files.

**File Format:**
- Line 1: Number of problems ($P$)
- Then for each problem:
  - Line $i$: Problem ID (e.g., `u120_00`)
  - Line $i+1$: `Capacity` `Num_Items` `Best_Known_Solution`
  - Next `Num_Items` lines: Item weights (one per line)

**Action:**
- Create a Python function `load_falkenauer_instances(file_path)` that returns a list of dictionaries:
  ```python
  [
    {
      "name": "u120_00",
      "capacity": 150,
      "num_items": 120,
      "best_known": 48,
      "items": [42, 69, 67, ...]
    },
    ...
  ]
  ```

## 3. Algorithm Design
We will use a **Hybrid GA**:
- **Genotype (Representation)**: A permutation (list) of Item IDs.
  - Example: `[5, 2, 1, 3, 4]` (Order in which items are presented to the heuristic).
- **Phenotype (Decoder)**: **First Fit Heuristic**.
  - We take the items in the order defined by the chromosome.
  - We place each item into the *first bin* where it fits.
  - If it fits nowhere, open a new bin.
- **Fitness Function**: Falkenauer's $k$-power objective.
  - $Fitness = \frac{\sum_{i=1}^{N} (fill\_i / C)^k}{N}$
  - where $k > 1$ (e.g., $k=2$ or $k=4$).
  - This rewards "tightly packed" bins, which is better than just counting bins.

## 4. Genetic Operators
- **Selection**: Tournament Selection (Size $k=2$ or $5$).
- **Crossover**: **Order Crossover (OX)** or PMX.
  - *Crucial*: Must preserve the permutation property (no duplicate items, no missing items).
- **Mutation**: **Swap Mutation**.
  - Swap two random items in the sequence.
- **Replacement**: Generational with Elitism (keep top 1-2 solutions).

## 5. Python Project Structure
We will organize the code into a clean, modular structure (or a well-organized Notebook).

```
project/
├── data/
│   ├── binpack1.txt
│   └── ...
├── src/
│   ├── parser.py       # Handles reading the Falkenauer files
│   ├── chromosome.py   # Class for Individual (genes + fitness)
│   ├── ga.py           # Main Genetic Algorithm loop
│   └── heuristic.py    # First Fit logic
├── main.py             # Entry point to run experiments
└── comparison.py       # Script to run FFD vs GA
```

## 6. Next Steps
1.  Implement `parser.py` to correctly read the 20 instances from `binpack1.txt`.
2.  Refine the `Chromosome` class to use the First Fit logic (done in notebook, can be moved to script).
3.  Run experiments on `u120` (Uniform) and `t60` (Triplets).

