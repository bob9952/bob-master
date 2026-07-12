> **Study notes only — not thesis prose.** This is a paraphrased digest for
> Nikola's own reading. Any idea used in the actual thesis must be
> rewritten entirely in his own words and cleared by the `plagiarism-guard`
> subagent; see `literature/digests/README.md`.

# Falkenauer & Delchambre (1992) — A Genetic Algorithm for Bin Packing and Line Balancing

**Zotero key:** `Y3A7G596`

## Full citation

Falkenauer, E., & Delchambre, A. (1992). A Genetic Algorithm for Bin Packing
and Line Balancing. In *Proceedings 1992 IEEE International Conference on
Robotics and Automation* (pp. 1186–1192). IEEE Computer Society Press.
https://doi.org/10.1109/ROBOT.1992.220088

(7 conference pages, pp. 1186–1192, two-column IEEE format; no embedded PDF
outline. Page boundaries below were reconstructed from form-feed markers in
the extracted text — treat exact page numbers as reliable but note them as
"(location approx.)" where stated, since PDF-extraction page splits can
occasionally be off by a line or two. Section numbering below follows the
paper's own: 1. Introduction — the Problems [1.1 The Bin Packing, 1.2 The
Line Balancing, 1.3 The Cost Function, 1.4 Context of the Line Balancing], 2.
Genetic Algorithms and Grouping Problems [2.1 Generalities, 2.2 The
Crossover, 2.3 The Mutation], 3. Operators for the two Problems [3.1 The
Encoding, 3.2 Apport of Known Heuristics, 3.3 Generating the First
Population, 3.4 BPCX — the Bin Packing Crossover, 3.5 The Mutation, 3.6 The
Inversion, 3.7 Modification for the Line Balancing], 4. Experimental Results
[4.1 The Bin Packing, 4.2 The Line Balancing], 5. Discussion [5.1
Conclusions, 5.2 Suggestions for Further Development], 6. Acknowledgement, 7.
References.)

## Overview

