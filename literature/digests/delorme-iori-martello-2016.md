> **Study notes only — not thesis prose.** This is a paraphrased digest for
> Nikola's own reading. Any idea used in the actual thesis must be
> rewritten entirely in his own words and cleared by the `plagiarism-guard`
> subagent; see `literature/digests/README.md`.

# Delorme, Iori & Martello (2016) — Bin Packing and Cutting Stock Problems: Mathematical Models and Exact Algorithms

**Zotero key:** `J232IF9S`

## Full citation

Delorme, M., Iori, M., & Martello, S. (2016). Bin Packing and Cutting Stock
Problems: Mathematical Models and Exact Algorithms. *European Journal of
Operational Research*, 255(1), 1–20.
https://doi.org/10.1016/j.ejor.2016.04.030

(The Zotero-attached PDF is Elsevier's **"Accepted Manuscript"** pre-typeset
version, not the final journal proof — it carries its own header/footer
apparatus ["ACCEPTED MANUSCRIPT" running headers, a single-column layout]
whose internal page count does *not* reliably map onto the published pp.
1–20 pagination. Locators below therefore cite the paper's own **section
numbers**, which are stable across both versions, rather than invented page
numbers. Section structure: 1 Introduction, 2 Formal statement, 3 Upper and
lower bounds [3.1 Approximation algorithms, 3.2 Lower bounds, 3.3 Heuristics
and metaheuristics], 4 Pseudo-polynomial formulations [4.1 Considerations on
the basic ILP model, 4.2 One-cut formulation, 4.3 DP-flow formulation, 4.4
Arc-flow formulations], 5 Enumeration algorithms [5.1 Branch-and-bound, 5.2
Constraint programming approaches], 6 Branch-and-price [6.1 Set covering
formulation and column generation, 6.2 Integer round-up property, 6.3
Branch(-and-cut)-and-price algorithms], 7 Experimental evaluation [7.1
Benchmarks, 7.2 Computer codes, 7.3 Experiments], 8 Conclusions,
Acknowledgements, References. No embedded PDF outline.)

## Overview

A comprehensive, modern survey of mathematical models and exact algorithms
for the 1D bin packing and cutting stock problems: pseudo-polynomial ILP
formulations (one-cut, DP-flow, arc-flow), enumeration (branch-and-bound,
constraint programming), and branch-and-price, plus an extensive
computational evaluation of **twelve solvers** across four major benchmark
groups, including a newly designed class of especially hard "augmented
Non-IRUP" instances. It also reviews and updates the classical worst-case
bounds literature, notably reporting that the *exact* (non-asymptotic)
worst-case ratio of FF/BF — open for roughly forty years after Johnson et
al. (1974) — was finally resolved by Dósa and Sgall. §3.3's literature
review of heuristics/metaheuristics explicitly discusses Falkenauer &
Delchambre (1992) and Falkenauer (1996), including the pointed caveat
(citing Gent 1998) that most of Falkenauer's widely-used benchmark instances
are actually "very easy" — an important nuance for anyone (including
Nikola) benchmarking a GA against that instance family. This is the most
detailed and most recent of the six literature-digest sources for
theoretical background material, and its own benchmark set later became the
core of BPPLIB (Delorme, Iori & Martello 2018).

## Section-by-section walkthrough

### 1. Introduction

Traces the problem's history: "Its structure and its applications have been
studied since the thirties, see Kantorovich [82]," with Gilmore and Gomory
[69] introducing column generation for this problem class in 1961, itself
derived from Ford & Fulkerson and Dantzig & Wolfe's earlier ideas. Notes BPP
was "one of the first problems for which, since the early seventies, the
worst-case performance of approximation algorithms was investigated."
Informally defines BPP (n items of integer weight, unlimited identical bins
of integer capacity c, minimize bins used) and its generalization CSP (m
item *types*, each with integer demand dⱼ, "rolls" and "cutting" terminology
from the paper industry). States motivation: presenting, "for the first
time, a complete overview" of the field plus a fresh computational
evaluation on a dedicated benchmark web page; notes a bibliometric signal of
rising interest ("over 150 Google Scholar entries in 2015" for
bin-packing/cutting-stock titled papers). Surveys **prior surveys** in
detail — a ready-made map of the survey literature: Sweeney & Paternoster
(1992, first review, 400+ works from 1961–1990); Dyckhoff (1990) typology
classifying BPP/CSP as 1/V/I/M and 1/V/I/R; Martello & Toth (1990, book
chapter); Dyckhoff & Finke (1992, book); Coffman et al. (bibliography);
Wäscher et al.'s revised typology, re-classifying the problems this paper
considers as **1-dimensional SBSBPP** (Single Bin Size Bin Packing Problem)
and **1-dimensional SSSCSP** (Single Stock Size Cutting Stock Problem);
Garey & Johnson (1981) and Coffman et al. (1984, 1996, 1999, 2013) on
approximation algorithms specifically; Valério de Carvalho (2002) on LP
methods; Belov's PhD thesis; Haessler & Sweeney on 1D/2D cutting stock;
Lodi et al. on 2D packing. Previews the paper's own structure (Sections
2–8).

