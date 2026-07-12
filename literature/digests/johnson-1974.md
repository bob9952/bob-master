> **Study notes only — not thesis prose.** This is a paraphrased digest for
> Nikola's own reading. Any idea used in the actual thesis must be
> rewritten entirely in his own words and cleared by the `plagiarism-guard`
> subagent; see `literature/digests/README.md`.

# Johnson, Demers, Ullman, Garey & Graham (1974) — Worst-Case Performance Bounds

**Zotero key:** `2HXW5VW2`

## Full citation

Johnson, D. S., Demers, A., Ullman, J. D., Garey, M. R., & Graham, R. L.
(1974). Worst-Case Performance Bounds for Simple One-Dimensional Packing
Algorithms. *SIAM Journal on Computing*, 3(4), 299–325.
https://doi.org/10.1137/0203025

(27 PDF pages; no embedded outline — the paper's own section numbers are used
below: §1 Introduction, §2 First-fit and best-fit, §3 First-fit decreasing and
best-fit decreasing, §4 First-fit decreasing upper bounds, §5 Concluding
remarks, References.)

## Overview

This is the foundational paper proving worst-case approximation ratios for
the four simplest bin-packing heuristics: Next-Fit-style First-Fit (FF),
Best-Fit (BF), and their decreasing-order variants First-Fit-Decreasing (FFD)
and Best-Fit-Decreasing (BFD). Rather than average-case experiments, the
authors derive *exact* worst-case guarantees relative to the optimal number
of bins L*, and — crucially — construct matching adversarial instances
proving each bound is essentially the best possible for that algorithm
class, i.e. the bounds are tight, not just sufficient. The core technique
throughout is the "weighting function": assign each item a real-valued
weight w(x) depending only on its size such that (a) the total weight of the
list is within a fixed additive constant of the number of bins the algorithm
actually uses, and (b) no legally packed bin can hold elements totaling more
than a fixed constant r of weight — combining the two pins down the
algorithm's bin count in terms of L*. This is the paper the "no worse than a
small multiplying factor above optimal" folklore result in every later 1D-BPP
paper (Falkenauer 1996, Munien et al. 2020, Delorme/Iori/Martello 2016, etc.)
traces back to, and it is also where FF/BF/FFD/BFD are first given as
precise, numbered algorithms rather than informal descriptions.

## Section-by-section walkthrough

### §1. Introduction (pp. 299–301)

States the abstract problem: given a list L = (a₁, a₂, ..., aₙ) of reals in
(0, 1], place the elements into a minimum number L* of "bins" so that no
bin's contents exceed 1 (the normalized/unit-capacity formulation). Frames
this as a special case of the 1D cutting-stock problem and the
assembly-line-balancing problem, and lists concrete applications: table
formatting (packing fixed-size data fields into computer words), prepaging
(fitting program segments into memory pages), and file allocation (packing
files onto disk tracks). Notes the problem is NP-complete (citing Cook 1971
and Karp 1972), which motivates heuristics over exact search.

Gives the four algorithms as **numbered definitions** (this is the primary
citable source for their exact formal definitions):

- **Algorithm 1 (First-fit).** Bins B₁, B₂, ... start empty. Items a₁, ..., aₙ
  are placed in that order; to place aᵢ, find the *least* j such that Bⱼ is
  filled to level β ≤ 1 − aᵢ, and place aᵢ there.
- **Algorithm 2 (Best-fit).** Same placement order, but choose the least j
  such that Bⱼ's level β ≤ 1 − aᵢ *and* β is as large as possible (i.e. the
  fullest bin the item still fits in).
- **Algorithm 3 (First-fit decreasing).** Sort L into non-increasing order,
  then apply Algorithm 1.
- **Algorithm 4 (Best-fit decreasing).** Sort L into non-increasing order,
  then apply Algorithm 2.

Defines FF(L), BF(L), FFD(L), BFD(L) as the bin counts each algorithm uses on
L, and R_FF(k) = max over all lists with L* = k of FF(L)/L* (similarly for
R_BF, R_FFD, R_BFD). The four headline asymptotic results are stated as
equations (1)–(4):

