> **Study notes only — not thesis prose.** This is a paraphrased digest for
> Nikola's own reading. Any idea used in the actual thesis must be
> rewritten entirely in his own words and cleared by the `plagiarism-guard`
> subagent; see `literature/digests/README.md`.

# Falkenauer (1996) — A Hybrid Grouping Genetic Algorithm for Bin Packing

**Zotero key:** `2CV824V5`
(Note: the item key given in the original task, `T6KJYXY8`, currently points
to a **trashed duplicate** of this same reference in Zotero — see the dedupe
note in `CLAUDE.md`. `2CV824V5` is the live, non-trashed item this digest was
pulled from; same title/DOI/journal, so no risk of citing a different work.)

## Full citation

Falkenauer, E. (1996). A Hybrid Grouping Genetic Algorithm for Bin Packing.
*Journal of Heuristics*, 2(1), 5–30. https://doi.org/10.1007/BF00226291

(26 journal pages, pp. 5–30; no embedded PDF outline. Page numbers below are
cross-checked against the paper's own running-header page markers
["FALKENAUER" on verso pages, "A HYBRID GROUPING GENETIC ALGORITHM" on recto
pages] visible in the extracted text, so they should be reliable to within a
page; anything not directly confirmed against a marker is flagged "location
approx." One numbering quirk in the source: after §6.2 (BPRX crossover) the
mutation subsection is printed as "**4.3.** The mutation" — almost certainly
an OCR/extraction artifact for what is contextually **§6.3** (the paper's
real section 4 is the general, non-BPP-specific GGA description, already
concluded pages earlier). Section structure used below: 1. Introduction
[1.1 The bin packing problem, 1.2 The grouping problems], 2. Standard GA
operators and grouping problems [2.1 The encoding and redundancy, 2.2 The
crossover (2.2.1 Context insensitivity, 2.2.2 Schema disruption), 2.3 The
mutation], 3. Ordering GA operators and grouping problems [3.1 encoding/
redundancy, 3.2 crossover (3.2.1, 3.2.2), 3.3 mutation], 4. The grouping
genetic algorithm [4.1 encoding, 4.2 crossover, 4.3 mutation, 4.4
inversion], 5. The dominance criterion, 6. The hybrid GGA for bin packing
[6.1 The problem redefinition, 6.2 BPRX: the bin packing crossover with
replacement (6.2.1 mechanism, 6.2.2 rationale), 6.3 The mutation — mislabeled
"4.3" in the extracted text], 7. Experimental results [7.1 The setup, 7.2
Uniform item size distribution, 7.3 Triplets], 8. Conclusions,
Acknowledgments, Notes, References.)

## Overview

The definitive, extended journal treatment of the Grouping Genetic Algorithm
(GGA) for bin packing, building on the conference-length Falkenauer &
Delchambre (1992). Falkenauer systematically diagnoses why *both* the classic
Holland-style GA (item-per-gene encoding) *and* ordering/permutation GAs (the
family Nikola's thesis actually uses, decoded via First-Fit) perform poorly
on bin packing as a "grouping problem" — giving each its own dedicated
section with worked counterexamples — then proposes the group-based GGA
encoding and operators, explains Martello & Toth's dominance criterion for
BPP, and finally **hybridizes** GGA with a dominance-inspired local
optimization (into the "HGGA," Hybrid GGA), benchmarking extensively against
Martello & Toth's exact branch-and-bound MTP procedure on both "easy"
uniform-random instances and specially constructed "triplet" (perfect-
packing) instances. This is the single most detailed primary source for the
standard critique of permutation-GA + FF/BF-decoder approaches — i.e., the
approach Nikola's own thesis takes — making it essential reading before
writing any Related Work section that positions a permutation-GA method
against Falkenauer's own.

## Section-by-section walkthrough

### 1. Introduction (pp. 5–7)

**1.1 The bin packing problem** (p. 5) restates the BPP decision problem
(Garey & Johnson 1979 formulation: set O of item sizes, bin capacity C, bin
count N — does a partition into ≤N subsets exist?), its NP-hard
optimization counterpart, and gives FF/BF informally, noting BF "can... be
shown to perform as well (or as bad) as the FF, while being slower." Flags
Martello & Toth's (1990a) dominance-criterion-based reduction method
(discussed fully in §5) as "one of the best OR techniques for optimization
of the BPP to date."

**1.2 The grouping problems** (pp. 6–7) generalizes: BPP belongs to a
family of problems partitioning a set U into disjoint subsets, subject to
hard constraints, optimizing a cost function over valid groupings. Gives a
three-row table of example grouping problems (bin packing: hard constraint
= group-size-sum < C, cost = number of groups; workshop layouting: machine-
count-per-cell < C, cost = intercell traffic; graph coloring: no connected
nodes share a group, cost = number of groups/colors) — a clean illustration
that "grouping problems are characterized by cost functions that depend on
the *composition* of the groups... where one item taken isolatedly has
little or no meaning." Introduces GGA as a general paradigm (Falkenauer
1993, 1994) with the BPP application originating in Falkenauer & Delchambre
(1992); previews the paper's own structure (§2–3: weaknesses of standard/
ordering GAs; §4: GGA; §5: dominance criterion; §6: HGGA; §7: experiments;
§8: conclusions).