### 2. Formal statement

Gives the same ILP model as BPPLIB (2018) but as the paper's own eq.
(1)–(5) for BPP:

```
min  Σ_{i=1}^{u} y_i
s.t. Σ_{j=1}^{n} w_j x_ij ≤ c·y_i     (i = 1,...,u)
     Σ_{i=1}^{u} x_ij = 1              (j = 1,...,n)
     y_i, x_ij ∈ {0,1}
```

and eq. (6)–(10) for CSP (integer ξᵢⱼ replacing binary xᵢⱼ, demand
constraint Σᵢξᵢⱼ = dⱼ). States explicitly: "The BPP can be seen as a
special case of the CSP in which dⱼ = 1 for all j. In turn, the CSP can be
modeled by a BPP in which the item set includes dⱼ copies of each item type
j" — the formal equivalence underlying why the two problems are treated
uniformly throughout. Confirms strong NP-hardness (Garey & Johnson,
transformation from 3-Partition).

### 3. Upper and lower bounds

**3.1 Approximation algorithms.** Distinguishes *approximation algorithm*
(admits theoretical worst-case results) from *heuristic* (studied mainly
empirically) — terminology worth adopting explicitly when Nikola frames his
GA (a heuristic/metaheuristic without proven worst-case bounds) against
FF/BF/FFD/BFD (approximation algorithms with proven bounds). Gives Next-Fit
(NF): "at each iteration packs the next item into the current bin... or
into a new bin... if it does not [fit]," with **r(NF) = 2**. Gives FF and BF
informally (lowest-indexed feasible bin vs. tightest-fitting feasible bin).
States: "The exact WCPR of FF and BF has been an open problem for forty
years, until recently Dósa and Sgall [46,47] proved that **r(FF) = r(BF) =
17/10**" — i.e. Johnson et al. (1974)'s asymptotic 17/10 bound is now known
to hold *exactly*, not just in the limit, closing a four-decade-old open
question. FFD/BFD (sort decreasing, then FF/BF): **r(FFD) = r(BFD) = 3/2**
(Simchi-Levi). Gives **Property 1** with full proof: "No polynomial-time
approximation algorithm for the BPP can have a WCPR smaller than 3/2 unless
P = NP" — proved by reduction from the NP-complete Partition problem
(construct a BPP instance with c = half the total weight; a hypothetical
algorithm beating 3/2 could distinguish OPT=2 from OPT≥3, solving Partition
in polynomial time). Notes research since has focused on the *asymptotic*
WCPR r∞(A) (worst ratio for OPT(I) ≥ some threshold k), citing the most
recent survey (Coffman et al. 2013, 200 references) plus newer results:
Dósa et al. on FFD, Rothvoß improving a classical Karmarkar–Karp result,
Balogh et al. closing a long-standing online-bin-packing question.

**3.2 Lower bounds.** **L1** (continuous relaxation, O(n) time):

```
L1 = ⌈ Σ_{j=1}^{n} w_j / c ⌉,     r(L1) = 1/2
```

**L2** (Martello & Toth): partition items by size relative to a parameter α
(0 ≤ α ≤ c/2) into J1 = {wⱼ > c−α}, J2 = {c−α ≥ wⱼ > c/2}, J3 = {c/2 ≥ wⱼ ≥
α}; each item in J1∪J2 needs its own bin, and no J3 item fits alongside a J1
item, giving

```
L(α) = |J1| + |J2| + max(0, ⌈(Σ_{j∈J3} w_j − (|J2|c − Σ_{j∈J2} w_j)) / c⌉)
L2 = max{ L(α) : 0 ≤ α ≤ c/2, α integer },  computed in O(n log n), r(L2) = 2/3
```

