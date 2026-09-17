# One-dimensional bin packing algorithms

## Problem statement and notation

Given `n` items with sizes `w_j` and identical bins of capacity `C`, assign every item to exactly one bin, keep the total size in every bin at most `C`, and minimize the number of bins used. [chunk_002] [chunk_016]

A compact mathematical statement consistent with the summaries is:

\[
\min N
\quad\text{such that}\quad
\sum_{j \in B_i} w_j \le C \text{ for every used bin } i,
\quad
\bigcup_i B_i=\{1,\ldots,n\},
\quad
B_i\cap B_k=\varnothing\;(i\ne k).
\]

This formulation restates the stated objective, capacity condition, and requirement that all items be packed; the summaries do not provide a full binary-variable ILP formulation. [chunk_003] [chunk_016]

## Reference values, bounds, and quality measures

| Quantity | Formula or rule present in the summaries | Interpretation and caveat |
|---|---|---|
| Proven optimum from BPPLIB | `Best LB = Best UB = OPT` [chunk_002] | Equality certifies the common bin count only when workbook fields/status are read correctly; `Best UB` alone is not automatically an optimum. [chunk_003]
| LP-to-integer lower bound example | `lpval = 24.75`, `lpbnd = 25` [chunk_001] | The supplied solver record uses 25 as its integer lower bound, but no general rounding formula or lower-bound derivation is given in the summaries. [chunk_004]
| Construction-guaranteed T optimum | `OPT = n / 3` [chunk_002] | Applies to Falkenauer triplet instances by construction, with exactly three items per bin; reported examples are 20, 40, 83, and 167 for `n=60,120,249,501`. [chunk_002]
| Absolute signed gap used by the project | `Gap_h = bins_h - reference` [chunk_004] | Nonnegative when the reference is a valid optimum; calling it an optimality gap is unsafe for historical best-known or open workbook rows. [chunk_006]
| Absolute deviation reported for Scholl context | `|x-y|` [chunk_003] | Unlike the project gap, this removes sign; the two definitions should not be silently treated as identical. [chunk_003]
| Relative deviation reported for Scholl context | `|x-y| / y * 100%` [chunk_003] | The denominator `y` must be defined as the reference value in the thesis. [chunk_003]
| Missing-reference behavior in shown code | `Gap_GA = 0` when no optimum is truthy [chunk_007] | This is invalid as evidence because it conflates unknown reference data with an exact solution; use missing/NA instead. [chunk_008] [chunk_016]
| Runtime | elapsed wall-clock seconds around sorting plus heuristic execution, or around GA construction plus `run()` [chunk_005] [chunk_015] | Single timings from `time.time()` are preliminary; hardware, package versions, warm-up, repetition, and variance are not documented. [chunk_016]

No elementary lower bound such as a total-weight/capacity ceiling is explicitly recorded in the summaries, so it is not attributed to an existing project source here. [chunk_001] [chunk_016]

## Constructive heuristics

All shown implementations return bins containing a used-capacity value and item records; feasibility tests commonly use `used + item_size <= capacity + 1e-6` for decimal input. [chunk_003] [chunk_005]

| Name | Behavior in the summaries | Order/variant | Complexity or parity issue |
|---|---|---|---|
| First Fit (FF) | Scan bins in creation order; place the item in the first feasible bin, otherwise open a new bin. [chunk_005] | Original item order. [chunk_007] | Shown as a linear scan per item and discussed as worst-case quadratic; no source-verified tie-breaking test is recorded. [chunk_011] [chunk_012]
| First Fit Decreasing (FFD) | Sort items by nonincreasing size, then apply FF. [chunk_002] | Current Python proposals use general descending sort. [chunk_012] | The cited naming table says FFD uses Heapsort, so the Python result rule may match while the implementation/timing method does not. [chunk_012] [chunk_013]
| Best Fit (BF) | Among feasible bins choose the one leaving the least residual capacity. [chunk_005] | Original item order. [chunk_007] | Scan-based behavior is clear, but exact tie-breaking against the C++ source is unverified. [chunk_005] [chunk_014]
| Best Fit Decreasing (BFD) | Sort descending, then apply BF. [chunk_005] | Project-added paired variant. [chunk_012] | It appears in the thesis comparisons, but the supplied Rieck naming excerpt ends at BF and does not establish a `BFD` label there. [chunk_012] [chunk_013]
| Next Fit (NF) | Consider only the current/last bin; open a new bin when the next item does not fit. [chunk_005] | Original item order. [chunk_007] | External excerpts call it fastest because it manages one bin, but those C++ timings are not comparable with local Python timings. [chunk_011]
| Next Fit Decreasing (NFD) | Sort descending, then apply NF. [chunk_005] | General descending sort in current proposals. [chunk_012] | The supplied naming table distinguishes NFD from NFD+ by sorting method. [chunk_011] [chunk_012]
| Max-Rest (MR) | Among feasible bins choose the bin with the greatest remaining capacity. [chunk_005] | Original item order. [chunk_013] | The project treats this as Worst Fit, but equivalence to the requested PDF/C++ definition and its tie rules is not demonstrated. [chunk_005]
| Max-Rest Decreasing (MRD) | Sort descending, then apply MR. [chunk_005] | Project-added paired variant. [chunk_012] | It is not shown in the supplied PDF naming table and needs a clear project definition rather than implied source attribution. [chunk_012]
| MR+ | Use a priority queue keyed by negative remaining capacity to retrieve the bin with maximum free space. [chunk_011] | Same item order as MR. [chunk_011] | Claimed `O(n log n)` versus scan MR `O(n^2)`; one run showed equal bin counts, but general assignment/tie parity needs controlled tests. [chunk_012]
| MRD+ | Sort descending, then use MR+. [chunk_012] | Project-added decreasing priority-queue variant. [chunk_012] | Same parity requirement as MR+; it is not established as a name from the cited paper. [chunk_012]