```
lim_{k→∞} R_FF(k)  = 17/10
lim_{k→∞} R_BF(k)  = 17/10
lim_{k→∞} R_FFD(k) = 11/9
lim_{k→∞} R_BFD(k) = 11/9
```

The paper stresses these ratios are "achieved for small values of k" — the
worst case isn't just an asymptotic curiosity, it bites even on small
instances.

### §2. First-fit and best-fit (pp. 301–309)

Opens with a concrete example showing FF/BF's failure mode: a list built from
three "regions" of item sizes near 1/3 (region 1), 1/2 (regions 2 and 3);
region 1 items are ≈ 1/3+δ, later regions ≈ 1/2+δ. The optimal packing pairs
one item from each region per bin (L* = n/3), but FF/BF instead pack region-1
items six-to-a-bin, region-2 items two-to-a-bin, and region-3 items
one-to-a-bin, giving FF(L) = BF(L) = 5n/9, i.e. a ratio of 5/3 — already
worse than optimal, foreshadowing the tight bound.

**Theorem 2.1** (lower bound, pp. 302–303): for every k ≥ 1 there is a list L
with L* = k such that FF(L) = BF(L) > 1.7·L* − 8. The construction uses three
regions of ten-item "blocks" with sizes carefully perturbed around 1/6, 1/2,
and 1/2+δ so that FF/BF always fill certain bin combinations sub-optimally;
algebra on N (a multiple of 17) drives the ratio arbitrarily close to 17/10
from below. A follow-up remark shows the ratio 17/10 is exactly *attained*
(not just approached) for L* = 10 (FF(L) = BF(L) = 17) and L* = 20
(FF(L) = BF(L) = 34) — concrete small tight examples (Fig. 3).

**Theorem 2.2** (upper bound, p. 304): for every list L, FF(L) ≤ 1.7·L* + 2
and BF(L) ≤ 1.7·L* + 2. The proof uses only two shared structural properties
of FF/BF placement — (i) no element is placed in an empty bin unless it
fits in no nonempty bin, and (ii) if there's a unique nonempty bin of lowest
level, no element goes there unless it fits nowhere with a lower index — plus
a piecewise-linear weighting function W(β) (Fig. 2: slope 6/5 on [0, 1/6],
flat 0 on (1/6, 1/3], slope 6/5 again with offset on (1/3, 1/2], flat 7/10 on
(1/2, 1]) whose per-bin total is bounded (Claims 2.2.1–2.2.4) so that
summing over bins gives FF(L) ≤ W + 2 ≤ 1.7·L* + 2.

Combining Theorems 2.1–2.2 gives the **Corollary**: lim R_FF(k) = lim
R_BF(k) = 1.7 exactly, closing the gap between lower and upper bound
asymptotically (though the finite-k bounds still differ by additive
constants).

**Theorem 2.3** (restricted item sizes, pp. 307–308): if every item in L is
at most β (0 < β ≤ 1/2) and m = ⌊1/β⌋, then (i) there exist lists with
FF(L) ≥ [(m+1)/m]·L* − (1/m) and, symmetrically, (ii) FF(L) ≤
[(m+1)/m]·L* + 2 for all such lists — and the same holds with FF replaced by
BF. This generalizes the 17/10 bound: as β → 0 (m → ∞) the ratio bound tends
to 1, formalizing the intuition that FF/BF behave near-optimally when items
are all small relative to bin capacity. The **Corollary** states lim R_FF^β(k)
= lim R_BF^β(k) = 1 + 1/m — i.e. exactly (m+1)/m, tight.

### §3. First-fit decreasing and best-fit decreasing (pp. 308–316)

**Theorem 3.1** (lower bound, p. 308): for each k ≥ 1 there's a list L with
L* = k such that FFD(L) = BFD(L) > (11/9)·L* − 2. Construction: five "bands"
of items near 0.5+ε, 0.25+2ε, 0.25+ε, 0.25−2ε, and exactly 1.0, sized so
sorting-then-FF/BF still can't achieve the perfect pairing an optimal packing
finds (Fig. 4, "An 11/9 example"): L* = 9N+k but FFD(L) = BFD(L) = 11N+k.