### 2. Standard GA operators and grouping problems (pp. 7–9)

**2.1 The encoding and redundancy** (p. 7) — one-gene-per-item encoding
(chromosome `ADBCEB`). Invokes the "minimal redundancy" representation
design principle (Radcliffe 1991): each solution should ideally map to
exactly one chromosome. The straightforward encoding violates this badly —
group *names* are arbitrary, so e.g. in graph coloring, `ABCADD` and
`CADCBB` encode the *same* coloring under different color-name choices —
and "the degree of redundancy... grows exponentially with the number of
groups," inflating the effective search space the GA must cover.

**2.2 The crossover** (pp. 8–9). **2.2.1 Context insensitivity** (p. 8) —
the paper's sharpest worked counterexample. Standard two-point crossover
applied to two chromosomes that encode the *identical* solution
(`ABCADD`/`CADCBB`, same coloring under relabeling) should, "in absence of
mutation," reproduce that same solution in the offspring. Instead:

```
A|BC|ADD  ×  C|AD|CBB  →  CBCCBB (one child)
```

"the resulting child above encodes a solution that has nothing in common
with the solution its parents encode: there are two groups instead of
four!" — i.e. standard crossover can *destroy* a solution's structure even
when recombining two encodings of the same solution, because a gene's
problem-level meaning depends on the whole chromosome's context, not just
its own value. **2.2.2 Schema disruption** (p. 8) — restates the general
principle that good groupings are necessarily "long schemata" under this
encoding, and standard crossover's disruption probability grows with
schema-defining length, so "once a good candidate is found, instead of
improving this solution, it works against its own progress toward
destruction of the good schemata."

**2.3 The mutation** (p. 9) — early mutation (`ABDBAC`→`ABDEAC`) can
usefully introduce a missing allele. But once large uniform groups have
formed (`AAABBB`→`AACBBB`), the mutated individual now contains "a group of
just one element," suffers "a steep loss of fitness," and "will be
eliminated with high probability... on the very next step of the
algorithm, yielding hardly any benefit for the genetic search." Conclusion:
"the classic mutation is too destructive once the GA begins to reach a
good solution of the grouping problem." Notes (end of §2.3) that simply
enlarging the mutated unit (acting on several genes at once) would just
disregard the chromosome's gene structure entirely — motivating §4's
actual fix instead.

### 3. Ordering GA operators and grouping problems (pp. 9–12)

Extends the *same* critique to permutation/ordering GAs — **the family
Nikola's own method belongs to** (permutation encoding, decoded via a
constructive heuristic).

**3.1 The encoding and redundancy** (pp. 9–10) — chromosome is a
permutation of items, decoded left-to-right into the first available group
(e.g. First-Fit-style). Worked example: 10 items numbered 0–9, chromosome
`0123456789` decoded as bins `{0,1,2,3}`, `{4,5,6,7,8}`, `{9}`; "any
permutation of the items having the same bin contents" (e.g.
`3210 145678 19` or `87645 11032 19`) "encodes the same solution" — so
permutation encodings are *also* exponentially redundant in the same way
item-per-gene encodings were.