The original conference paper introducing the Grouping Genetic Algorithm
(GGA) applied to bin packing (and, in parallel, to assembly-line balancing —
its true dual "twin problem" in this paper), later extended into the fuller
Falkenauer (1996) journal treatment. It formally defines both problems, opens
with a first-principles argument for *why* the naive "number of bins" cost
function is unusable for a search algorithm and derives the k²-fill-ratio
fitness function as the fix; then gives a from-scratch diagnosis of why the
classic (Holland-style) GA performs poorly specifically on *grouping*
problems — the crossover-schema argument and the mutation-destructiveness
argument — before proposing the group-based encoding and a matched
crossover/mutation/inversion operator set, seeded and repaired using the
First-Fit (FF) / First-Fit-Decreasing (FFD) heuristics. It closes with
concrete experimental results on randomly generated adversarial ("perfect
packing minus a LEEWAY") instances for both BPP and LBP, showing the GA's
advantage over FFD grows as the packing gets tighter. This 1992 paper is
historically the *first* appearance of essentially every idea Falkenauer
(1996) later systematizes — citing it directly (rather than only the 1996
follow-up) is the more historically accurate move for a Related Work section
tracing the GGA idea's origin.

## Section-by-section walkthrough

### 1. Introduction — the Problems (p. 1186–1187)

**1.1 The Bin Packing** (p. 1186) states the BPP as a decision problem citing
Garey & Johnson (1979): given a finite set O of object sizes and constants B
(bin size) and N (bin count), does a partition of O into ≤N subsets exist
such that no subset's element-sum exceeds B? This NP-complete decision
problem gives rise to the NP-hard optimization version — minimizing the
number of bins — which is the paper's actual subject. States that Garey &
Johnson's simple heuristics are "no worse (but also no better) than a rather
small multiplying factor above the optimal number of bins," and gives FF and
Best-Fit informally (place each object into the first/most-filled bin with
enough remaining space), noting Best-Fit "can... be shown to perform as well
(as bad) as the FF, while being slower."

**1.2 The Line Balancing** (p. 1186) defines the line balancing problem
(LBP): given a DAG G=(T,P) of tasks T with precedence arrows P, task lengths
Lᵢ, cycle time C, and a target station count N, can T be partitioned into ≤N
subsets Sⱼ such that (1) no subset's task-length sum exceeds C and (2) the
subsets admit an ordering compatible with all precedence arrows? Shows LBP is
NP-complete by reduction *from* BPP (BPP is the special case P=∅), so LBP
"contains [BPP] as a special case" — the formal justification for treating
the two problems with near-identical machinery throughout the rest of the
paper.

**1.3 The Cost Function** (p. 1187) is the key argument. Starts from the
"obvious" cost function — raw bin count — and shows it is *useless for
guided search*: the search-space landscape it induces is pathological
because "a very small number of optimal points... are lost in a sea of
points where this purported cost function is just one unit above the
optimum," and critically, "the number of possible arrangements yielding N+1
bins grows exponentially with N... [yet] all these points... appear to be
absolutely equal in terms of merit" — an algorithm using raw bin-count as
fitness "would have to run into the optimal solution by mere chance." The
fix: find the "smallest natural piece of a solution which is meaningful
enough to convey information" — for BPP, that unit is the *bin itself*.
Reasoning: (a) a better-used bin means fewer bins overall; (b) given two bins,
one nearly full and one nearly empty is *better* than two half-filled bins,
because the near-empty bin can still accommodate objects too large for
either half-filled bin. This yields the cost function to **maximize**:

```
f_BPP = (1/N) · Σ_{i=1..N} (fill_i / C)^k
```

with N = bins used, fillᵢ = sum of object sizes in bin i, C = bin capacity, k
a constant > 1. k=1 degenerates to plain bin-count (undesirable, per the
argument above); larger k "expresses our concentration on the well-filled
'elite' bins" — pushing the search toward extremal (very full / very empty)
bin configurations rather than a homogeneous spread. Experimentally, **k=2**
"gives good results"; larger k values "seem to lead to premature convergence
... as the local optima, due to a few well-filled bins, are too hard to
escape." This is the primary citable derivation of the fitness function
Nikola's own GA implementation uses.

**1.4 Context of the Line Balancing** (p. 1187–1188) is industrial/systems
framing, not directly relevant to BPP theory: describes the "Integrated
Control" architecture for a robotized assembly cell under development at the
authors' lab (CRIF, Brussels), with off-line functions (design-for-assembly,
assembly planning, resource planning, scheduling) and on-line functions
(assembly supervision/error diagnosis, error recovery). States the paper's
LBP work specifically targets the *resource planning* stage. This section is
purely context/motivation and contributes no algorithmic content re-used
later.

### 2. Genetic Algorithms and Grouping Problems (p. 1188–1189)

**2.1 Generalities** (p. 1188) gives a one-paragraph GA primer (schemata as
the mechanism underlying crossover's efficiency, citing Holland 1975) and
then defines **grouping problems** precisely: "optimization problems where
the aim is to group members of a set into a small number of families, in
order to optimize a cost function... A problem is a grouping when the cost
function to maximize increases with the size and decreases with the number
of families created." Explicitly identifies BPP (and hence LBP) as a
grouping problem under this definition, since f_BPP grows with bin fill and
shrinks with bin count.

**2.2 The Crossover** (p. 1188–1189) walks through the standard one-gene-
per-object encoding (chromosome `ADBCEB` = object 1→bin A, object 2→bin D,
etc.) and shows the grouping of objects 3 and 6 into bin B is a "gain" that
"should... be transmitted to the next generation" but the two genes "are
positioned too far from each other on the chromosome to be safe against
disruption during crossover" (crossing-site probability grows with gene
distance). The standard fix, inversion, can bring genes together (`123456
ADBCEB` → `123654 ADBBEC`), and "this time the group of Bs has good chances
to survive a crossover." But — the central diagnosis — **this stops working
once groups grow larger**: in a chromosome like `123654 / ACBBBB`, "the
probability of disruption of the very promising group of four Bs is as large
as it was for the group of two Bs without inversion... the good schemata for
this problem are, by definition, *long* schemata." Conclusion: standard
crossover "works against its own progress towards destruction of the good
schemata" precisely as the population converges toward good solutions,
yielding "an algorithm stagnating on poor, never improving solutions."