**Theorem 3.2** (upper bound, the main FFD/BFD result): for all lists L,
FFD(L) ≤ (11/9)·L* + 4 and BFD(L) ≤ (11/9)·L* + 4. Together with Theorem 3.1
this gives lim R_FFD(k) = lim R_BFD(k) = 11/9 exactly.

The proof of Theorem 3.2 is split across the rest of §3 and all of §4,
described by the authors themselves as "considerably more complicated" than
the FF/BF proofs:

- **Lemma 3.3** (reduction lemma): if FFD(L) > r·L* + d (r, d ≥ 1), then
  deleting all elements of L not exceeding (r−1)/r still leaves
  FFD(L′) > r·L′* + d for the reduced list L′ — same for BFD. This lets the
  authors restrict attention to lists with all elements in (1/3, 1] when
  proving the 11/9 bound (since r = 11/9 ⟹ (r−1)/r = 2/11... the paper
  states the reduction targets (1/3,1]-type lists directly).
- **Theorem 3.4**: for lists L ⊆ [1/3, 1], BFD(L) ≤ FFD(L) always. Proved via
  an intricate simultaneous construction of the BFD packing alongside a fixed
  FFD packing PF, using a bijection f mapping not-yet-placed elements to
  still-open positions in PF and showing invariants (A)–(E) (1-1-ness,
  position/index monotonicity) are preserved element-by-element — a long,
  fully worked inductive proof (pp. 310–314, Claims 3.4.1–3.4.7). The point
  is that a single upper-bound proof for FFD then automatically transfers to
  BFD for this range.
- **Theorem 3.5**: the same domination BFD(L) ≤ FFD(L) holds for L ⊆ [1/2, 1]
  (stated without full proof, "a similar argument" per refs [6],[8]).
- Figures 5 and 6 show the ordering can reverse outside these ranges: there
  are lists with BFD(L)/FFD(L) = 10/9 and others with FFD(L)/BFD(L) = 11/10,
  so the domination results are genuinely range-dependent, not universal.

### §4. First-fit decreasing upper bounds (pp. 314–324)

Rather than prove Theorem 3.2 head-on, the authors first prove a structurally
similar but simpler warm-up result and then sketch how the same machinery
extends.

**Theorem 4.1**: for all lists L ⊆ (0, 1/2], FFD(L) ≤ (71/60)·L* + 5, and
this is tight — Fig. 8 exhibits lists (with all items < 1/2, five size-bands
near 5/29, 6/29, 8/29) where FFD(L) = 71N and L* = 60N.

The proof machinery, generalized later to Theorem 3.2, is genuinely novel and
worth noting structurally even without reproducing every algebraic step:

- Elements are classified by size into "k-pieces" — x is a *k-piece* if
  x ∈ (1/(k+1), 1/k]; 2-pieces are called B-pieces, 3-pieces C-pieces,
  4-pieces D-pieces, and items in (1/5, 1/4] are E-pieces. A "k-bin" is one
  whose largest element is a k-piece.
- A base weight w₁(x) = ⌈1/x⌉ − 1 is defined (so a k-piece has w₁ = 1/k).
  BASIC is the set of pieces that are the "type-defining" element of their
  bin under FFD; SURPLUS = L − BASIC is everything else.
- **Claim 4.2.1**: Σ_{BASIC} w₁(x) ≥ FFD(L) − Σ_{j=2}^{N−1} 1/j — i.e. w₁
  alone almost accounts for the FFD bin count, up to a harmonic-sum slack.
