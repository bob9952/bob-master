> **Study notes only — not thesis prose.** This is a paraphrased digest for
> Nikola's own reading. Any idea used in the actual thesis must be
> rewritten entirely in his own words and cleared by the `plagiarism-guard`
> subagent; see `literature/digests/README.md`.

# Munien et al. (2020) — Metaheuristic Approaches for 1D-BPP

**Zotero key:** `98Y6HQGS`

## Full citation

Munien, C., Mahabeer, S., Dzitiro, E., Singh, S., Zungu, S., & Ezugwu, A. E.-S.
(2020). Metaheuristic Approaches for One-Dimensional Bin Packing Problem: A
Comparative Performance Study. *IEEE Access*, 8, 227438–227465.
https://doi.org/10.1109/ACCESS.2020.3046185

(28 journal pages, pp. 227438–227465; no embedded PDF outline — the paper's own
section numbers are used below: I. Introduction, II. Literature Review [A.
Classical heuristic approaches, B. Metaheuristic approaches], III.
Representative Metaheuristic Algorithms [A. Firefly Algorithm, B. Hybrid
Firefly Algorithm, C. Adaptive Cuckoo Search Algorithm, D. Hybrid Cuckoo
Search Genetic Algorithm, E. Artificial Bee Colony, F. Genetic Algorithm], IV.
Experimentation, Results and Discussion [A. Datasets, B. Results and
Discussion, C. Hybrid vs Non-Hybrid Cuckoo Search, D. Hybrid vs Non-Hybrid
FA], V. Conclusion, References.)

## Overview

A systematic, empirical comparative study applying six representative
population-based metaheuristics — Firefly Algorithm (FA), a hybridized/mutated
Firefly variant (FAH), Adaptive Cuckoo Search (ACSA), a hybrid Cuckoo
Search–Genetic Algorithm (CSGA), Artificial Bee Colony (ABC), and a standard
Genetic Algorithm (GA) — to the classical 1D-BPP, each metaheuristic paired
with one of two underlying constructive decoding heuristics: best-fit or
"better-fit" (Bhatia, Hazra & Basu 2009). Across three dataset categories
(easy/100-capacity, medium/1000-capacity, hard/100,000-capacity;
~1,210 instances in total, drawn from a public BPP dataset repository) the
paper's headline finding is that the *underlying decoding heuristic matters
more than which metaheuristic wraps it*: best-fit degrades sharply as
instance complexity/size grows, while better-fit stays close to optimal
almost regardless of instance size or bin capacity — at the cost of
substantially higher computation time, especially when paired with ACSA,
CSGA, or GA. Each metaheuristic operates purely as a *permutation search* over
item orderings, with the underlying heuristic doing the actual bin
construction/decoding — architecturally the same "permutation + constructive
decoder" pattern as Nikola's own permutation-GA + First-Fit decoder, making
this the most directly comparable empirical study of that pattern's variants.

## Section-by-section walkthrough

### I. Introduction (p. 227438–227439)

States the classical 1D-BPP: given fixed bin capacity C and a list of n items
L = (p₁, ..., pₙ) with sizes 0 ≤ s(pᵢ) < C, find the minimum integer m such
that L partitions into B₁ ∪ ... ∪ Bₘ with each bin's item-size sum ≤ C. Gives
the standard ILP model (their eq. 1–5): binary yᵢ ("bin i used"), binary xᵢⱼ
("item j packed into bin i"),

```
Minimize  Σ_{i=1}^{u} y_i
s.t.      Σ_{j} w_j x_ij ≤ c·y_i        for 1 ≤ i ≤ u
          Σ_{i} x_ij = 1                for 1 ≤ j ≤ n
          y_i, x_ij ∈ {0,1}
```