## Optimized and lookup variants

| Project/source label | Stated mechanism | Mapping and unresolved issue |
|---|---|---|
| FF+ in the supplied paper excerpt | STL vector removes bins that are too full to accept any remaining item. [chunk_011] [chunk_012] | Exact close-bin condition is unclear because the excerpt's `c_l = K - w` formula is encoding-damaged and potentially inconsistent. [chunk_011]
| FF++ in the supplied paper excerpt | STL map/lookup structure stores a useful starting bin/index for later items. [chunk_011] [chunk_012] | The paper still reportedly states `O(n^2)`; no faithful Python parity test is present. [chunk_011]
| `first_fit_lookup` / FFL in project proposals | Store a last-used bin index keyed by item size and resume scanning there. [chunk_013] | It was described as analogous to FF++, but equivalence is unproven and the label FFL does not occur in the supplied naming table. [chunk_013] [chunk_014]
| FFD+ in the supplied paper excerpt | FF+ plus Counting Sort. [chunk_011] [chunk_012] | Project code instead appears to mean ordinary FF preceded by Counting Sort; this may preserve a packing order but omit FF+'s active-bin structure. [chunk_013]
| FFD++ in the supplied paper excerpt | FF++ plus Counting Sort. [chunk_011] [chunk_012] | Deferred in conversation; no verified Python implementation is reported. [chunk_012]
| NFD+ | NF preceded by Counting Sort. [chunk_011] [chunk_012] | The project falls back to ordinary descending sort for non-integral item sizes, so the label denotes different sorting paths across datasets. [chunk_013] [chunk_015]
| `best_fit_lookup` / BFL | Bucket bin indices by exact integer residual capacity and search upward from the item size. [chunk_013] [chunk_014] | Not established by the supplied paper naming table; it may truncate non-integral item/residual values and allocate `capacity+1` buckets, making correctness and cost on capacity 100000 unresolved. [chunk_013]
| Counting Sort helper | Bucket integer-sized items and emit identifiers from largest size downward. [chunk_013] | Claimed `O(n)` under bounded-integer assumptions versus comparison sorting `O(n log n)`; the full cost also depends on the maximum item value/range. [chunk_011] [chunk_013]

## Naming and source mapping

The supplied Rieck naming excerpt defines `MR`, `MR+`, `FF`, `FF+`, `FF++`, `FFD`, `FFD+`, `FFD++`, `NF`, `NFD`, `NFD+`, and `BF`. [chunk_012]

The project additionally uses `BFD`, `MRD`, `MRD+`, `FFL`, and `BFL`; these should be presented as project labels unless direct source evidence is found. [chunk_012] [chunk_013]

The project has at different times claimed 14 heuristics plus GA, but displayed/stored algorithm lists have differed, and some reports omitted computed variants such as MRD+. The authoritative list must come from the validated runner, not conversational counts. [chunk_013]

## Observed behavior that needs explanation

1. Descending variants sometimes used more bins than their unsorted bases, including Falkenauer triplet examples where FF/BF/NF/MR reached the construction optimum while FFD/BFD/NFD/MRD did not. These outputs may be valid for the particular original order, but parser order and implementation parity need verification. [chunk_008] [chunk_011] [chunk_016]
2. MR+ and MRD+ matched MR and MRD bin counts throughout one displayed 30-instance run, while a single rounded timing example showed MR+ about 7.5 times faster; this is not enough to establish general equivalence or speedup. [chunk_012]
3. Lookup and counting-sort variants matched corresponding unspecialized bin counts throughout one pasted sample, suggesting their intended difference there was runtime rather than packing quality; console output omitted the needed timings. [chunk_016]
4. NF/NFD were often substantially worse in bin count than other constructive heuristics in the displayed samples, but unseeded sampling and incomplete/revised implementations prevent a general claim. [chunk_005] [chunk_016]

## Implementation-parity work still required

- Read the original heuristic PDF and the C++ `first-fit.cpp`, `best-fit.cpp`, `next-fit.cpp`, `max-rest.cpp`, and related helpers before finalizing Python names or complexity claims. [chunk_013] [chunk_014]
- Create controlled fixtures that compare Python and C++ bin counts, item assignments, and tie behavior for every mapped variant, including integer and decimal inputs. [chunk_014]
- Verify that every algorithm packs every item exactly once and never exceeds capacity; `1e-6` tolerance versus exact integer rescaling is still an explicit design choice for decimal Falkenauer files. [chunk_003]
- Separate packing-rule parity from performance parity: Python's Timsort, `heapq`, lists, and dictionaries need not reproduce the C++ paper's Heapsort, Counting Sort, STL vector, map, or custom heap costs. [chunk_011] [chunk_012]
- Replace missing-reference gap `0` with missing data and retain workbook lower bound, upper bound, and status so quality labels are correct. [chunk_003] [chunk_016]