**3.2 The crossover** (pp. 10–12). **3.2.1 Context insensitivity** — a
gene's contribution to the decoded solution "depends heavily on all the
genes that precede it," since decoding proceeds left-to-right. Worked
example: chromosome `0123456789` groups items 4–8 together, but
`9123456780` or `9012345678` — differing only in where item 9 sits at the
head — "most probably encode different solutions," since which items
already share a bin by the time item 4 is reached depends on what came
before. Walks through **Goldberg's PMX** (partially mapped crossover, "the
best-known ordering crossover") on a concrete example (parents
`0123|4567|89` and `9173|5482|60`, crossing section defining the mapping
4↔5, 5↔4, 6↔8, 7↔2), producing child `9123|4567|80`; notes that this child
differs from one parent only by a swap of the first/last genes, yet the two
parents "encode very different solutions of the BPP, one hav[ing] the
group 45678 together, the other not" — "the PMX transmits information that
more often than not gets a different meaning in the new chromosome." States
the general reason: "o-schemata... have little meaning in a grouping
problem: they are not building blocks capable of conveying useful
information," since "the only information useful in grouping problems
concerns the groups and these are obtained from a permutation of items in
a far too indirect way." Backs this theoretically *and* empirically, citing
**Hinterding & Khan (1994)**'s finding of *performance degradation with
increasing crossover rate* for an ordering GA on the cutting stock problem
— concluding "the best ordering GA for a grouping problem would be one with
no crossover!" **3.2.2 Schema disruption** — same disruption argument as
§2.2.2 applies, since permutation encoding also maps items onto genes.

**3.3 The mutation** (p. 12) — ordering-GA mutation (reordering genes) is
argued to be a lose-lose operator: "either not having any effect at all
because of the high redundancy of the encoding or being too destructive
because of its impact on all the items that map onto genes following the
modified site."

### 4. The grouping genetic algorithm (pp. 12–16)

**4.1 The encoding** (pp. 12–14). Diagnoses the shared root cause behind
§2 and §3's failures: chromosomes are "item oriented instead of being group
oriented," with "no structural counterpart" for groups even though the cost
function depends on group composition — explicitly framed as a call for
"the thesis of good building blocks" (Goldberg 1989), also raised
previously by Radcliffe and by Vose & Liepins but, per Falkenauer, largely
unheeded in prior grouping-problem GA literature (§2–3's citation list).
**The fix**: augment the item-part chromosome with a **group part**, one
gene per group, e.g. item part `012345` + group part `ADBCEB:BECDA` means
"item 0 is in the bin labeled A... the group part... expresses the fact
that there are five bins," with bin *names* irrelevant — only bin
*contents* matter (recoverable by lookup against the item part). "The
important point is that the genetic operators will work with the group
part of the chromosomes" — implying variable-length chromosomes (bin count
varies per individual). States the rationale explicitly: "in grouping
problems it is the groups that are the meaningful building blocks... the
very idea behind the GA paradigm is to perform an exploration of the search
space... [with building blocks that] simultaneously serve as estimators of
quality... If... the encoding scheme does not allow [this]... the GA
strategy inevitably fails."

**4.2 The crossover** (pp. 14–16) gives the **general GGA crossover
pattern** (any grouping problem): (1) select two random crossing sites in
each parent; (2) inject the first parent's crossing-section groups into the
second parent at its first crossing site; (3) eliminate now-duplicated
items from their *old* groups (altering those groups); (4) repair/adapt per
problem-specific hard constraints and cost function, optionally via local
heuristics; (5) repeat with parent roles swapped for the second child. This
is the general schema BPP's BPRX (§6.2) instantiates. Contains an important
**comparison to Reeves (1994)**, quoted in full below — Reeves's ordering
GA + FF/BF decoder is explicitly compared and found "substantially
inferior" to Falkenauer's own GGA results; the paper also critiques
Reeves's "reduction" mechanism (fixing sufficiently-filled bins and removing
their items from all individuals) as prone to getting "stuck in a local
optimum because it violates the search strategy of the GA" — specifically,
Holland's optimal sampling strategy requires continued (reduced-rate)
sampling of solutions *not* containing a promising building block, which
Reeves's hard fixation permanently forecloses. Also cites Falkenauer (1995)
comparing GGA against nine standard/ordering GAs (Jones & Beltramo 1991) on
the "equal piles" grouping problem (very similar to BPP): the best of the
nine (an ordering GA + greedy heuristic) beat the best standard GA, but
"was itself outperformed by a wide margin by the GGA."