and a closed-form lower bound (their eq. 6): N ≥ ⌈(Σᵢ Sᵢ)/C⌉. Briefly
distinguishes 1D/2D/3D-BPP variants and cites specialized BPP variants
(Coffman et al.'s max-items-per-bin variant; Krause et al.'s bin-cardinality-
constrained variant for task scheduling). Lists applications: industrial
applications, supply-chain packaging design (container/truck loading,
multi-container and multi-pallet loading problems), and health-care resource
allocation, plus classic examples (memory allocation, commercial-to-
station-break assignment). Confirms 1D-BPP is NP-hard, motivating heuristic/
metaheuristic approaches for real-world-sized instances. States the six
algorithms studied: FA, FAH, ACSA, CSGA, ABC, GA — chosen as "representative"
state-of-the-art nature-inspired metaheuristics, each tested with both best-
fit and better-fit as the underlying reordering/decoding heuristic. Four
explicit technical contributions are listed (p. 227439): (1) a review of
state-of-the-art metaheuristics for 1D-BPP; (2) a systematic performance study
of representative algorithms; (3) implementation of two hybrid metaheuristics
(CSGA and a mutated/hybrid FA); (4) presentation of initial comparative
results.

### II. Literature Review (p. 227440–227441)

**A. Classical heuristic approaches for 1D-BPP.** Restates First-Fit, Best-
Fit, Next-Fit as the traditional online/sequential heuristics, and FFD/BFD as
their decreasing-order offline extensions. States a performance ranking
(citing ref. [3], i.e. effectively Johnson 1973/1974's line of results): "Best
Fit Decreasing, First Fit Decreasing, Best Fit, First Fit and Next Fit" in
descending order of performance. Introduces the **better-fit** heuristic
(Bhatia, Hazra & Basu 2009, ref. [38]): it replaces the item already tentatively
packed in a bin with the next item on the list if that next item fills the
bin more completely; time complexity O(n²m) (n = items, m = number of
distinct sizes), contrasted with best-fit's O(n log n); the paper states
better-fit "was proved to produce better results than the best fit
algorithm," while explicitly noting "the best fit produces the worst packing
of 1.7*optimum" (i.e. invoking the classical FF/BF 17/10 worst-case bound,
citing the same source [38]).

**B. Metaheuristic approaches for 1D-BPP.** A literature survey of prior
metaheuristic applications to 1D-BPP, several directly relevant to Nikola's
related-work section:

- **Whale Optimization Algorithm** (citing [34]) — adapted with Lévy flights,
  an added mutation phase, and a logistic chaotic map; results comparable to
  Adaptive Cuckoo Search but with fewer iterations/agents needed.
- **Kucukyilmaz & Kiziloz [61]** — "a novel scalable island-parallel grouping
  genetic algorithm... reported significant improvements on the Hard28 problem
  instances by outperforming the state-of-the-art existing genetic
  algorithms," with additional analysis of search-space-diversity parameters.
- **Dokeroglu & Cosar [62]** — hybrid parallel algorithms combining parallel
  computation, evolutionary grouping-GA metaheuristics, and bin-oriented
  heuristics for large-scale 1D-BPP; tested on 1,318 benchmark problems,
  reaching optimal solutions for **88.5%** of instances with practical
  optimization times, and solving the remainder "with no more than one extra
  bin."
- **Abd Elminaam et al. [32]** — adaptive Fitness-Dependent Optimizer (AFDO)
  seeded via a modified First-Fit heuristic; tested on 30 BPP benchmarks;
  outperformed PSO, Crow Search, and Jaya by 16%, 17%, 11% respectively on
  solution quality, and by up to 46%/54%/43% on execution time.
- **Gherboudj [63]** — adaptive African Buffalo Optimization (ABO) combined
  with a ranked-order-value (ROV) discretization method; tested on 1,210
  instances (the same/similar dataset this paper itself uses).
- **Ashamawi et al. [36]** — modified Squirrel Search Algorithm; outperformed
  PSO though didn't always reach optimum.
