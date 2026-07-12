> **Study notes only — not thesis prose.** This is a paraphrased digest for
> Nikola's own reading. Any idea used in the actual thesis must be
> rewritten entirely in his own words and cleared by the `plagiarism-guard`
> subagent; see `literature/digests/README.md`.

# Delorme, Iori & Martello (2018) — BPPLIB: a Library for Bin Packing and Cutting Stock Problems

**Zotero key:** `99FRTI6H`

## Full citation

Delorme, M., Iori, M., & Martello, S. (2018). BPPLIB: a library for bin
packing and cutting stock problems. *Optimization Letters*, 12(2), 235–250.
https://doi.org/10.1007/s11590-017-1192-z

(16 journal pages, printed pp. 235–250; PDF has an embedded outline, and the
PDF's own internal page count (p. 1–16) offsets exactly to the printed page
numbers by +234 — i.e. PDF p. *n* = printed p. *(n+234)*. Page numbers below
are given as printed-journal pages, cross-checked against this offset.
Section structure per the PDF outline: Abstract, 1 Introduction, 2 Web-based
libraries for optimization problems, 3 Computer codes [3.1 Branch-and-bound,
3.2 Branch-and-price, 3.3 Pseudo-polynomial formulations solved via ILP, 3.4
BppGame: an interactive visual solver], 4 Benchmarks [4.1 Literature
instances, 4.2 Randomly generated instances, 4.3 Hard instances, 4.4 GI
instances], 5 Computational experiments, 6 Conclusions and future research,
Acknowledgements, References.)

## Overview