- Because w₁ alone "overcharges" (many lists have Σw₁(X) exceeding 71/60 for
  a legally packed bin, X's sum ≤ 1), a second function w₂ is introduced that
  *discounts* an element y's weight when paired with an x satisfying
  "relation k" (x is a k-piece and kx+y ≤ 1) — the discount corresponds to
  billing the excess weight to SURPLUS elements via an explicit "billing"
  bookkeeping scheme (Claim 4.2.2, an intricate combinatorial argument, pp.
  317–321) so that the lower bound proven for w₁(BASIC) transfers to the
  actual weight function W(X) = min over partitions into 1- and 2-element
  sets of the discounted total.
- **Lemma 4.2**: W(L) ≥ FFD(L) − N + 2 for any N ≥ 4, L ⊆ (1/N, 1/2].
- **Lemma 4.3**: for any X ⊆ (1/6, 1/2] with Σ(X) ≤ 1 (i.e. any legally
  packed bin's contents), W(X) ≤ 71/60. Proven by exhaustive case analysis
  over the finitely many possible "type configurations" of a bin (the paper
  works four representative cases explicitly, e.g. one B-piece + two
  C-pieces gives W(X) ≤ 71/60 exactly after applying a relation-2 discount,
  and notes "there are only two [configurations] which yield a bound of
  71/60; all other cases are bounded by 6/7" — leaving ~70 routine cases "to
  the ambitious reader").
- Combining Lemmas 4.2–4.3 with subadditivity of W over the optimal packing's
  bins gives Theorem 4.1 directly.
- **Corollary**: restricting further to items ≤ 1/3 tightens the bound to
  lim R_FFD(k) = 71/60 for that sub-range... and a related result for items
  in (1/4, 1/3]. (paper states two related asymptotic corollaries, (a) and
  (b), for different sub-ranges — location approx., algebra partially
  garbled by PDF-extraction artifacts on p. 322).
- **Theorem 4.4**: for items restricted to (1/5, 1/4], lim R_FFD(k) = 23/20 —
  another concrete restricted-range tight ratio.

The section closes by sketching (pp. 322–324) how the same weight-function
idea, now handling "A-pieces" (items > 1/3) via two auxiliary set-valued
functions f and g that track which non-A-bins and A-bins in the FFD packing
versus the optimal packing "correspond," completes the proof of the general
Theorem 3.2 (FFD(L) ≤ (11/9)L* + 4). The authors are explicit that they omit
the full details ("the amount of space required... prohibit us from giving
them here"), referring to Johnson's 1973 MIT doctoral thesis [8] for the
complete argument.

### §5. Concluding remarks (p. 324)

Frames FF/BF/FFD/BFD as special cases of broader algorithm classes studied
elsewhere by Johnson, and lists six open directions:

1. Worst-case behavior of FFD/BFD when items are restricted to an interval
   (α, β) for general 0 ≤ α < β < 1 (only FF/BF results were known at the
   time).
2. How the algorithms compare *pairwise* beyond FFD-vs-BFD (e.g. how large or
   small can BFD(L)/FFD(L) get for large L*?).
3. Trade-offs between algorithmic effectiveness and implementation
   efficiency (FFD/BFD are O(n log n); could O(n) or O(n²) algorithms do
   better?).
4. Bins of differing capacities and how bin-ordering affects performance.
5. Extension to two-dimensional bin packing.
6. **Expected (average-case) behavior** — the paper notes contemporaneous
   simulation results (refs [4], [8]) already indicated "FFD(L) and BFD(L)
   are almost always better than FF(L) and BF(L) for a random L, with BF
   occasionally slightly better than FF" — an early empirical note that
   presages exactly the kind of average-case experimental comparison
   Nikola's own thesis performs (GA vs. FF/BF/NF/Max-Rest and their
   decreasing variants on real benchmark instances, not just worst-case
   analysis).

## Citable specifics

> "We show that neither the first-fit nor the best-fit algorithm will ever
> use more than 1.7·L* + 2 bins. Furthermore, we outline a proof that, if L
> is in decreasing order, then neither algorithm will use more than L* + 4
> bins." (Abstract, p. 299)

> "given a list L = (a₁, a₂, ..., an) of real numbers in (0, 1], place the
> elements of L into a minimum number L* of 'bins' so that no bin contains
> numbers whose sum exceeds 1." (p. 299, problem statement)

> "ALGORITHM 1 (First-fit). Let the bins be indexed as B₁, B₂, ···, with
> each initially filled to level zero. ... To place aᵢ, find the least j
> such that Bⱼ is filled to level β ≤ 1 − aᵢ, and place aᵢ in Bⱼ." (p. 300,
> Algorithm 1 — and similarly Algorithms 2–4 immediately following)

> "lim_{k→∞} R_FF(k) = 1.7, lim_{k→∞} R_BF(k) = 1.7, lim_{k→∞} R_FFD(k) =
> 11/9, lim_{k→∞} R_BFD(k) = 11/9." (p. 301, equations (1)–(4), the four
> headline asymptotic ratios)

> "THEOREM 2.1. For every k ≥ 1, there exists a list L, with L* = k, such
> that FF(L) = BF(L) > 1.7L* − 8." (p. 302)

> "THEOREM 2.2. For every list L, FF(L) ≤ 1.7L* + 2 and BF(L) ≤ 1.7L* + 2."
> (p. 304)

> "there is a list L with L* = 10 and FF(L) = BF(L) = 17. ... There is also a
> list L having L* = 20 and FF(L) = BF(L) = 34." (p. 306 — concrete tight
> small examples for the 17/10 bound)