- **Simulated Annealing** discussion (Pinto et al. [45], Bertsimas & Tsitsiklis
  [46]): explains the physical-annealing analogy (heating/cooling, acceptance
  of worse solutions to escape local optima) and its four algorithmic
  components (initial solution, neighborhood generation, acceptance
  criterion, stopping criterion). Rao & Iyengar [48] compared five heuristics
  including SA against Largest-Piece-First (LPF), Shortest-Piece-First (SPF),
  FFD, and First-Fit-Increasing (FFI): "the FFD and SA were the better
  performing algorithms," with SA uniquely consistent as bin count increased.
  Sonuc et al. [49] found FFD+SA beat plain FFD, with FFD+SA alone achieving
  optimal results in their experiment.

### III. Representative Metaheuristic Algorithms (p. 227441–227448)

**A. Firefly Algorithm (FA).** Population-based, nature-inspired (Yang 2008),
draws an analogy to bioluminescent attraction among fireflies. Three
simplifying assumptions: fireflies are unisex; attractiveness is proportional
to brightness (less-bright fireflies move toward brighter ones, and if none
is brighter, movement is random); brightness is governed by the fitness
function (derived from the objective function). Light intensity (their eq. 7):

```
I(r) = I0 · e^(−γr²)
```

Brightness (eq. 8): β = β0·e^(−γr²). Distance is Euclidean (eq. 9):
r_ij = ‖s_i − s_j‖ = sqrt(Σ_k (s_ik − s_jk)²). Firefly movement (eq. 10):

```
s_i^(t+1) = s_i^t + β0·e^(−γ·r_ij²)·(s_i^t − s_j^t) + α·ε_i^t
```

Two asymptotic special cases noted: γ→0 reduces FA to a PSO-like update;
γ→∞ reduces the movement term to a Simulated-Annealing-like behavior — "FA a
generalization of these three algorithms" (PSO, DE, SA). Algorithm 1 (p.
227442) gives the full pseudocode including a mutation step with decreasing
rate π. **Advantages** listed: simple to implement, efficient, avoids the
poor-starting-solution issue common to population methods. **Disadvantages**:
slow convergence rate; can still get trapped in local optima despite
mitigation mechanisms.

**B. Hybrid Firefly Algorithm (FAH).** Adds a random mutation with a
decreasing rate π over iterations (favoring exploration early, exploitation
late); mutation reorders the item arrangement passed to the underlying
better-fit heuristic, producing a new solution/firefly. Implemented in Java.

**C. Adaptive Cuckoo Search Algorithm (ACSA).** Based on Yang & Deb's 2009
Cuckoo Search via Lévy flights, itself inspired by brood-parasitic cuckoo
species. Three governing rules: one egg laid per nest at random; best-quality
nests survive to the next generation; a host discovers a foreign egg with
probability p_a ∈ [0,1], triggering replacement via a "local walk" operator.
Local random walk (eq. 11):

```
x_i^(t+1) = x_i^t + α·s ⊗ H(p_a − ε) ⊗ (x_j^t − x_k^t)
```

(H = Heaviside function, ε a random number, x_j/x_k two randomly chosen
nests). Global walk via Lévy flight (eq. 12): x_i^(t+1) = x_i^t + α·L(φ). This
paper's *adaptation* (Zakaria et al. [14]) is the "ranked order value" (ROV)
rule to discretize the continuous CS solution into an item permutation: the
smallest continuous value gets rank 1, the next smallest rank 2, etc.,
producing a valid permutation "without creating additional overhead."
Objective is to minimize wastage (eq. 13): wastage = capacity − pointer,
where "pointer" is the index the bin's running sum reaches (worked example:
capacity 10, items 1+2+3=6 packed, pointer=6, wastage=4). Full objective (eq.
14): minimize f = n·capacity − Σ_{k=0}^{n} pointer_k. **Drawbacks**: Lévy
flights can slow convergence; may fall into local optima if parameters are
mis-set.