The paper documenting BPPLIB (http://or.dei.unibo.it/library/bpplib), the
benchmark/code repository that supplies essentially all of Nikola's
experimental instances (Falkenauer, Scholl, Wäscher, Schwerin,
Schoenfield/Hard28 — 1263 files total per `CLAUDE.md`). It is simultaneously
(a) a formal problem-definition reference (clean ILP models for both BPP and
its generalization, the Cutting Stock Problem), (b) an annotated catalogue of
twelve exact solution codes spanning three solution paradigms
(branch-and-bound, branch-and-price, pseudo-polynomial ILP), (c) a precise
description of every benchmark instance family's construction, size, and
known difficulty (Table 2 is the single best "benchmark landscape" reference
available for citing *why* each instance family is hard), and (d) a fresh
round of computational experiments comparing all twelve codes (with both
CPLEX and the free SCIP solver) across four major benchmark groups —
literature instances, randomly generated instances, "hard" (Non-IRUP /
augmented-IRUP) instances, and the newer GI instances. BPPLIB's own stated
citation requirement (per `CLAUDE.md`) means this paper must be cited
whenever Nikola's thesis uses instances drawn from it — which, given the
`BPPLIB/` git submodule, is effectively always.

## Section-by-section walkthrough

### Abstract (p. 235)

Summarizes: a library of computer codes, benchmark instances, and literature
pointers for BPP/CSP; twelve programs (seven directly downloadable, five
linked externally); dual CPLEX/SCIP versions where an ILP solver is needed;
"over six thousands instances... together with the corresponding solutions,"
including instances "difficult to solve to proven optimality"; a BibTeX file
of 150+ references; an interactive visual solver ("BppGame"); and new
computational experiments.

### 1. Introduction (p. 236–237)

Formal **BPP** definition: n items of integer weight wⱼ (j=1,...,n) packed
into the minimum number of identical bins of integer capacity c. With u an
upper bound on the solution value, binary yᵢ ("bin i used") and xᵢⱼ ("item j
in bin i"), the ILP model (citing Martello & Toth 1990), given as eq. (1)–(5):

```
min  Σ_{i=1}^{u} y_i                                          (1)
s.t. Σ_{j=1}^{n} w_j x_ij ≤ c·y_i     for i = 1,...,u           (2)
     Σ_{i=1}^{u} x_ij = 1             for j = 1,...,n           (3)
     y_i ∈ {0,1}                       for i = 1,...,u           (4)
     x_ij ∈ {0,1}                      for i=1,...,u; j=1,...,n  (5)
```

Then generalizes to the **Cutting Stock Problem (CSP)**: m item *types* of
weight wⱼ, each with integer *demand* dⱼ, and integer variables ξᵢⱼ ("copies
of item type j in bin i") replacing the binary xᵢⱼ, giving eq. (6)–(10):

```
min  Σ_{i=1}^{u} y_i                                          (6)
s.t. Σ_{j=1}^{m} w_j ξ_ij ≤ c·y_i     for i = 1,...,u           (7)
     Σ_{i=1}^{u} ξ_ij = d_j            for j = 1,...,m           (8)
     y_i ∈ {0,1}                       for i = 1,...,u           (9)
     ξ_ij ≥ 0, integer                 for i=1,...,u; j=1,...,m  (10)
```

States BPP is **NP-hard in the strong sense** (by transformation from
3-Partition, citing Garey & Johnson 1979), and since any BPP instance
transforms easily into an equivalent CSP instance (and vice versa), the same
hardness holds for CSP. Frames the field's scale: "Two recent surveys on
exact methods (Delorme et al. [14]) and approximation algorithms (Coffman et
al. [10]) consider in total over 230 different references," and lists prior
surveys by name (Garey & Johnson, Coffman et al., Sweeney & Paternoster,
Dyckhoff, Martello & Toth Ch. 8, Dyckhoff & Finke, Valério de Carvalho,
Wäscher et al.) — a ready-made map of the survey literature for a Related
Work section. Previews the rest of the paper's structure.

### 2. Web-based libraries for optimization problems (p. 237–238)

A short survey of sibling benchmark repositories for other combinatorial
problems, situating BPPLIB among them: **OR-Library** (Beasley, the oldest,
covering many OR problem types including 1D/2D packing), **QAPLIB**
(quadratic assignment), the **TSP web page** (Applegate et al.), **VRPH**
(vehicle routing heuristics library), **MIPLIB** (mixed-integer programming),
**libcgrpp** (bound-constrained global optimization), **CBLIB 2014** (conic
mixed-integer/continuous optimization, offering solve-reward incentives),
**CVRPLIB** (VRP instances, also reward-incentivized). Notes BPPLIB itself
grew out of "an earlier, smaller version... implemented as an auxiliary
instrument" for Delorme/Iori/Martello (2016)'s computational experiments, and
points to ESICUP (the EURO working group on cutting and packing) as another
source of BPP/CSP data sets and generators.

### 3. Computer codes (p. 238–241)

Twelve exact codes total, chosen for "historical relevance, efficiency,
reliability, and availability," summarized in Table 1 (code name, problem,
BPPLIB delivery mode [code/pointer/link], language, algorithm type,
reference, author, year, and which ILP solver — CPLEX/Gurobi/SCIP — each
needs, if any).

**3.1 Branch-and-bound** (p. 238–239) — the historically first exact
approach family:
- **MTP**: Martello & Toth (1990)'s original Fortran BPP code (from the
  book's diskette); depth-first branch-decision tree, one item per level,
  descendants generated by assigning the item to each already-open bin or a
  new bin. "Effective for BPP instances" but "clearly inefficient for CSP
  instances with high item multiplicity" (one-item-at-a-time doesn't exploit
  identical-item structure).
- **BISON**: Scholl, Klein & Jürgens (1997) — enriches MTP with new lower
  bounds plus a Tabu Search to generate strong heuristic incumbents; Pascal
  implementation; explicitly praised as "still working and quite effective"
  despite its age.
- **CVRPSEP**: a C-code separation routine (Lysgaard, built from MTP
  procedures) originally for the capacitated VRP branch-and-cut algorithm of
  Lysgaard et al. (2004); "generally less efficient than MTP" but included
  for C-vs-Fortran language preference.

**3.2 Branch-and-price** (p. 240) — "the modern evolution of
branch-and-bound... combining implicit enumeration and column generation":
- **BELOV**: C++ (Belov & Scheithauer 2006) branch-and-cut-and-price,
  CPLEX-dependent; "tailored to the exact solution of CSP instances," and
  "computationally proved to be the most powerful approach both in the case
  of low and high item multiplicity."
- **SCIP-BP**: free SCIP-based branch-and-price using the classical Ryan &
  Foster (1981) branching rule; "only effective for instances with small
  number of item types and low item multiplicity."

**3.3 Pseudo-polynomial formulations solved via ILP** (p. 240–241) — models
from a graph representation of the solution space, historically regarded as
"very theoretical, with no practical interest" due to huge variable/
constraint counts, but "nowadays computational power of ILP solvers made
them competitive... provided the number of generated variables... is not too
big":
- **ONECUT** (Rao 1976 / Dyckhoff 1981's one-cut CSP model, C++
  implementation),
- **ARCFLOW** (Valério de Carvalho's arc-flow CSP model),
- **DPFLOW** (Cambazard & O'Sullivan's DP-flow BPP model),
- **VPSOLVER** (Brandão & Pedroso's arc-flow implementation with graph
  compression) — "currently the most effective pseudo-polynomial approach,
  and its performance is often competitive with that of BELOV." The first
  three ship in both CPLEX and SCIP variants; VPSOLVER uses Gurobi.

**3.4 BppGame: an interactive visual solver** (p. 241) — an open-source
ScalaFX GUI (derived from a general 2D-packing training tool, Costa et al.
2017) letting a user drag-and-drop items into bins to manually construct a
BPP/CSP solution; described as useful for educational demonstration of
problem difficulty.

### 4. Benchmarks (p. 241–244)

**6,195 benchmark instances across four categories**, each provided in both
BPP and CSP format. **Table 2** (p. 242) is the single clearest "benchmark
landscape" reference, giving for every family: instance count (#), item
count n, capacity c, weight distribution, and flags (large c, "perf. pack."
= perfect packing, "non-IRUP"):

| Family | # instances | n | c | Distribution | Flags |
|---|---|---|---|---|---|
| Falkenauer U | 80 | {120,250,500,1000} | 150 | Uniform | — |
| Falkenauer T | 80 | {60,120,249,501} | 1000 | Ad-hoc | perf. pack. |
| Scholl1 | 720 | {50,100,200,500} | {100,120,150} | Uniform | — |
| Scholl2 | 480 | {50,100,200,500} | 1000 | Uniform | — |
| Scholl3 | 10 | 200 | 100,000 | Uniform | large c |
| Wäscher | 17 | [57–239] | 10,000 | Ad-hoc | large c, perf.pack., non-IRUP |
| Schwerin1 | 100 | 100 | 1000 | Uniform | — |
| Schwerin2 | 100 | 120 | 1000 | Uniform | — |
| Hard28 | 28 | {160,180,200} | 1000 | Ad-hoc | perf.pack., non-IRUP |
| Random | 3840 | 50–1000 (8 values) | 50–1000 | Uniform | — |
| AI | 250 | {202,403,601,802,1003} | ≤{2.5K,10K,20K,40K,80K} | Ad-hoc | large c, non-IRUP |
| ANI | 250 | {201,402,600,801,1002} | ≤{2.5K,10K,20K,40K,80K} | Ad-hoc | large c, non-IRUP |
| GI | 240 | ~10.5×{125,250,500} | {500K, 1.5M} | Uniform | large c |

**4.1 Literature instances** (p. 243) — 1615 instances total, one-line
provenance for each set: **Falkenauer** [18]: "80 (easy) instances with
uniformly distributed item sizes and 80 (more difficult) instances obtained
through triplets of items that, in any optimal solution, must be packed into
the same bin without leaving unused space (perfect packing)" — the exact
construction of the Falkenauer_T triplet instances Nikola uses. **Scholl et
al.** [32]: three uniform-distribution sets — 720 "easy," 480 "medium
difficulty," and 10 "difficult... characterized by huge capacities."
**Wäscher and Gau** [39]: "17 very hard instances selected... from a much
larger set of instances belonging to different typologies." **Schwerin and
Wäscher** [33]: two sets of 100 "relatively easy" instances. **Schoenfield**
[31]: "28 hard instances that do not involve huge capacities" — Hard28.
Additional instances can be generated via linked generators (Schwerin &
Wäscher; Gau & Wäscher's CUTGEN1).

**4.2 Randomly generated instances** (p. 243) — 3840 instances from
Delorme/Iori/Martello (2016)'s own experiments: n ∈ {50,100,200,300,400,500,
750,1000}, c ∈ {50,75,100,120,125,150,200,300,400,500,750,1000}, item weight
ranges with minimum ∈ {0.1c, 0.2c} and maximum ∈ {0.7c, 0.8c} — 10 instances
per each of 384 (n, c, min, max) quadruplets. Characterized as "relatively
easy" — most solved within reasonable CPU time by the library's own codes.

**4.3 Hard instances** (p. 243–244) — defines the **Integer Round-Up
Property (IRUP)**: an instance possessing it (per Berge & Johnson) is
"generally considered less difficult to solve in practice." Non-IRUP
instances (built on a base set from Caprara et al. 2014) split into two
250-instance classes: **augmented Non-IRUP** — "an optimal solution is easy
to find, but its optimality is very difficult to prove," since even the
continuous relaxations underlying both branch-and-price and pseudo-
polynomial approaches "fail in reaching the optimal value," so around n≈400
"no algorithm is capable of solving all of them to proven optimality"; and
**augmented IRUP** — the reverse difficulty, "easy to produce a lower bound
whose value is equal to the optimum, but... difficult to build an optimal
solution."

**4.4 GI instances** (p. 244) — 240 new instances (Gschwind & Irnich 2016),
uniformly randomly generated with very large capacities, organized into four
60-instance sets; "two of such sets are generally difficult to solve" (borne
out in §5's experiments below).

### 5. Computational experiments (p. 244–248)

Hardware: **Intel Xeon 3.10 GHz, 4 cores, 8 GB RAM, single core per run.**
Pre-filtering methodology: compute a BFD (Best-Fit-Decreasing) upper bound
and the L2 lower bound (Martello & Toth), and *only* test instances where
these two values differ — i.e. trivially-solved instances (upper bound =
lower bound already) are excluded from the timing tables. A 1-CPU-minute
time limit is used throughout; unsolved instances are counted as the full 60
seconds in averages.

**Table 3** (enumerative algorithms, literature instances, non-trivial
subset) — selected figures (instances solved within 1 min, average CPU
seconds in parentheses):

| Set | tested | MTP | BISON | CVRPSEP | BELOV | SCIP-BP |
|---|---|---|---|---|---|---|
| Falkenauer U | 74 | 22 (42.8) | 44 (24.5) | 22 (42.2) | **74 (0.0)** | 18 (50.1) |
| Falkenauer T | 80 | 6 (55.5) | 42 (30.6) | 0 (60.0) | 57 (24.7) | 35 (39.4) |
| Hard28 | 28 | 0 (60.0) | 0 (60.0) | 0 (60.0) | **28 (7.3)** | 7 (51.2) |
| Total | 976 | 419 (34.4) | 783 (12.3) | 319 (40.8) | 953 (2.7) | 371 (42.2) |

BELOV solves essentially everything (953/976) and is the only method to
fully clear Falkenauer U and Hard28; MTP/CVRPSEP struggle badly on
Falkenauer T and Hard28 (0/28 solved by both within the minute).

**Table 4** (pseudo-polynomial models, literature instances): VPSOLVER is
the standout, e.g. Falkenauer T 80/80 solved (0.4s avg), Hard28 27/28
(14.2s); ONECUT/ARCFLOW/DPFLOW under CPLEX are strong on Falkenauer/Scholl1
but weak on Wäscher/Scholl3/Hard28 (mostly 0 solved); performance drops
sharply when SCIP replaces CPLEX for the same models, especially on harder
sets.

**Tables 5–6** (random instances, n up to 1000): same pattern — BELOV and
VPSOLVER dominate (BELOV solves essentially all 2901 non-trivial instances,
avg 0.2s; VPSOLVER 2891/2901, avg 1.4s under CPLEX), while MTP/CVRPSEP/
SCIP-BP degrade sharply as n grows (e.g. SCIP-BP falls to 0/441 solved at
n=1000).

**Table 7** (GI instances, 1-hour limit): BELOV solves **all 240** instances
quickly (avg 6.8s); ARCFLOW solves only 39/240 (many timeouts at 3600.0s);
VPSOLVER solves 113/240. The AB and BB groups (large capacity ≥500,000,
small item weights) are uniformly hard for the pseudo-polynomial models —
0/20 solved in every AB/BB row for ARCFLOW, and 0/20 for VPSOLVER on AB.

**Explanatory notes on model blow-up**: ARCFLOW produces, on average, 1735
variables/103 constraints for "Scholl 1" instances vs. 39,307
variables/840 constraints for "Scholl 2" — illustrating how capacity and
item-weight structure (not just item count) drive pseudo-polynomial model
size. Similarly for GI instances, ARCFLOW averages 549,441 variables/
131,219 constraints for set AA (m=125) vs. 5,754,617 variables/404,283
constraints for set AB (m=125) — a >10× variable blow-up from capacity
structure alone.

**Headline conclusion of §5**: "the clear superiority of BELOV and VPSOLVER
over the other algorithms," with SCIP consistently underperforming CPLEX,
especially as instance difficulty/size grows.

### 6. Conclusions and future research (p. 248)

Restates the library's four components (codes, benchmarks, references,
visual solver) and states intent to keep BPPLIB updated with new
contributions and expand into related problem variants. Frames BppGame as
also useful pedagogically. Acknowledgements: funded by AFOSR (Grant
FA9550-17-1-0067) and MIUR-Italy (PRIN 2015); credits Gianluca Costa for
BppGame development.

## Citable specifics

> "In the bin packing problem (BPP), n items of given integer weight
> w_j (j=1,...,n) have to be packed into the minimum number of identical
> containers (bins) of integer capacity c." (p. 236, §1 — canonical problem
> statement, with the ILP model eq. 1–5 immediately following)

> "The BPP is known to be N P-hard in the strong sense (by transformation
> from the 3-Partition problem, see Garey and Johnson [20])." (p. 236, §1)