**Property 2** (with proof, mirroring Property 1's Partition reduction): "No
lower bound, computable in polynomial time, for the BPP can have a WCPR
greater than 2/3 unless P = NP" — so L2 is provably best-possible for
poly-time lower bounds, exactly as FFD/BFD are best-possible upper-bound
heuristics. Notes generalizations with better *practical* (not
worst-case) performance: L2LLM (Labbé et al.), Chen & Srivastava's bound,
theoretical study by Elhedhli; Bourjolly & Rebetez showed L2LLM's asymptotic
WCPR is r∞ = 3/4. **L3** (Martello & Toth): iteratively reduces the instance
and re-invokes L2; O(n³) time, asymptotic WCPR r∞(L3) = 3/4 (proved by
Crainic et al.). Also surveys **dual feasible functions** (Johnson's
original concept, extended by Fekete & Schepers): a function u(x) is dual
feasible if Σx∈S x ≤ 1 ⟹ Σx∈S u(x) ≤ 1 for any finite set S, so any bound
computed over transformed weights u(w) remains valid for the original
weights — gives a worked example U^(α)(w′) that recovers L2 as a special
case when maximized over α. Notes "fast" (O(n log n)) lower bounds by Chao
et al. and Crainic et al., and improvement techniques (if l bins is proven
infeasible, l+1 is valid) by Dell'Amico & Martello, Alvim et al., Haouari &
Gharbi, Jarboui et al.

**3.3 Heuristics and metaheuristics.** Explicitly scoped as secondary to
this survey's main exact-algorithm focus, but reviewed "for the sake of
completeness." **Heuristics**: Eilon & Christofides (BFD + reshuffle
routine, "the first relevant contribution"); Roodman (greedy + local
search for CSP variants); Vahrenkamp (random search); **Wäscher & Gau** —
studied rounding-based heuristics on instances from their own **CUTGEN**
generator, which "creates CSP instances depending on five parameters:
number of item types, minimum and maximum weight, bin capacity, and average
demand" (the generator underlying the Wäscher/Schwerin instance families in
Nikola's benchmark set); Gupta & Ho (minimize unused capacity, beats
FFD/BFD at higher CPU cost); Mukhacheva et al. (modified FFD, later
embedded in the Belov & Scheithauer exact algorithm); Osogami & Okano,
Bhatia et al., Kim & Wy, Fleszar & Charalambous (various local-search/
item-exchange modifications); Lewis (hill-climbing via item exchange).
**Metaheuristics**, grouped by paradigm: *Simulated annealing/Tabu search* —
Kämpke's classical SA, Loh et al.'s "weight annealing" variant, Scholl et
al.'s Tabu search embedded in BISON (§5.1), Alvim et al.'s Tabu-search
hybrid. *Population-based algorithms* — the key passage for Nikola's
related work:

> "Probably, the first genetic approach to the BPP is the one by Falkenauer
> and Delchambre [58]: they showed that the classical genetic approach
> cannot work efficiently for certain kinds of problems (like the BPP), and
> presented a variant (the grouping genetic algorithm) capable of producing
> a good computational behavior. Falkenauer [57] improved this method
> through hybridization with the dominance criterion by Martello and Toth
> [106]..., and proposed a set of benchmark instances that was later
> adopted by many authors for computationally testing BPP algorithms.
> Although Gent [68] showed that the majority of them are very easy, these
> instances were used, e.g., for testing the genetic approaches by Reeves
> [115], Bhatia and Basu [16], Singh and Gupta [138], Ülker et al. [143],
> and Stawowy [140]." (§3.3)

Continues: other GAs by Poli et al. and Rohlfshagen & Bullinaria; "a very
effective genetic algorithm... proposed by Quiroz-Castellanos et al."; ant
colony (Levine & Ducatelle); evolutionary programming for CSP variants
(Liang et al.). *Hyper-heuristics*: Ross et al. (GA + hyper-heuristics),
López-Camacho et al., Sim et al., Burke et al. (evolutionary algorithms +
hyper-heuristics), Bai et al. (SA hyper-heuristic), Sim & Hart (genetic
programming as a generative hyper-heuristic). *Other*: Fleszar & Hindi
(variable neighborhood search, modifying Gupta & Ho's heuristic);
Gómez-Meneses & Randall (hybrid extremal optimization + local search).

### 4. Pseudo-polynomial formulations

**4.1 Considerations on the basic ILP model.** The textbook model (1)–(5)
"involves a polynomial number of variables and constraints but is not very
efficient in practice." Symmetry-breaking additions: yᵢ ≥ yᵢ₊₁ (bins used in
increasing index order); xᵢⱼ = 0 for i > j+1 (item j can only go in one of
the first j+1 bins, since there's always an optimal solution respecting
this); tightened relaxation via xᵢⱼ ≤ yᵢ; plus knapsack-polytope-derived
cover inequalities. Despite these, "the computational behavior of model
(1)–(5) remains quite poor" — motivating pseudo-polynomial alternatives,
whose *drawback* is that variable count depends on bin capacity, not just
item count, but which give a strictly stronger LP relaxation.