**D. Hybrid Cuckoo Search Genetic Algorithm (CSGA).** Inspired by Lim et al.
(2014)'s CS-GA hybrid for hole-making sequence optimization: GA crossover and
mutation *replace* the CS random-walk/Lévy-flight operators. Crossover: two
parents chosen via k-tournament; two random crossover points chosen
(two-point crossover, avoiding full parent-swap); offspring formed by
interchanging values between the points; elitism — "a child will only
progress if the evaluated fitness is greater than at least one parent."
Mutation: a mutation rate is set; a Gaussian-drawn number is checked against
it; if triggered, two random bounds are drawn and the items between them are
*reversed* (i.e. a segment-reversal mutation, not swap). Algorithm 2 (p.
227446) gives full pseudocode.

**E. Artificial Bee Colony (ABC).** Karaboga's algorithm mimicking honeybee
foraging: employed bees, onlooker bees, scout bees. Food source
representation (eq. 15): xᵢ = (xᵢ,₁, ..., xᵢ,ₙ). Employed-bee phase generates
a neighbor solution (eq. 16): vᵢ,ₖ = xᵢ,ₖ + φᵢ,ₖ·(xᵢ,ₖ − xⱼ,ₖ). Fitness
transform (eq. 17):

```
fit_i(x_i) = 1/(1+f_i(x_i))         if f_i(x_i) ≥ 0
fit_i(x_i) = 1/(1+|f_i(x_i)|)       if f_i(x_i) < 0
```

Onlooker-bee selection probability (eq. 18): pᵢ = fitᵢ(xᵢ) / Σ_{i=1}^{SN} fitᵢ(xᵢ).
Scout-bee phase: solutions whose "trial" counter (failed-improvement count)
exceeds a threshold are discarded and replaced randomly. Implementation:
initial population generated by randomizing item order, then packed via
best-fit or better-fit; objective = bins + wastage, minimized. **Advantages**:
global-optimum capability, simple/robust, flexible, few parameters.
**Disadvantages**: premature convergence risk; slow late-stage convergence.

**F. Genetic Algorithm (GA).** Standard Holland-style GA (p. 227447–227448),
presented as the "classic metaheuristic... covered many times over the last
50 years" used here as a comparator. Standard 8-step loop given verbatim
(initialize → evaluate → evaluate fitness → select → crossover → mutate →
new population/fitness → repeat until termination). Encoding: chromosome =
permutation of item weights (e.g. `{74, 32, 15, 23, 25, 36, 45}`); population
= X random permutations of this set. k-tournament selection; **single-point
crossover** (not order-crossover); worked numeric example given:

```
Parent 1 → 7 11 6 3 4 8
Parent 2 → 11 6 8 7 4 3
Offspring 1 → 7 11 6 8 4 3
Offspring 2 → 11 6 8 7 3 4
(after mutation)
Offspring 1 → 7 4 6 8 11 3
Offspring 2 → 11 7 8 6 3 4
```

Fitness of a permutation = wastage from the chosen decoder (best-fit/better-
fit) applied to it. Termination: fixed generation count set by the user.
**Advantages**: easy to conceptualize, quick to implement, good when
near-optimal suffices, fast convergence and versatility. **Disadvantages**:
increased computation for complex problems, slower than some newer methods,
premature convergence, heavy dependence on initial population. Notes GA was
combined with CS and FA to build the CSGA and FAH hybrids respectively.

### IV. Experimentation, Results and Discussion (p. 227448–227462)

**A. Datasets.** Hardware: 3.75 GHz AMD Ryzen 7, 16GB 2666MHz RAM; Java in
Eclipse. Instances drawn from a public BPP dataset repository (ref. [62], the
"BPP Datasets" site www2.wiwi.uni-jena.de/Entscheidung/binpp). Three dataset
categories, over 1,210 instances total:

| Dataset | Label | Capacity | Item counts tested |
|---|---|---|---|
| 1 ("easy") | Table 7 | 100 | 50, 100, 500 |
| 2 ("medium") | Table 8 | 1000 | 50, 100, 500 |
| 3 ("hard") | Table 9 | 100,000 | 200 (fixed) |