> "Two recent surveys on exact methods (Delorme et al. [14]) and
> approximation algorithms (Coffman et al. [10]) consider in total over 230
> different references." (p. 237, §1)

> "Falkenauer [18]: 80 (easy) instances with uniformly distributed item
> sizes and 80 (more difficult) instances obtained through triplets of
> items that, in any optimal solution, must be packed into the same bin
> without leaving unused space (perfect packing)." (p. 243, §4.1 — the
> precise construction of the Falkenauer_T "triplet" instances Nikola's
> benchmark set includes)

> "Schoenfield [31]: 28 hard instances that do not involve huge capacities."
> (p. 243, §4.1 — Hard28, one of the core families in Nikola's `BPPLIB/`
> submodule)

> "An instance of an optimization problem that possesses the so-called
> Integer round-up property... is called an IRUP instance and is generally
> considered less difficult to solve in practice with respect to instances
> not possessing such property." (p. 243, §4.3 — the definition underlying
> why several instance families are explicitly flagged "non-IRUP" in Table
> 2, i.e. deliberately harder)

> "For the 250 instances of the [augmented Non-IRUP] class an optimal
> solution is easy to find, but its optimality is very difficult to prove.
> ... already for n ≈ 400, no algorithm is capable of solving all of them to
> proven optimality." (p. 243–244, §4.3)