**4.3 The mutation** (p. 16) — for grouping problems generally, three
strategies: create a new group, eliminate an existing group, or shuffle a
small number of items among groups (problem-specific implementation
details vary).

**4.4 The inversion** (pp. 15–16) — applied only to the group part
(`ADBCEB:BECDA`→`ADBCEB:CEBDA`); item part is untouched since group
membership doesn't depend on chromosome position. Purpose: bring promising
(well-performing) groups closer together to protect them from crossover
disruption, "mak[ing] the proliferation of the good group-schemata easier."

### 5. The dominance criterion (pp. 16–17)

Presents Martello & Toth's (1990a) key idea (Figure 1): given bins B1, B2,
if there's a subset {i1,...,il} of B2's items and a partition {P1,...,Pl}
of B1's items such that each iⱼ is "no bigger" than its corresponding Pⱼ,
then **B2 dominates B1** — any solution using B2 needs no more bins than
one using B1. An exact algorithm could repeatedly find and fix a globally
dominating bin, but this runs in exponential time; Martello & Toth's
practical approximation restricts the dominance check to item-sets of size
≤3, and when no dominating set is found, relaxes the problem (drops the
smallest unassigned item) and retries — used by them to compute BPP lower
bounds. Falkenauer repurposes this dominance *concept* (not the exact
algorithm) as a local-optimization step feeding the GGA (detailed in §6.2).

### 6. The hybrid GGA for bin packing (pp. 17–20)

**6.1 The problem redefinition** (p. 17). Repeats and extends the argument
(from Falkenauer & Delchambre 1992) that raw bin-count is unusable as a
search-guiding cost function ("a needle in a haystack" — a vivid phrasing
not present in the 1992 paper), then gives the fitness function:

```
f_BPP = (1/N) · Σ_{i=1..N} (F_i / C)^k
```