30 instances were selected in total (10 per dataset), each run 10 times per
metaheuristic × underlying-heuristic combination. Three named instances per
dataset were examined in depth: **N1C1W1_D, N2C1W2_N, N4C1W4_A** (Dataset 1);
**N1W1B1R9, N2W1B1R3, N4W2B1R3** (Dataset 2); **HARD2, HARD5, HARD8**
(Dataset 3) — chosen to vary item count/capacity.

**B. Results and Discussion.**

*Dataset 1 (capacity 100).* Table 10 / Figures 1–3: every algorithm performs
well; **better-fit reaches optimal for every algorithm on every instance**;
under best-fit, only FAH and GA fall one bin short of optimal. Computational
time (Figs. 4–6): under best-fit, differences between algorithms are
sub-millisecond and negligible for 50/100 items; at 500 items ABC and GA are
fastest under best-fit, ACSA slowest; under better-fit (more computationally
expensive generally), ACSA, CSGA, GA are consistently worse, with GA/ACSA
taking "up to 30... approximately 100 milliseconds longer on average" than
the rest at 500 items. ABC shows almost no performance degradation as item
count grows.

*Dataset 2 (capacity 1000).* Table 11 / Figs. 7–9: at 50 items (Fig. 7) both
heuristics do well; best-fit attains optimal in all but two algorithms,
better-fit in all. At 100 items (Fig. 8) better-fit attains optimal for every
metaheuristic while best-fit cannot; ACSA/CSGA do relatively better than
others under best-fit here. At 500 items (Fig. 9) **even better-fit fails to
reach the optimum** for this specific instance — the paper's one explicit
counter-example to "better-fit is always near-optimal." Timing (Figs.
10–12): under better-fit, ACSA time-per-item roughly doubled (5.76 → 11.27
ms/item) when items doubled from 50 to 100, "suggest[ing] that ACSA, CSGA and
GA perform substantially worse... with respect to time" as instance size
grows; FA/FAH/ABC remain close together and comparatively unaffected.

*Dataset 3 (capacity 100,000, 200 items, "hard").* Table 12 / Figs. 13–15:
best-fit struggles across all instances (as expected given the "ideal items
per bin... between 3 and 5" for this scale, so wastage per bin is
proportionally larger for a bin-count miss); better-fit reaches optimal
almost everywhere. Notably, on the HARD2 instance (Fig. 13) **GA was the
*only* algorithm to reach the optimal solution** — the single dataset/
instance in the whole study where GA uniquely wins. ACSA, CSGA, GA "appeared
to slightly outperform the other algorithms" on HARD5 specifically.