A running **Example 1** is used throughout §4: BPP instance n=6, c=9, w =
(4,4,3,3,2,2); equivalent CSP instance m=3, c=9, w=(4,3,2), d=(2,2,2);
optimal value 2 (each bin holds one item of weight 4, 3, and 2).

**4.2 One-cut formulation** (Rao 1976 / Dyckhoff, independently). Models the
physical cutting process: a bin/residual of width p is cut into a left
piece (item) of width q and a right residual of width p−q. Defines R (set
of feasible residual widths), demand levels Lq, and sets A(q)/B(q)/C(q)
tracking which widths can produce/leave/be-cut-from a piece of width q.
With xₚq = number of times a bin/residual of width p is cut into pieces q
and p−q, the ILP (eq. 13–15) minimizes Σq∈W x_cq subject to a
flow-conservation-like demand constraint. Worked through fully on Example
1 (R = {2,3,4,5,6,7,9}; optimal solution x₉,₄=2, x₅,₃=2 — cut two width-4
items from two bins, then two width-3 items from the resulting residuals,
leaving two width-2 items from what's left). Model has **O(mc) variables,
O(c) constraints**. Quotes Stadtler's comparison to column generation: "The
set of real world cutting stock problems solvable by the one-cut model (of
Rao and Dyckhoff) is only a subset of those which could be tackled by the
column generation approach (of Gilmore and Gomory)."

**4.3 DP-flow formulation** (Cambazard & O'Sullivan). States are (j,d) —
"decisions have been taken up to item j and result in a partial bin filling
of d units" — with arcs representing pack/don't-pack decisions for the next
item; a bin-filling is a path from (0,0) to (n+1,c); "loss arcs" from layer
n to the terminal node capture unused capacity. The BPP becomes a
min-cost-flow-style ILP (eq. 16–19) selecting the minimum number of
node-disjoint-in-flow paths covering all items. **O(nc) variables and
constraints.** Developed originally for BPP but extensible to CSP.

**4.4 Arc-flow formulations** (Valério de Carvalho). Obtained by *vertically
shrinking* the DP-flow graph — merging all states with equal partial bin
filling into one node — so vertical arcs disappear and parallel slanting
arcs merge. Gives an ILP (eq. 20–23) with **O(mc) variables, O(m+c)
constraints**, and proves its LP relaxation has "the same solution value as
the Gilmore and Gomory... model" (i.e. matches the strong column-generation
bound). Notes Valério de Carvalho's own refinements (only create nodes
corresponding to feasible weight combinations) and Brandão & Pedroso's
newer three-index multi-graph variant (a per-item-type "level," CSP-
generalized version of DP-flow) reduced via graph compression — "the
overall code proved to be very efficient on benchmark instances" (this is
the VPSOLVER code, later shown to be one of the two best performers in
§7).

### 5. Enumeration algorithms

**5.1 Branch-and-bound.** First BPP B&B: Eilon & Christofides, adapting
Balas's 0-1 LP enumerative scheme; initialized via BFD + reshuffle,
LP-relaxation lower bounds; "could only solve instances of very moderate
size." **MTP** (Martello & Toth): the historically dominant exact code,
"the standard reference for the exact solution of the BPP" through the
1990s. Defines the **dominance criterion** underlying its reduction
procedure (**Property 3**): a feasible set F1 (items summing ≤ c)
dominates F2 if there's a partition of F2 and a subset of F1 matching each
part by weight-majorization — meaning F1 can always replace F2 in an
optimal solution. The Martello-Toth Reduction Procedure (MTRP) restricts
this check to feasible sets of cardinality ≤3, O(n²) time, and is also used
iteratively (O(n³)) to compute the improved lower bound L3 (§3.2). MTP
itself sorts items by non-increasing weight, indexes bins by
initialization order, and does depth-first branch-decision search (each
node assigns the next item to an already-open bin or a new one). **BISON**
(Scholl et al.): built on MTP's tools plus new lower bounds and a Tabu
Search for strong incumbents. Schwerin & Wäscher later improved MTP's
competitiveness against BISON via a column-generation-based lower bound.
Mukhacheva et al. proposed a pattern-oriented B&B for both BPP and CSP;
Korf's "bin completion" algorithm (improved by Schreiber & Korf) branches
by assigning a whole feasible *set* to a bin at each node rather than one
item at a time. Notes that from the late nineties, branch-and-price (§6)
overtook branch-and-bound as "the most popular choice for the exact
solution of the BPP."