with N = bins used, Fᵢ = fill of bin i, C = bin capacity, k > 1 constant;
k=2 "gives good results" experimentally, while larger k risks premature
convergence ("local optima, due to a few well-filled bins, are too hard to
escape"). **New in this paper vs. the 1992 original**: a short formal
argument (pp. 17–18) that f_BPP doesn't introduce *spurious* optima beyond
the true minimum-bin-count optimum: comparing a true-optimal N-bin packing
P_N against any (N+1)-bin packing P_{N+1}, even in the most adverse case
(P_{N+1} has an "elite" of N full bins among N+1 total, vs. P_N's N equally
filled bins), algebra shows f_BPP(P_{N+1}) < f_BPP(P_N) whenever **k ≤ 2**
— so "the fBPP function defined above yields the same optima as the
original BPP objective" for the k values actually used.

**6.2 BPRX: the bin packing crossover with replacement** (pp. 18–20).
**6.2.1 The mechanism** — the worked crossover example (group parts
`ABCDEF`/`abcd`, crossing sites yielding `A|BCD|EF` and `ab|cd|`, injection
giving `AcdBCDEF`, duplicate-item elimination dropping bins that also held
injected items down to `AcdBD`) is identical in structure to the 1992
paper's BPCX. **The genuinely new contribution here**: before falling back
to plain FFD reinsertion (as in 1992), the hybrid algorithm first performs
a **local optimization inspired by Martello & Toth's dominance idea**: for
each bin already in the (partial) solution, check whether up to 3 of its
items can be *replaced* by 1–2 currently-unassigned items such that the
bin's fill increases without overflowing — and if so, perform the swap.
This has two benefits stated explicitly: (1) it directly improves the
target bin's fill; (2) since total item size is fixed, it frees up smaller
items elsewhere, indirectly making *other* bins easier to fill too. This
replacement process repeats until no further swap is possible, at which
point plain FFD completes the solution. **6.2.2 The rationale** (pp.
19–20) — frames this replacement stage as an *approximate, decentralized*
dominance search: Martello & Toth's exact dominance check is intractable
directly, and even their ≤3-item approximation requires an arbitrary
relaxation step when no dominance is found, with "little guarantee that
the relaxation... will preserve the global optimality" and no backtracking
once a bad relaxation is taken. The GGA sidesteps this because *whole
bins* are transmitted via crossover across the whole population: "each
improvement is usefully propagated throughout the population," which is
"analogous to testing the dominance of each bin under many different
relaxations" simultaneously — a bin surviving many generations unmodified
is (probabilistically) evidence it dominates most rivals built from its
items, without ever needing the expensive exact check. Further: two
disjoint (no-shared-item) bins from two independently-surviving
individuals can both be inherited by a BPRX child "without a need of new
verification of their dominance," since population-level selection has
already implicitly vetted each.

**6.3 The mutation** (mislabeled "4.3" in the extracted text, pp. 20)
— select a few bins/genes at random, eliminate them, and reinsert their
items using the *same* replacement-then-FFD machinery as the crossover
(§6.2.1).

### 7. Experimental results (pp. 20–27)

**7.1 The setup** (pp. 20–21). Benchmark: the Hybrid GGA (**HGGA**) vs.
Martello & Toth's exact **MTP** branch-and-bound procedure (chosen as "one
of the best methods for the bin packing problem to date"). GA
configuration: steady-state, order-based, population 100, tournament
selection (size 2); per generation, 50 individuals replaced via crossover
of the 50 best, 33 randomly selected for mutation, 25 for inversion.
Initial population: FF applied to 100 random item permutations — "the
heuristic is extremely fast, yielding a run time of 0.0 CPU seconds
whenever an optimal solution appeared already in the initial population."
HGGA coded in C++ on an R4000 Silicon Graphics workstation (IRIX 5.1); MTP
in Fortran (Martello & Toth's own code) on a Control Data CD4000 (also
R4000, EP/IX 2.1). MTP was capped at **1,500,000 backtracks** per instance
(raised if this cut MTP off before it had used as much CPU time as the
HGGA, to keep the comparison fair). Two experiment classes: (7.2) uniform-
random instances matching Martello & Toth's own hardest reported setup;
(7.3) specially constructed "triplet" instances to probe the HGGA's
*practical limits*.

**7.2 Uniform item size distribution** (pp. 21–24). Following Martello &
Toth's own finding that bin capacity 150 with item sizes uniform in
[20,100] is their hardest configuration, generated 20 instances each at
n = 120, 250, 500, 1000 items. Evaluation budget: 134,000 evaluations
(2,000 generations) for n=120/250; 335,000 (5,000 generations) for
n=500/1000. Results (Tables 1–4; Theo = theoretical minimum bins ⌈total
size / capacity⌉):

| n | MTP fully solved | HGGA reaches Theo | Notable result |
|---|---|---|---|
| 120 | 18/20 (2 unsolved after cutoff) | matches MTP on all 20 | MTP faster on the easy cases, but only marginally |
| 250 | 9/20 confirmed optimal | 17/20 confirmed optimal, matches MTP's count on remaining 3 | HGGA both better *and* faster from here up |
| 500 | 0/20 confirmed optimal | **all 20 at Theo** | MTP never reaches Theo; HGGA strictly dominates |
| 1000 | 0/20 confirmed optimal | **all 20 at Theo** | same; MTP solutions differ from HGGA's by ≥2 bins in nearly all cases |

For the two unsolved 120-item cases (runs 9, 20) neither algorithm found a
Theo-bin solution, but that Theo+1-bin solution "appeared already in the
initial population of the HGGA" — suggesting these instances' near-optimum
is "extremely easy to find, yet very hard to prove" have no better
solution exists. From 250 items up, "the explosive nature of MTP starts to
show," with the 500/1000-item results showing MTP solutions worse than
HGGA's "by two bins or more" in nearly every case — described as meaning
even an increased backtrack budget "would still end up with a solution
worse than the HGGA."

**7.3 Triplets** (pp. 24–27). Constructs the hardest known instance class:
items drawn from (0.25, 0.50) relative to unit bin capacity, so a
well-filled bin needs exactly **one big item (>1/3 bin) plus two small
items (<1/3 bin)** — any other combination (two big, or three small) wastes
space. Falkenauer explicitly draws an analogy (via Van Vliet 1993) to
**3-SAT** — the hardest fixed-arity SAT class, since 2-SAT is polynomial
while k-SAT gets easier as k grows past 3 — arguing triplets (3 items/bin)
are similarly the hardest BPP configuration, with instances having >3
items per bin becoming progressively easier to approximate. Construction
recipe for known-optimal instances (bin capacity 1000): draw the first
(large) item uniform in [380,490]; draw the second (medium) item uniform
in [250, s/2] where s is remaining space; the third item exactly fills the
bin. Generated 20 instances each at n = 60, 120, 249, 501 items (Tables
5–8), with evaluation budgets 67,000 (60/120 items) and 134,000 (249/501
items) evaluations. Results: MTP fully solved only **6 of 20** at n=60 and
**never finished** at any larger size within the 1,500,000-backtrack cap;
HGGA missed the optimum on 2 of the 20 n=60 instances (runs 8, 19 — where
even MTP fared one bin worse, suggesting the evaluation budget was simply
too tight there) but "from 120 items up, the HGGA fared better than the
MTP procedure in all respects... always found a globally optimal solution,
while the MTP never did," and was also consistently faster. Notes the
501-item triplets "constitute a limit to online performance of the HGGA
run on ordinary hardware" of the era — larger instances "will probably
have to be run overnight." All 160 instances used across §7.2–7.3 were
donated to Beasley's OR-Library — **this is the direct origin of the
Falkenauer_U (uniform) and Falkenauer_T (triplet) instance families in
Nikola's own `BPPLIB/` benchmark set.**

### 8. Conclusions (p. 28)

Restates the paper's contribution: the HGGA marries the GGA's structural
fit for grouping problems with Martello & Toth's dominance-inspired local
optimization, and "performs better than either of its components
separately," confirmed by extensive experiments against MTP. Draws out an
important methodological point: both HGGA and MTP embed the *same* local
techniques (FFD and the dominance criterion both appear in MTP; both
appear, differently, in HGGA), but differ in their *global* search
mechanism — GA crossover vs. branch-and-bound tree search — and HGGA's
demonstrated superiority is offered as evidence that "the search mechanism
of the GA will be recognized as a very viable instrument in searching the
vast search spaces of difficult problems." Stresses two necessary
ingredients for a high-performance GA: (1) an encoding/operators that fit
the problem's structure, and (2) a sophisticated local optimization —
"we believe that both are necessary." Notes the GGA+dominance marriage
should generalize to other grouping problems if a domain-appropriate
dominance notion can be found.

## Citable specifics

> "The bin packing problem (BPP) is defined as follows (Garey and Johnson,
> 1979): given a finite set 0 of numbers (the item sizes) and two constants
> C (the bin's capacity) and N (the number of bins), is it possible to pack
> all the items into N bins..." (p. 5, §1.1)

> "the resulting child above encodes a solution that has nothing in common
> with the solution its parents encode: there are two groups instead of
> four!" (p. 8, §2.2.1, Context insensitivity)

> "the classic mutation is too destructive once the GA begins to reach a
> good solution of the grouping problem." (p. 9, §2.3)

> "the only information useful in grouping problems concerns the groups and
> these are obtained from a permutation of items in a far too indirect
> way... the best ordering GA for a grouping problem would be one with no
> crossover!" (p. 12, §3.2.1 — citing Hinterding & Khan 1994's empirical
> finding that ordering-GA performance on the cutting stock problem
> *degrades* with increasing crossover rate)