**C. Hybrid vs Non-Hybrid Cuckoo Search.** ACSA and CSGA reach very similar
bin counts across all three datasets ("we... cannot conclude anything in that
respect" for solution quality), but CSGA is consistently 2.5–4× faster than
ACSA in wall-clock time, attributed to CSGA's simpler GA-style operators
replacing the more expensive Lévy-flight walk. Concrete timing figures
(Dataset 1, easy): ACSA + best-fit ≈ 70 ms (50 items) scaling up; ACSA +
better-fit ≈ 341 ms (50 items) escalating to **≈ 96,000 ms at 500 items**.
CSGA + best-fit: 30–920 ms; CSGA + better-fit: 130–32,000 ms across the same
item-count range — so best-fit remains the time-preferable underlying
heuristic for both Cuckoo variants despite better-fit's quality edge. On the
hard dataset, ACSA + best-fit "did not achieve any optimal results," instead
producing "an average of n+3 bins" (n = optimal); with better-fit, ACSA
reached optimal on 9 of 10 hard instances but required "approximately 16
times more milliseconds."

**D. Hybrid vs Non-Hybrid FA.** FA and FAH perform almost identically in bin
count (both optimal under better-fit, both near-optimal under best-fit); "no
statement can be made about the effectiveness of the hybrid in terms of bin
packing." Timing is likewise near-identical except on HARD instances under
better-fit, where FAH is marginally faster than FA (but the gap is
sub-millisecond and "negligible"). Overall conclusion for this pairing: "the
FAH provides no meaningful improvement to the FA both in terms of bin packing
results and time." FA/FAH rank second only to ABC in overall speed across the
whole study.

### V. Conclusion (p. 227462)

Restates the headline trade-off: best-fit attains optimal solutions readily
on the easy dataset but degrades as complexity increases (still producing
"near-optimal solutions and a good packing schema for most instances");
better-fit "results in optimal solutions almost all the time, regardless of
capacity and number of items," at the cost of substantially higher
computation time, "especially with the ACSA, CSGA, and GA metaheuristics."
For FA, FAH, and ABC, better-fit's extra cost is judged worthwhile since the
time increase is comparatively modest. ABC is confirmed as the fastest
metaheuristic overall, followed by FA/FAH. Future work suggested: reducing
computational cost of ACSA/CSGA/GA; testing other contemporary metaheuristics
(Monarch Butterfly Optimization, Earthworm Optimization, Elephant Herding
Optimization, Moth Search, Symbiotic Organisms Search); and investigating
non-random initial-population generation strategies (the paper's own GA/ACSA/
CSGA/ABC all start from *purely random* permutations — a contrast worth
flagging against Nikola's heuristic-seeded initial population).

## Citable specifics

> "It is worth noting that by utilizing best fit heuristic, the algorithms
> attained optimal solutions for instances of the easy dataset... However,
> as the complexity of the instances increased, the ability to produce
> high-quality results decreased... utilizing better fit as the underlying
> heuristic results in optimal solutions almost all the time, regardless of
> capacity and number of items." (Abstract, p. 227438)

> "Mathematically, the bin packing problem (BPP) can be modelled as
> follows... Minimize Σ y_i s.t. Σ w_j x_ij ≤ c y_i (1 ≤ i ≤ u); Σ x_ij = 1
> (1 ≤ j ≤ n); y_i, x_ij ∈ {0,1}." (p. 227438–227439, §I, eq. 1–5 — the ILP
> model)

> "Listing the traditional and extension heuristics, in descending order of
> performance, one obtains Best Fit Decreasing, First Fit Decreasing, Best
> Fit, First Fit and Next Fit [3]." (p. 227440, §II.A)

> "The better fit algorithm replaces the object that is already packed in the
> bin with the next object on the list if the next object fills the bin
> better. The time complexity of this algorithm is O(n²m)... This algorithm
> was proved to produce better results than the best fit algorithm... The
> best fit produces the worst packing of 1.7* optimum [38]." (p. 227440–227441,
> §II.A)

> "Kucukyilmaz and Kiziloz [61] proposed a novel scalable island-parallel
> grouping genetic algorithm for the well-known combinatorial optimization
> problem... reported significant improvements on the Hard28 problem
> instances by outperforming the state-of-the-art existing genetic
> algorithms." (p. 227440, §II.B)

> "Dokeroglu and Cosar [62] proposed a set of robust and scalable hybrid
> parallel algorithms... a total number of 1,318 benchmark problems were
> examined with the proposed set of algorithms, and it was shown that
> optimal solutions for 88.5% of these instances could be obtained with
> practical optimization times while solving the rest of the problems with
> no more than one extra bin." (p. 227440, §II.B)

> "The genetic algorithm is quite standard and uses the same conventions as
> most other GAs. It does, however, differ in the sense that it is used in
> conjunction with an underlying heuristic [38]." (p. 227448, §III.F.2,
> Implementation — GA relies on best-fit/better-fit as decoder, exactly the
> architecture pattern Nikola's own permutation-GA + First-Fit decoder
> belongs to)

> "It can be observed from the Table and the Figures above that every
> algorithm performed well for each of the instances. Each algorithm was able
> to attain the optimal number of bins using the better fit algorithm..."
> (p. 227449–227450, §IV.B, Dataset 1 results)