**5.2 Constraint programming approaches.** Shaw introduced a dedicated CP
constraint (later implemented as IloPack in CPLEX's CP Optimizer) using
pruning/propagation rules built on lower bound L2; later improved by
Cambazard & O'Sullivan (integrating §4's pseudo-polynomial formulations into
the CP approach), Dupuis et al. (using L2LLM plus an added reduction), and
Schaus et al. (a cardinality-based filtering rule).

### 6. Branch-and-price

**6.1 Set covering formulation and column generation.** Based on Gilmore &
Gomory's seminal set-covering CSP model: enumerate all feasible *patterns*
p (item combinations fitting in one bin), variable yₚ = times pattern p is
used, minimize Σyₚ subject to each item type's demand being covered (eq.
24–26). Since the pattern count is exponential, **column generation** is
used: solve a restricted master problem (RMP) over a small pattern subset,
extract dual variables πⱼ, and solve a pricing/slave sub-problem — an
**unbounded knapsack problem** maximizing Σπⱼvⱼ subject to Σwⱼvⱼ ≤ c (eq.
30–32) — to find a new column with negative reduced cost, iterating to LP
optimality. Notes the set-partitioning variant (equality constraints)
yields the same optimal value, since excess pattern copies can always be
trimmed. Surveys **dual-cut acceleration** techniques (Valério de Carvalho;
Ben Amor et al.; Clautiaux et al., who add dual cuts *and* tighten dual
variable bounds to stabilize convergence) and alternative solution methods
for the RMP's LP relaxation (Briant et al.'s bundle-method comparison;
Kiwiel's inexact bundle method + rounding heuristic; Elhedhli & Gzara's
Lagrangian-relaxation-based heuristic).