**2.3 The Mutation** (p. 1189) runs the same argument for mutation. Early on,
mutating `ABDBAC` → `ABDEAC` can be "beneficial," introducing a possibly
missing allele. But once large same-letter groups have formed
(`AAABBB`), a random mutation (`AAABBB`→`AAEBBB`) creates "a 'group' of just
one element" — since grouping accounts for the gain, "this mutated individual
will most probably show a steep loss of fitness... [and] will be eliminated
with high probability... on the very next step of the algorithm, yielding
hardly any benefit for the genetic search." Conclusion: "the classic mutation
is too destructive once the GA begins to reach a good solution of the
grouping problem."

### 3. Operators for the two Problems (p. 1189–1191)

**3.1 The Encoding** (p. 1189) diagnoses the *root cause* behind §2's
failures: the standard chromosome is "much too object oriented, instead of
being group (i.e. bin) oriented" — f_BPP rewards well-filled *bins*, but the
object-per-gene chromosome has "no structural counterpart for them." States
this generalizes beyond BPP/LBP to all grouping problems (citing
Falkenauer 1991 on a grouping classification problem) and frames the fix as
compliance with the "Thesis of Good Building Blocks" central to the GA
paradigm. **The fix**: augment the object-part chromosome with a **group
part**, one gene per bin, e.g. `ADBCEB` (object assignment) becomes
`ADBCEB:BECDA` (object part : group part, group part after the colon). "The
important point is that the genetic operators will work with the group part
of the chromosomes" — the object part merely records membership. Notes this
implies variable-length chromosomes (number of bins varies across
individuals) — an important structural departure from Nikola's fixed-length
permutation encoding.

**3.2 Apport of Known Heuristics** (p. 1189–1190) justifies building FF/FFD
into the genetic operators via three properties of FF: (1) it places objects
one at a time, independent of the whole set — so it works on subsets too;
(2) it doesn't need to restart from scratch — it can extend a *partial*
solution (some bins already filled); (3) it is *complete* — "there is a
leeway in its function: the solution it produces depends on the order in
which the objects are presented..., and at least one permutation of the
objects leads to the optimum. Note that this is rather exceptional for a
heuristic." Contrasts with FFD (sort decreasing, then FF): "while performing
slightly better than FF, it always produces a unique solution" (i.e. FFD
sacrifices FF's order-dependent flexibility for slightly better typical
performance).

**3.3 Generating the First Population** (p. 1190): the initial population
must be both random and constraint-valid. FF is used as the generator: fed
objects "in a random order, it generates a solution which is reasonable...
yet still random to a large extent" — and (per §3.7) the same mechanism
extends cleanly to LBP.

**3.4 BPCX, the Bin Packing Crossover** (p. 1190) — the operator design,
given as a fully worked example. Group parts of two parents, e.g.
`ABCDEF` (parent 1) and `abcd` (parent 2); two random crossing sites are cut
in each, e.g. `A|BCD|EF` and `ab|cd|`. The bins between the second parent's
crossing sites are **injected** into the first at its first crossing site:
`AcdBCDEF`. Duplicate objects (now appearing in two bins) are resolved by
**deleting the original bins that contained them** — e.g. if bins C, E, F
also contained objects from the injected c, d, those bins are dropped
entirely: `AcdBD`. This necessarily orphans some objects that were in the
deleted bins but *weren't* duplicates; these are **reinserted via FFD**,
producing e.g. `AcdBDx` where x is one or more new bins built from the
reinserted objects. The child thus inherits bins A, B, D from parent 1 and c,
d from parent 2 — though A/B/D "might not be exactly the original ones,"
since FFD may have topped them up with reinserted objects, which the authors
note is "actually beneficial, since it leads to bins even better filled than
in the parent."