> "The experimental results obtained with the ordering GA were inferior to
> the ones reported in Falkenauer and Delchambre (1992), which means that
> they are substantially inferior to the performance of the algorithm
> presented here." (p. 15, §4.2 — on Reeves's [1994] ordering-GA-with-
> FF/BF-decoder results; note this corrects an earlier draft of this digest
> that misattributed the quote to p. 14)

> "in grouping problems it is the groups that are the meaningful building
> blocks — that is, the smallest piece of a solution that can convey
> information on the expected quality of the solution they are part of...
> If, on the contrary, the encoding scheme does not allow the building
> blocks to be exploited... the GA strategy inevitably fails and the
> algorithm performs in fact little more than a random search." (pp.
> 13–14, §4.1)

> "We thus settled... for the following cost function for the BPP: maximize
> f_BPP = (1/N)·Σ(Fᵢ/C)^k... We have experimented with several values of k
> and found out that k = 2 gives good results. Larger values of k seem to
> lead to premature convergence of the algorithm." (p. 17, §6.1)

> "given the contents of two bins B1 and B2, if there exists a subset
> {i1,...,il} of items in B2 and a partition {P1,...,Pl} of items in B1
> such that for each item iⱼ there is a no-bigger corresponding Pⱼ, then B2
> is said to dominate B1." (p. 16, §5 — Martello & Toth's dominance
> criterion, paraphrased from Figure 1's caption/surrounding text)