**6.2 Integer round-up property.** Defines **IRUP**: an instance has it if
⌈L_LP⌉ = z_opt (the rounded-up LP-relaxation value of the set-covering
model equals the true optimum). Conjectured universal in the 1970s;
disproved in the 1980s — Marcotte's first counterexample (n=24, c=3,397,386,255)
and Chan et al.'s smaller one (n=15, c=1,111,139) — in both cases "the gap
between the rounded up lower bound and the optimal solution is exactly one
bin," motivating the weaker **MIRUP** conjecture (z_opt − ⌈L_LP⌉ ≤ 1 always)
— which "to the best of our knowledge... is still open both for the BPP and
the CSP." Reviews the Non-IRUP-instance-construction literature: Kartak
(sufficient conditions + checking algorithm); **Schoenfield**, via "a huge
number of computational tests on randomly generated instances," created a
set of hard instances (some with z_opt − L_LP > 1) — this is the direct
origin of the **Hard28/Schoenfield** family in Nikola's benchmark set;
Rietz & Dempe (perturbation-based construction); **Caprara et al.**
produced a large Non-IRUP set via a BPP–edge-coloring relationship, with
the smallest instances at n=13, c=100 ("showing that Non-IRUP instances may
also appear in practical contexts"), plus a general IRUP→Non-IRUP
transformation method — this benchmark ("B" in the paper's own notation) is
the direct basis of the ANI/AI instances built in §7.1; Kartak et al.
(enumerative method, proving IRUP holds for n≤9 and producing Non-IRUP
instances at n=10); Eisenbrand et al. and Newman et al. connecting MIRUP to
Beck & Sós's three-permutation discrepancy-theory conjecture.

**6.3 Branch(-and-cut)-and-price algorithms.** Surveys the evolution of
practical B&P for BPP/CSP: **Vance et al. (1994)**, the first BPP B&P,
using Ryan & Foster's classical set-partitioning branching rule (force a
fractionally-co-packed item pair together or apart) plus Farley's
early-termination bound; Scheithauer & Terno's MIRUP-oriented hybrid
(reduce via rounded-down LP solution, then heuristics, then B&B with
pricing on the residual); Vance's proof that Dantzig-Wolfe decomposition of
the basic CSP model (6)-(10) yields exactly the set-covering model,
enabling tailored branching; **Valério de Carvalho**'s column generation
built on the *arc-flow* formulation instead of Gilmore-Gomory (branches on
fractional flow variables, slave = a longest-path DP); Vanderbeck's
branch-on-column-set rule (a true Branch-and-Cut-and-Price); Degraeve &
Schrage (branch on a fractional pattern), improved by Degraeve & Peeters
(heuristics, pruning, sub-gradient acceleration); Scheithauer et al.'s
cutting-plane approach (Chvátal-Gomory cuts closing the LP-IP gap),
improved by Belov & Scheithauer and finally embedded into a full B&P — this
is the lineage of the **BELOV** code (branches on the pattern variable
closest to 0.5), later shown in §7 to be the strongest overall performer;
Belov et al.'s attempt to combine Chvátal-Gomory cuts with arc-flow
formulations "did not prove to be very effective."

### 7. Experimental evaluation

**7.1 Benchmarks.** Three benchmark classes, all downloadable from the
dedicated web page that would become BPPLIB. **Literature instances**:
Falkenauer [57] — "Falkenauer U" (uniform sizes, n between 120–1000,
c=150) and **"Falkenauer T"** — precisely described here as "the so-called
triplets, i.e., groups of three items (one large, two small) that need to
be assigned to the same bin in any optimal packing" (n between 60–501,
c=1000); Scholl et al. — three uniform sets ("Scholl 1/2/3", n 50–500,
capacities 100–150 / 1000 / 100,000 respectively); Wäscher & Gau — 17 hard
instances (n 57–239, c=10,000); Schwerin & Wäscher — two 100-instance sets
(n=100/120, c=1000); **Schoenfield** — 28 "Hard28" instances (n 160–200,
c=1000). **Randomly generated instances**: same construction as later
reused in BPPLIB (2018) — n ∈ {50,...,1000}, c ∈ {50,...,1000}, wmin ∈
{0.1c, 0.2c}, wmax ∈ {0.7c, 0.8c}, 10 instances per quadruplet, 3840 total.
**Difficult instances** (designed here specifically because "all the above
instances can be solved in less than 10 minutes by at least one of the
softwares... tested"): **augmented Non-IRUP (ANI)** instances built from
Caprara et al.'s 15-item Non-IRUP base set B (each satisfying Σwⱼ = 3c,
L_LP=3, optimum=4) by iteratively adding item triplets summing to c under a
non-completability condition (doubling capacity/weights when the condition
can't be met); five 50-instance sets with n ∈ {201,402,600,801,1002} and
capacity caps {2500, 10000, 20000, 40000, 80000}. **Augmented IRUP (AI)**
instances are the "easier" counterpart: split one of the 15 original items
in two so the Non-IRUP structure is lost — "for the AI instances, all bins
are completely filled, so the continuous relaxation provides the optimal
solution value, and the only difficulty is to construct a feasible solution
having the same value."

**7.2 Computer codes.** Twelve total, tested wherever source was available
or easily implementable: branch-and-bound (MTP, BISON, CVRPSEP); branch-
and-price (VANCE, BELOV, SCIP-BP); pseudo-polynomial (ONECUT, ARCFLOW,
DPFLOW, VPSOLVER); plus BASIC ILP (the textbook model 1–5) and CSTRPROG (a
simple CP implementation using IloPack + an FFD-based search phase) as
weak-baseline comparators. All CPLEX-based codes used CPLEX 12.6.0;
VPSOLVER used Gurobi 5.6; SCIP-BP used SCIP 3.0.2.

**7.3 Experiments.** Hardware: Intel Xeon 3.10 GHz, 8GB RAM, 4 cores, single
core per run. Pre-filtering via BFDL2 (BFD upper bound + L2 lower bound) —
only non-coincident instances tested. **Table 1** (1-min limit, literature
instances) headline numbers: BELOV solves 953/976 (avg gap 0.0), VPSOLVER
928/976, ARCFLOW 895/976, VANCE 883/976; the old branch-and-bound codes
struggle badly on Falkenauer T and Hard28 (MTP: 6/80 and 0/28 respectively;
CVRPSEP: 0/80 and 0/28). **Table 3** (10-min limit, four best codes only):
BELOV solves **all 976**, VPSOLVER 968 (99%), ARCFLOW 938 (96%), BISON 797
(82%) — "instances with very large capacity values turned out to be
particularly hard for ARCFLOW." Four numbered observations (§7.3): (1)
among old B&B codes, only BISON solves many instances; (2) VANCE and
especially BELOV do well among B&P, SCIP-BP is not competitive — BELOV's
only real weakness is Falkenauer T, "probably because of the small
capacities involved" (which favor pseudo-polynomial models instead); (3)
ARCFLOW and VPSOLVER are the best pseudo-polynomial codes; ONECUT, despite
its 1970s vintage, is competitive and shares ARCFLOW's LP-relaxation
quality; (4) BASIC ILP and CSTRPROG are, as expected, weak. **Random
instances** (Tables 4–11): BELOV solves all 2901 non-trivial instances
within a minute; VPSOLVER trails by only 10; SCIP-BP is only competitive
for n≤100; branch-and-price performance is unaffected by capacity while
pseudo-polynomial-model performance (ARCFLOW, DPFLOW) is capacity-
sensitive. **Item multiplicity** (μ = n/m, Table 10): CSP-oriented methods
(BELOV, ONECUT, ARCFLOW, VPSOLVER) are essentially unaffected by μ, but
BPP-oriented methods degrade sharply as μ grows — SCIP-BP solves all
instances at μ≤2 but "less than one tenth of those with μ≥10." **Difficult
ANI/AI instances** (Tables 12–13, 1-hour limit): even BELOV — which closed
every other benchmark — "was unable to solve them to proven optimality" at
the larger sizes (0 solved at n=1002 for every code tested); AI instances,
despite their easier LP structure, "also look quite hard" without a
specially tailored heuristic. **Table 14** (CPLEX version history on
ARCFLOW's ILPs, 20 selected random instances, n 300–1000): dramatic
improvement from CPLEX 6.0 (1998, 13/20 solved in 10 min) to CPLEX 12.6.0
(2013, 20/20) — directly explaining why pseudo-polynomial models, long
dismissed as "too theoretical," are competitive today purely due to ILP
solver maturation, not algorithmic change.

**Overall verdict** (§7.3, closing paragraph): "BELOV and VPSOLVER are the
best" algorithms tested; "ARCFLOW can be seen as a reasonable compromise
between simplicity and performance"; Basic ILP/SCIP-BP suit only small
instances; MTP/CVRPSEP/BISON are viable if one wants to avoid commercial/
free ILP solvers entirely; CSTRPROG is inefficient but flexible for extra
side-constraints; ONECUT is "competitive with much more recent approaches"
despite its age; DPFLOW is "mainly [of] theoretical interest" but simple to
understand; VANCE is mainly of historical interest but "has an acceptable
performance."

### 8. Conclusions

Frames the survey as covering "the last fifty years" of BPP/CSP exact
methods. Explicitly flags open research directions: the AI/ANI instances
remain unsatisfactorily solved "even in the case of moderate sizes"; the
improving power of ILP solvers may re-open pseudo-polynomial methods as an
active research direction; and, theoretically, "the MIRUP conjecture...
is still open." Acknowledgements credit Armin Scholl (BISON), Gleb Belov
(experiment assistance), and IBM's CPLEX team (Table 14 experiments).

## Citable specifics

> "The exact WCPR of FF and BF has been an open problem for forty years,
> until recently Dósa and Sgall [46,47] proved that r(FF) = r(BF) = 17/10."
> (§3.1)

> "No polynomial-time approximation algorithm for the BPP can have a WCPR
> smaller than 3/2 unless P = NP." (§3.1, Property 1, proved via reduction
> from Partition)

> "No lower bound, computable in polynomial time, for the BPP can have a
> WCPR greater than 2/3 unless P = NP." (§3.2, Property 2)

> "The BPP can be seen as a special case of the CSP in which dⱼ = 1 for all
> j. In turn, the CSP can be modeled by a BPP in which the item set includes
> dⱼ copies of each item type j." (§2, Formal statement)

> "Probably, the first genetic approach to the BPP is the one by Falkenauer
> and Delchambre [58]: they showed that the classical genetic approach
> cannot work efficiently for certain kinds of problems (like the BPP), and
> presented a variant (the grouping genetic algorithm) capable of producing
> a good computational behavior." (§3.3, Heuristics and metaheuristics —
> the field's own historical framing of the GGA's origin)