> "The tables confirm the clear superiority of BELOV and VPSOLVER over the
> other algorithms." (p. 245, §5 — the paper's own headline computational
> finding)

> "BISON: ... Worth is mentioning that, in spite of its 'age', this program
> is still working and quite effective." (p. 239, §3.1 — BISON is a
> reference exact solver Nikola's Solutions.xlsx/known-optima comparisons
> ultimately trace back to)

> "We believe that the BPPLIB can be a useful tool to foster new research on
> the challenging area of Bin Packing and Cutting Stock optimization." (p.
> 248, §6 Conclusions)

## How it helps Nikola's thesis

- This is the **primary citation BPPLIB itself requires** whenever Nikola's
  thesis uses instances drawn from it — per `CLAUDE.md`'s note that
  "BPPLIB's own citation requirement" applies to any use of their material,
  and given the `BPPLIB/` git submodule underlies essentially all of
  Nikola's 1263 benchmark files, this citation is mandatory in Ch3/Ch5.
- **Table 2** (p. 242) is the best available single source for precisely
  describing each benchmark family's construction and known difficulty in a
  Methods/Experimental Setup section — Nikola can cite exact instance
  counts, item-count ranges, capacities, distributions, and the perfect-
  packing/non-IRUP flags directly rather than re-deriving them.
- The clean ILP models for **both BPP (eq. 1–5) and CSP (eq. 6–10)** let
  Nikola cross-check his own formal problem statement, and explicitly shows
  how BPP is the special case of CSP with unit demand per item — useful if
  Ch1 wants to briefly situate 1D-BPP within the broader cutting-stock
  family.
- The **IRUP/non-IRUP distinction** (§4.3) gives Nikola precise vocabulary
  for *why* certain instance families (Wäscher, Hard28, AI/ANI) are
  deliberately harder than others, beyond just "more items" — useful when
  Ch5 discusses instance-family-dependent GA performance.
- **Table 3's concrete solved-instance counts and CPU times** across five
  exact solvers (MTP, BISON, CVRPSEP, BELOV, SCIP-BP) is a ready reference
  point for how hard these instance families are known to be *even for
  purpose-built exact solvers* — good context for framing why a heuristic/
  metaheuristic GA is worth studying on them at all, and a natural point of
  comparison if Nikola ever wants to note that his GA does not aim for (and
  is not benchmarked against) exact-solver optimality guarantees, only
  known-best solution values from `Solutions.xlsx`.