**3.5 The Mutation** (p. 1190): select a few bins at random and eliminate
them; reinsert their objects via plain FF in random order. Two rules improve
mutation's odds of helping: (1) **the emptiest bin is always among those
eliminated**; (2) **at least three bins are always eliminated and
reinserted** together (since bin count can't improve by touching fewer than
three).

**3.6 The Inversion** (p. 1190): the classic inversion operator, applied only
to the group part of the chromosome (object-part membership is positional-
order-independent so is untouched). Purely representational — brings
promising (well-filled) bins closer together on the chromosome to protect
them from BPCX disruption, mirroring §2.2's discussion.

**3.7 Modification for the Line Balancing** (p. 1190–1191): adapts the BPP
operators to respect LBP's added precedence constraint. Key insight: the
constraint is violated exactly when merging same-station nodes in the
precedence graph creates a *cycle*. Mutation is automatically valid (it only
removes/reinserts objects into an already-valid solution). BPCX needs an
extra repair step: after injecting/deleting bins, check the remaining
chromosome's group-graph for cycles; if none, proceed with constrained FFD as
usual; if a cycle exists, **repeatedly remove one random object from the
cycle and recheck** until the cycle breaks, minimizing disruption to
inherited schemata.

### 4. Experimental Results (p. 1191)

**4.1 The Bin Packing.** FFD is the benchmark (a "good heuristic for the
BPP"). Test-instance construction (an important adversarial-instance
technique, conceptually close to Falkenauer's later "triplet" difficult
instances): generate objects with random sizes admitting a **perfect
packing** (f_BPP = 1), then subtract a total of **LEEWAY%** of one bin's size
from randomly chosen objects — e.g. LEEWAY=3% with bin size 255 removes 7.65
total from the objects. Because only a small fraction of one bin's capacity
is removed, "the optimum number of bins hasn't changed" — but reaching it
becomes harder to *find*. The GA was capped at **5000 generations**. Results
(Figure 2): average proportion, over **50 successive runs of 64-object test
cases**, successfully optimized by GA vs. FFD, as a function of LEEWAY
(swept 1.5% through 15% of bin size) — "the chart shows the net superiority
of the GA in 'tough' conditions, i.e. when the space for the objects to pack
is tight." Runtime: "of the order of a minute on a 4D35 Silicon Graphics (33
MIPS)" — a period-typical workstation benchmark, useful only as a historical
runtime anchor, not a meaningful comparison to modern hardware.

**4.2 The Line Balancing.** Precedence constraints generated by time-sorting
tasks and linking each to a randomly chosen earlier task, ensuring the
optimal packing also respects precedence. FFD can no longer serve as
benchmark ("when modified as indicated in section 3.7... its performance
deteriorates badly"), so only the GA's own LEEWAY-sweep curve (Figure 3,
analogous to Figure 2) is reported, this time allowing up to **10000
generations**; average runtime "of the order of 5 minutes." The GA finds the
optimal station count reliably "with only a small LEEWAY (say 5% of the
cycle time)." Industrial-relevance claims (p. 1191–1192): 64 operations
"comfortably covers the majority of industry's needs," with "preliminary
tests suggest[ing] that problems of up to two hundred tasks could still be
handled in a reasonable time"; a 5% LEEWAY is realistic since exact
(cycle-time-divisible) line balances are rare in practice. Contrasts
favorably against enumeration/dynamic-programming alternatives, which need
much denser precedence constraints to be tractable — citing Peng (1991)'s
DP approach needing "60% nonempty entries in the precedence matrix" to solve
25-task problems "reasonably fast," versus the GA's tolerance for sparse
constraints "thanks to its bin packing 'ancestor'."