> "THEOREM 3.1. For each k ≥ 1, there exists a list L with L* = k such that
> FFD(L) = BFD(L) > (11/9)L* − 2." and "THEOREM 3.2. For all lists L,
> FFD(L) ≤ (11/9)L* + 4, and BFD(L) ≤ (11/9)L* + 4." (p. 308)

> "THEOREM 3.4. Suppose L ⊆ [1/3, 1]. Then BFD(L) ≤ FFD(L)." (p. 310)

> "THEOREM 4.1. For all lists L ⊆ (0, 1/2], FFD(L) ≤ (71/60)L* + 5." (p. 316)

> "Simulation results on FF, BF, FFD, BFD [4], [8] indicate that FFD(L) and
> BFD(L) are almost always better than FF(L) and BF(L) for a random L, with
> BF occasionally slightly better than FF." (p. 324, §5 Concluding remarks —
> an explicit early pointer toward average-case/empirical comparison, which
> is exactly the kind of study Nikola's thesis conducts on real benchmark
> instances)

## How it helps Nikola's thesis

This is the primary source for the classical worst-case bounds (17/10 for
FF/BF, 11/9 for FFD/BFD, plus the finer restricted-item-size bounds like
71/60 and 23/20) that belong in the Theoretical Background chapter (Ch1–Ch2)
before Nikola introduces his GA as an alternative to these heuristics — cite
it directly rather than only second-hand via later surveys (Munien 2020,
Delorme/Iori/Martello 2016). Specifically useful:

- The **precise, numbered algorithm definitions** (Algorithms 1–4, p. 300)
  give Nikola a clean, authoritative primary source for exactly how FF, BF,
  FFD, and BFD are defined — matching what `project/src/heuristic.py`
  implements, and letting Nikola state "as originally defined by Johnson et
  al. (1974)" rather than paraphrasing a textbook.
- The **tightness constructions** (Theorem 2.1's adversarial three-region
  list, the k=10/k=20 exact-ratio examples) are good illustrative material
  for a discussion of *why* FF/BF can misbehave on small or adversarial
  instances — directly relevant context for the Falkenauer "triplet"
  (perfect-packing) instances Nikola's `BPPLIB/` benchmark set includes,
  which are deliberately constructed in the same adversarial spirit.
  Falkenauer's difficult instances and Johnson et al.'s Theorem 3.1
  construction (perfect L* pairing vs. FFD/BFD's failure to find it) are
  conceptually the same trick — worth noting explicitly in Related Work.
- §5's closing remark that simulation already showed FFD/BFD beating FF/BF
  "almost always" in the average case is a nice historical anchor: it shows
  the average-case question Nikola's thesis answers experimentally (does a
  GA beat these heuristics on real instances, not just in the worst case)
  was recognized as open and interesting from this paper's very first
  publication.
- The 11/9 vs. 17/10 asymptotic separation is the original theoretical
  justification for why *sorting before packing* helps — directly
  underpinning why FFD/BFD matter as GA-seeding heuristics in Nikola's
  `_seed_orders`/`initialize_population` design (`project/src/ga.py`).