> "Falkenauer [57]... proposed a set of benchmark instances that was later
> adopted by many authors for computationally testing BPP algorithms.
> Although Gent [68] showed that the majority of them are very easy, these
> instances were used, e.g., for testing the genetic approaches by Reeves
> [115], Bhatia and Basu [16], Singh and Gupta [138], Ülker et al. [143],
> and Stawowy [140]." (§3.3 — an important caveat: the widely-cited
> Falkenauer benchmark set is *not* uniformly hard, per an independent
> assessment by Gent)

> "Falkenauer [18/57]: 80 instances... The second class ('Falkenauer T')
> includes the so-called triplets, i.e., groups of three items (one large,
> two small) that need to be assigned to the same bin in any optimal
> packing." (§7.1 — the precise construction of the triplet/"perfect
> packing" instances in Nikola's `BPPLIB/` submodule)

> "For the AI instances, all bins are completely filled, so the continuous
> relaxation provides the optimal solution value, and the only difficulty
> is to construct a feasible solution having the same value." (§7.1)

> "BELOV and VPSOLVER are the best [algorithms]. As both use quite complex
> tools, ARCFLOW can be seen as a reasonable compromise between simplicity
> and performance." (§7.3, closing verdict)

> "It is indeed known... that, on specific instances, an older version of
> CPLEX can beat a newer one." (§7.3, Table 14 discussion, on the counter-
> intuitive occasional regressions across CPLEX versions)