### 5. Discussion (p. 1192)

**5.1 Conclusions** restates the paper's contribution succinctly: an
efficient GA for two NP-hard grouping problems, justified by first showing
the classic GA performs poorly on problems of this type, and demonstrating
real-world-scale handling for LBP specifically. **5.2 Suggestions for
Further Development** proposes two concrete LBP extensions: (a) letting
users specify soft/hard preferences for co-locating (or not) certain tasks on
the same workstation; (b) accounting for per-workstation cost as a function
of task heterogeneity (a station handling very dissimilar tasks — i.e. more
flexible — costing more than a specialized one). Notes (a) was "currently
under way" at the authors' lab. §6 Acknowledgement credits ESPRIT II Project
2637 (ARMS) funding. §7 References is a short, historically interesting list
— notably [Garey and Johnson, 79] for the BPP definition/heuristic bounds,
and [Holland, 75] / [Goldberg, 89] for GA foundations.

## Citable specifics

> "[Garey and Johnson,79] cite simple heuristics which can be shown to be no
> worse (but also no better) than a rather small multiplying factor above
> the optimal number of bins." (p. 1186, §1.1)

> "Putting the object into the first available bin found yields the First
> Fit (FF) heuristic. Searching for the most filled bin still having enough
> space for the object yields the Best Fit, a seemingly better heuristic,
> which can, however, be shown to perform as well (as bad) as the FF, while
> being slower." (p. 1186, §1.1)

> "The trouble is that such a cost function lacks any capacity of guiding an
> algorithm in the search... The number of possible arrangements yielding
> N+1 bins grows exponentially with N and is thus very large even for small
> problem sizes. Nevertheless, all these points in the search space yield
> the same cost of N+1 and thus appear to be absolutely equal in terms of
> merit for searching their surroundings." (p. 1187, §1.3 — the core
> argument against raw bin-count as a GA fitness function)

> "We thus settled for the following cost function for the BPP: maximize
> f_BPP = (1/N)·Σ_{i=1..N}(fill_i/C)^k, with N being the number of bins
> used, fill_i the sum of sizes of the objects in bin i, C the bin capacity
> and k a constant, k>1... We have experimented with several values of k and
> found out that k=2 gives good results. Larger values of k seem to lead to
> premature convergence of the algorithm, as the local optima, due to a few
> well-filled bins, are too hard to escape." (p. 1187, §1.3 — verbatim
> derivation and parameter choice for the fitness function Nikola's GA
> itself uses)

> "A problem is a grouping when the cost function to maximize increases with
> the size and decreases with the number of families created. The BPP (and
> hence LBP) can clearly be seen to be a grouping problem." (p. 1188, §2.1)

> "In a chromosome like 123654 / ACBBBB, the probability of disruption of
> the very promising group of four Bs is as large as it was for the group
> of two Bs without inversion... the good schemata for this problem are, by
> definition, long schemata." (p. 1188–1189, §2.2 — the schema-disruption
> argument against standard crossover on grouping problems)

> "In other words, the classic mutation is too destructive once the GA
> begins to reach a good solution of the grouping problem." (p. 1189, §2.3)

> "The main reason is that the structure of the simple chromosome (which the
> above operators work with) is much too object oriented, instead of being
> group (i.e. bin) oriented... the fact that the object i is in the bin j is
> meaningless — it is the fact that the bin j is full or empty that is
> important." (p. 1189, §3.1 — diagnosis motivating the group-part
> encoding)

> "Third, [FF] is complete, i.e. it can generate the optimal solution.
> Indeed, there is a leeway in its function: the solution it produces
> depends on the order in which the objects are presented to the heuristic
> ..., and at least one permutation of the objects leads to the optimum.
> Note that this is rather exceptional for a heuristic." (p. 1189–1190,
> §3.2 — the property that justifies FF as a GA-embedded decoder/repair
> operator, directly analogous to Nikola's own permutation-GA + FF-decoder
> design)

