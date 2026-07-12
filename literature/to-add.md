# Zotero literature — to file / to acquire

Status from the literature gap analysis (2026-07-09). Zotero is in **local-only mode**
(reads work, writes need the Web API key Nikola declined), so **all actions below are manual
in the Zotero desktop app**.

## A. Already in the library — just FILE into the "master" collection (drag & drop)

These were added (as PDFs) but sit loose with no collection. No re-acquisition needed.

- **Coffman, Garey & Johnson (1984)** — *Approximation Algorithms for Bin-Packing: An Updated
  Survey* — item key `FRBA429M`. → Theoretical Background (its Table I is the canonical
  worst-case-bounds table: NF 2, FF/BF 17/10, Worst-Fit 2, FFD/BFD 11/9).
- **Martello & Toth (1990)** — *Knapsack Problems: Algorithms and Computer Implementations* —
  item key `MPPFL5QZ`. → Related Work (exact/B&B baseline, dominance criterion).
- Note: **Falkenauer (1996)** is *already filed* in "master" as `T6KJYXY8`. A duplicate
  (`2CV824V5`) is unfiled — merge the two via Zotero's Duplicate Items view rather than filing both.

## B. Genuinely missing — ACQUIRE via "Add Item by Identifier" (magic-wand icon)

Use the identifier, **not** a bare PDF, so metadata imports clean (avoids the RajacicJasna
problem where a title-less attachment won't format as a citation).

### MUST-HAVE
- **Falkenauer & Delchambre (1992)** — *A genetic algorithm for bin packing and line balancing*,
  Proc. IEEE ICRA, pp. 1186–1192. DOI `10.1109/ROBOT.1992.220088` (if the DOI import balks,
  import directly from the IEEE Xplore page: https://ieeexplore.ieee.org/document/220088/).
  → Methodology / Related Work — the original grouping-GA paper the 1996 article formalizes.
- **Delorme, Iori & Martello (2016)** — *Bin Packing and Cutting Stock Problems: Mathematical
  Models and Exact Algorithms*, EJOR 255(1), 1–20. DOI `10.1016/j.ejor.2016.04.030`.
  → Related Work / Results — the modern definitive survey; positions GA vs exact/ILP baselines.
  (Distinct from the 2018 BPPLIB paper `99FRTI6H` already in the library.)
- **Garey & Johnson (1979)** — *Computers and Intractability: A Guide to the Theory of
  NP-Completeness*, W.H. Freeman. ISBN `9780716710455`.
  → Theoretical Background — canonical NP-hardness citation for BPP.

### NICE-TO-HAVE (grounds GA operator theory; currently no generic GA text in the library)
- **Goldberg (1989)** — *Genetic Algorithms in Search, Optimization, and Machine Learning*,
  Addison-Wesley. ISBN `9780201157673`.
- **Michalewicz (1996)** — *Genetic Algorithms + Data Structures = Evolution Programs* (3rd ed.),
  Springer. ISBN `9783540606765`. Stronger on encoding design than Goldberg.

## C. Still no clean source

- **Schoenfield (2002)** — *Fast, exact solution of open bin packing problems without linear
  programming*, unpublished US Army technical report. No DOI, no PDF on hand. If you can't find
  a copy, create a manual Zotero item of type **Report** with the citation fields typed in.