> "There are still benchmarks (the AI and the ANI instances) which are not
> satisfactorily solved by the best available algorithms, even in the case
> of moderate sizes... a relevant issue concerns the MIRUP conjecture, which
> is still open." (§8, Conclusions)

## How it helps Nikola's thesis

- The strongest single source for an up-to-date **Theoretical Background**
  section (Ch1/Ch2) on worst-case bounds and lower bounds: it both updates
  Johnson et al. (1974)'s 1970s asymptotic results with the modern *exact*
  proof (Dósa & Sgall, r(FF)=r(BF)=17/10 exactly) and gives a precise,
  citable computable lower bound (L2, O(n log n), WCPR 2/3) Nikola could
  optionally use to evaluate how close his GA's solutions get to a
  computable bound on instances where the true optimum is unknown.
- **§3.3's population-based-algorithms paragraph is a ready-made,
  authoritative Related Work anchor**: it independently corroborates the
  historical account in `falkenauer-delchambre-1992.md` and
  `falkenauer-1996.md` (first GA, then hybridized with Martello-Toth
  dominance), and lists five further genetic-approach papers (Reeves,
  Bhatia & Basu, Singh & Gupta, Ülker et al., Stawowy) as concrete
  candidates if Nikola wants to expand his GA-related-work citations
  beyond Falkenauer.
- **The Gent [68] caveat that most Falkenauer benchmark instances are "very
  easy"** is an important nuance Nikola should be aware of and can address
  directly in Ch5: it means strong GA performance on the easy Falkenauer_U
  set is a weaker result than performance on Falkenauer_T (triplets),
  Hard28, or Wäscher — all flagged elsewhere as deliberately harder
  (non-IRUP / perfect-packing) — giving Nikola independent justification
  for weighting his results discussion toward the harder instance families.
- The precise **IRUP/MIRUP/Non-IRUP** definitions and history (§6.2) —
  including that Schoenfield's Hard28 and Caprara et al.'s edge-coloring-
  based instances are the direct ancestors of the "non-IRUP" flag on
  several families in Nikola's own `BPPLIB/` submodule — gives Ch1/Ch3
  precise vocabulary for *why* certain benchmark families are harder than
  others, beyond simply "more items."
- **Table 14's CPLEX-version comparison** is a nice illustrative point for
  a methodology discussion: it shows empirically that solver/hardware
  maturation alone can flip an algorithm from "impractical" to
  "competitive" over 15 years — worth a cautionary footnote if Nikola ever
  compares his GA's runtime against decades-old heuristic timing figures
  (e.g. Falkenauer & Delchambre 1992's "about a minute on a 4D35 Silicon
  Graphics, 33 MIPS").
- The §7 experimental results (BELOV/VPSOLVER dominance; ANI/AI instances
  still unsolved even by the best exact solvers at moderate size) are good
  context for Ch5's framing of *why* heuristic/metaheuristic approaches
  (including Nikola's GA) remain worth studying: even purpose-built exact
  solvers cannot close every benchmark instance within reasonable time,
  and Nikola's GA is not positioned as a competitor to these exact methods
  but as a practical alternative measured against known-best values from
  `Solutions.xlsx`.