> "[BPCX example] ABCDEF (first parent), abcd (second parent)... A|BCD|EF
> and ab|cd|... the bins between the crossing sites in the second chromosome
> are injected into the first, at the first crossing site, yielding
> AcdBCDEF... We eliminate those [duplicate-containing] bins, leaving AcdBD.
> ... we apply the FFD heuristic to reinsert them, yielding, say AcdBDx." (p.
> 1190, §3.4 — the full worked BPCX crossover example)

> "In order to improve the chances of the mutation to improve the current
> solution, we follow two rules: the emptiest bin is always among the
> eliminated ones, and we always eliminate and subsequently reinsert at
> least three bins (the number of used bins cannot be improved with less)."
> (p. 1190, §3.5)

> "We constructed the test data as follows: we first generated objects of
> random sizes admitting a perfect packing (i.e. f_BPP=1), and then
> subtracted from randomly chosen objects a total of LEEWAY percentage of
> the size of one bin." (p. 1191, §4.1 — the adversarial-instance
> construction technique, conceptually the direct ancestor of Falkenauer's
> later "triplet"/perfect-packing difficult instances that Nikola's
> `BPPLIB/` benchmark set includes)

> "The chart shows the net superiority of the GA in 'tough' conditions, i.e.
> when the space for the objects to pack is tight." (p. 1191, §4.1 — GA vs.
> FFD, 50 runs, 64-object instances, LEEWAY swept 1.5%–15% of bin size)

> "The GA's performance also represents a very good alternative in
> comparison to most enumeration techniques. This is due mainly to its
> capacity to handle cases with very sparse precedence constraints, thanks
> to its bin packing 'ancestor'." (p. 1192, §4.2)

## How it helps Nikola's thesis

- This is the **primary, original source** (predating Falkenauer 1996) for
  both the k²-fill fitness function and its first-principles derivation from
  the failure of raw bin-count as a search-guiding cost function — citing
  this 1992 paper directly, with its actual derivation (§1.3, p. 1187), is
  more historically accurate for Ch2/Ch3 (methodology / fitness design) than
  only citing the 1996 follow-up.
- The **crossover-schema-disruption** and **mutation-destructiveness**
  arguments (§2.2–2.3) are the earliest fully worked statement of the
  standard critique against naive GA encodings on grouping problems —
  essential background for Ch2's discussion of why Nikola's own thesis
  instead pairs a *permutation* encoding with a First-Fit *decoder* (sidestepping
  the group-part encoding Falkenauer proposes here, at the cost of inheriting
  a different, related critique that Falkenauer (1996) later levels
  specifically at ordering GAs — see `falkenauer-1996.md`).
- §3.2's argument for *why* FF specifically is attractive as a GA-embedded
  operator (order-dependent but complete, incremental, subset-safe) is a
  clean, citable justification Nikola can adapt when explaining why his own
  GA uses a First-Fit decoder rather than Best-Fit or another constructive
  heuristic — directly relevant to Ch3 methodology.
- The **§4.1 LEEWAY adversarial-instance construction** (perfect packing
  minus a controlled percentage) is conceptually the direct ancestor of the
  Falkenauer "triplet" difficult instances in Nikola's `BPPLIB/` benchmark
  set — worth an explicit historical link in Ch1/Related Work: both
  constructions deliberately build in a *near-miss* to perfect packing to
  stress-test whether an algorithm can still find it.
- The **BPCX crossover worked example** (§3.4) and the **group/mutation
  rules** (§3.5, "always eliminate the emptiest bin plus at least three
  total") are concrete, citable operator designs to contrast directly
  against Nikola's own order-crossover + swap-mutation permutation operators
  in a Methodology comparison table.