> "In Figure 13 the GA was the only heuristic to obtain the optimal solution.
> This was the only instance in the dataset where this occurred, and better
> fit found the optimal solution with the remaining heuristics in every other
> instance." (p. 227455, §IV.B, Dataset 3/HARD2 result — GA's single unique
> win in the whole study)

> "Both the hybrid and nonhybrid Cuckoo Search (ACSA and CSGA) attained very
> similar results when it came to the number of bins required... In terms of
> time it is, however, a different story... The CSGA was consistently 2.5 to
> 4 times faster than the ACSA." (p. 227457–227458, §IV.C)

> "The ACSA algorithm with the best fit did not achieve any optimal results.
> An average of n + 3 bins was produced, where n is the optimal number. With
> the better fit heuristic, however, optimal results were achieved for 9 out
> of 10 of the instances." (p. 227460, §IV.C, hard dataset)

> "We can suggest that the FAH provides no meaningful improvement to the FA
> both in terms of bin packing results and time." (p. 227461, §IV.D)

> "The downfall of this heuristic is the computational time required to
> produce these solutions, especially with the ACSA, CSGA, and GA
> metaheuristics. Therefore, a trade-off between the quality of solution and
> computational time required must be made when choosing which underlying
> heuristic performs better." (p. 227462, §V Conclusion)

> "Moreover, investigating alternative methods to generate the initial
> population of the metaheuristics may prove beneficial, as this study
> involved simply randomizing initial positions." (p. 227462, §V Conclusion
> — an explicit gap this paper leaves open that Nikola's heuristic-seeded
> `_seed_orders`/`initialize_population` directly addresses)

## How it helps Nikola's thesis

- Gives an up-to-date (2020), empirically grounded related-work anchor for
  where grouping-GA and metaheuristic work on 1D-BPP stood, with concrete,
  citable numbers (Hard28 improvements per Kucukyilmaz & Kiziloz; 88.5%
  optimal-rate per Dokeroglu & Cosar on 1,318 instances) — useful for Ch1
  related-work / Ch5 results-comparison framing.
- The clean ILP formulation (eq. 1–5) and lower bound (eq. 6) is a second,
  independent cross-check for Nikola's own formal problem statement in Ch1,
  worded almost identically to Delorme/Iori/Martello's model.
- **Architecturally the closest empirical study to Nikola's own method**: all
  six metaheuristics here are permutation-search wrappers around a
  constructive decoder (best-fit/better-fit), exactly the "permutation GA +
  decoder" pattern Nikola uses (with First-Fit as decoder). Their GA's
  single-point crossover + full-reversal mutation, applied to a *purely
  random* initial population, is a direct baseline Nikola can contrast his
  own order-crossover + swap-mutation + **heuristic-seeded** population
  against — the paper's own stated future-work gap ("this study involved
  simply randomizing initial positions," p. 227462) is precisely what
  Nikola's `_seed_orders` design fills.
- The Dataset-3/HARD2 result where GA is the *sole* algorithm reaching
  optimum (p. 227455) is a small but concrete data point that a plain
  permutation-GA-with-decoder can occasionally outperform swarm-based
  metaheuristics even without heuristic seeding — useful supporting evidence
  in Ch5 when discussing why GA-family approaches remain worth studying
  despite Falkenauer's documented critique of ordering GAs (see
  `falkenauer-1996.md`).
- The best-fit-vs-better-fit trade-off (quality vs. runtime) is a good
  explicit precedent for Nikola's own First-Fit-vs-alternative-decoder
  discussion in Ch2/Ch3, and the concrete millisecond-scale timing blowups
  for ACSA/CSGA/GA under better-fit (e.g. ACSA+better-fit: 341 ms → ~96,000
  ms from 50 to 500 items) are a useful comparison point if Nikola reports
  his own GA's runtime scaling in Ch5.