> "Since whole bins are transmitted during a crossover, each improvement is
> usefully propagated throughout the population... which is analogous to
> testing the dominance of each bin under many different relaxations." (pp.
> 19–20, §6.2.2, Rationale)

> "From 120 items up, the HGGA fared better than the MTP procedure in all
> respects. It always found a globally optimal solution, while the MTP
> never did. The HGGA was also much faster." (p. 27, §7.3, Triplets —
> summarizing Tables 6–8)

> "The respective performances of the HGGA and the MTP procedure inspire an
> important conclusion. Both methods use the same local techniques (both
> FFD and the dominance criterion are embedded in MTP) but they use
> different global mechanisms for generating candidate solutions... Given
> the superiority of the HGGA demonstrated above, we hope that the search
> mechanism of the GA will be recognized as a very viable instrument in
> searching the vast search spaces of difficult problems." (p. 28, §8
> Conclusions)

## How it helps Nikola's thesis

- This is the single best source for a Related Work paragraph that honestly
  acknowledges the standard critique of permutation-GA + FF/BF-decoder
  approaches (**Nikola's own method's family**) — §3's context-insensitivity
  and schema-disruption arguments, backed by the empirical Hinterding & Khan
  citation, are a serious, citable challenge Nikola should address directly
  (e.g. by framing heuristic seeding as a way of front-loading good building
  blocks that crossover alone cannot reliably discover or preserve) rather
  than appear unaware of.
- The **§4.2 comparison to Reeves (1994)** — an ordering GA with an FF/BF
  decoder found "substantially inferior" to GGA — is a direct historical
  precedent for exactly the kind of algorithm family Nikola's thesis builds
  on, and a data point Nikola's own results (GA never losing to FF,
  strictly beating it on some instances per `CLAUDE.md`'s status notes)
  should be read against: Nikola's heuristic-seeded permutation GA
  arguably improves on Reeves's unseeded version in a way this paper
  doesn't get to test.
- The **k²-fill-ratio fitness function**, now with an added formal argument
  (pp. 17–18) that k≤2 preserves the original bin-count optimum, is a
  stronger, more complete citation for Ch2/Ch3 methodology than the 1992
  conference version alone — cite both together for the fitness function's
  full derivation-plus-correctness-argument.
- The **Falkenauer_U/Falkenauer_T instance construction** (§7.2–7.3) is the
  primary source for exactly how Nikola's own benchmark files were built —
  particularly the triplet-instance recipe (large item [380,490], medium
  item [250, s/2], third item fills the bin, unit capacity 1000) and the
  explicit 3-SAT-difficulty analogy, both useful for a Methods/Benchmark
  Description section explaining *why* triplet instances are the hardest
  BPP configuration rather than just asserting it.
- The **dominance criterion** (§5) and its use as an approximate local
  search inside crossover (§6.2) is a concrete illustration of hybridizing
  a metaheuristic with an OR technique — a useful contrast if Nikola
  discusses potential future extensions to his own GA (e.g. adding a
  local-search repair step beyond plain First-Fit decoding).
- The **§7 experimental protocol** (fixed backtrack/evaluation budgets,
  reporting both solution quality *and* time, using Theo = ⌈total size /
  capacity⌉ as a free lower-bound reference for "solved to proven
  optimality") is a useful methodological template for Nikola's own Ch5
  experimental write-up, particularly the practice of reporting the
  theoretical lower bound alongside actual results to identify which
  instances were solved *provably* optimally versus merely matched in bin
  count.
