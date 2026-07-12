# Structural Breakdown of RajacicJasna (2013) — Reference Only, NOT a Source of Prose

**What this document is.** A structural/analytical map of Jasna Rajačić's 2013 master's
thesis *"Rešavanje jednodimenzionog problema pakovanja kombinovanjem optimizacionih
metoda"* (Faculty of Mathematics, University of Belgrade; Zotero item `A4TXVCY7`,
52 pages, Serbian; ACO-based approach to 1D-BPP). It exists so Nikola can model the
**shape** of his own GA thesis on a proven, closely-related example, without touching
her prose.

**The rule (MSNR §2.7, enforced by the `plagiarism-guard` agent).** Everything below
describes *what each section does and how it is built* — never how it is worded. No
sentence, phrase, or formula-surrounding text from the original is reproduced; section
titles are quoted only as short identifying labels. When Nikola drafts his own thesis,
each "transferable" item below still requires him to **independently derive and phrase**
the content from the underlying primary sources (Garey & Johnson, Martello & Toth,
Falkenauer, etc.) — reading this map is not a substitute for reading those sources, and
copying Rajačić's realization of a transferable idea is exactly the "remix"/paraphrase
violation MSNR prohibits. Sections flagged **HIGH RISK** below cover material Nikola's
own thesis must also cover (same problem, same classical heuristics) — these are the
ones where the temptation to lightly reword her text will be strongest, and where he
must instead go back to the primary literature and write from that.

---

## 1. Section-by-section walk

### Predgovor (Preface)
- **Purpose:** Formal acknowledgments — advisor, committee, family. One page.
- **How it's organized:** Three short paragraphs, each thanking a different party. No
  technical content.
- **Transferable?** Yes, trivially — this is a universal thesis-front-matter convention,
  not authored content specific to her.
- **Plagiarism-risk flag:** None — nothing here is substantive to copy.

### Uvod (Introduction)
- **Purpose:** Establish the problem, its complexity, the state of the art in one
  paragraph, and this thesis's specific contribution, then roadmap the remaining
  chapters.
- **How it's organized:** ~2 pages, four moves in sequence: (1) name the problem and
  its practical settings in one sentence, (2) cite the NP-hardness result and note that
  exact methods only scale to small/medium instances, (3) state that evolutionary
  metaheuristics — naming the strongest prior one (a hybrid grouping GA) — are the
  modern answer for larger instances, then pivot to "this thesis proposes ACO instead,"
  with one sentence on ACO's origin (Dorigo, TSP) and its general mechanism (pheromone
  trail); (4) a short per-chapter roadmap paragraph, one sentence per chapter.
  No figures, no tables, no citations beyond inline numbered refs.
- **Transferable? Partly.** The four-move shape maps almost exactly onto MSNR's own
  introduction checklist (broader area → problem → motivation → prior-work summary →
  gap → goal/approach/results → roadmap), so structurally this is a strong template.
  Content-wise only moves (1)–(2) are shared with Nikola's problem (same NP-hardness
  result, same practical framing); move (3) is where the two theses diverge — Nikola's
  "this thesis proposes ___" pivot is a permutation-encoded, heuristic-seeded GA, not
  ACO — so the second half of this section is not reusable material, only a reusable
  *slot*.
- **Plagiarism-risk flag:** Moderate on moves (1)–(2) (shared problem framing,
  NP-hardness citation) — write independently from Garey & Johnson directly, not by
  paraphrasing her paraphrase.

### 1. Jednodimenzioni problem pakovanja (The 1D Bin Packing Problem)

**1.1 Matematička formulacija problema (Mathematical formulation)**
- **Purpose:** State the formal decision/optimization version of 1D-BPP: binary
  variables for item→bin assignment and bin-usage, the objective (minimize bins used),
  and the three constraints (capacity, exactly-one-bin-per-item, binary domains).
- **How it's organized:** One page, purely formal — a one-sentence verbal definition,
  then the two binary-variable definitions, the objective function, and four numbered
  constraints, each with a one-line gloss of what it enforces. No figures.
- **Transferable? Yes — this is the identical mathematical object Nikola's thesis is
  also solving**, so his methodology chapter needs the same formalization (it is the
  standard Garey & Johnson / Martello & Toth definition, not Rajačić's invention).
- **Plagiarism-risk flag: HIGH.** This is explicitly one of the three sections flagged
  in the task brief as maximum-temptation material. The binary-variable notation
  (`x_ij`, `y_i`) is standard across the whole BPP literature, so using the *same
  symbols* is fine and expected — but the surrounding sentences, the order in which
  constraints are introduced, and the glosses must be Nikola's own composition, derived
  directly from Garey & Johnson (1979) / Martello & Toth (1990), both already in his
  Zotero library.

**1.2 Problemi grupisanja (Grouping problems)**
- **Purpose:** Situate BPP inside a broader family of "grouping problems" — partition
  a set into disjoint subsets subject to a feasibility rule, optimizing some function of
  the resulting groups (not of individual items) — with graph coloring as the second
  example.
- **How it's organized:** Short (~1 page): a two-condition formal definition of a
  set partition, a paragraph of framing prose, then a small two-row table (BPP vs.
  graph coloring: constraint / objective function).
  A heading immediately followed by a short table-driven contrast.
- **Transferable? Partly.** The conceptual move — "BPP is an instance of a more general
  combinatorial family" — is a nice way to open a formulation chapter, but it is
  optional scaffolding, not something Nikola's thesis structurally needs (his THESIS_PLAN
  goes straight from the formulation to the heuristics/metaheuristics). Worth
  considering as an optional half-page if he wants an extra hook, not required.
- **Plagiarism-risk flag:** Low — this is generic combinatorics framing; if used at all,
  write it fresh rather than lift the two-condition setup verbatim.

**1.3 Dosadašnje rešavanje BPP-a (Prior approaches to solving BPP)**
- **Purpose:** Survey the solution landscape before presenting this thesis's method —
  exact methods (branch-and-bound), the classical fast heuristics, a dominance-based
  reduction procedure (Martello & Toth's MTP), the strongest existing metaheuristic
  (hybrid grouping GA / HGGA), and one existing ACO-based hybrid (HACO, Levine &
  Ducatelle) — ending with the observation that ACO is competitive with HGGA.
- **How it's organized:** ~2 pages, prose-only (no tables/figures/pseudocode — those
  are deferred to Chapter 2), organized as an ascending sequence: exact → simple
  heuristic → smarter reduction procedure → best-known metaheuristic → the specific
  prior ACO hybrid this thesis will build on. Each method gets 2–5 sentences: what it
  does, its complexity/quality trade-off, one citation.
- **Transferable? Partly.** The ascending "exact → fast heuristics → hybrid
  metaheuristic → this-thesis's-specific-family" survey arc is a solid template for a
  related-work section, and Nikola's own survey will have a structurally similar
  shape — ending at his own family (permutation GA + FF decoder) instead of ACO, and
  citing Falkenauer 1996, Reeves 1996, Scholl/BISON 1997, Munien 2020, Dokeroglu 2014
  where she cites HGGA and HACO.
- **Plagiarism-risk flag: HIGH** on the overlapping portions — the classical-heuristics
  summary and, especially, the HGGA description, since Nikola's own related-work section
  will describe the *same* Falkenauer HGGA (his THESIS_PLAN already lists it as "the
  heavyweight alternative"). Write the HGGA paragraph from Falkenauer (1996) directly.

**1.4 Primene (Applications)**
- **Purpose:** Motivate the problem's real-world relevance and connect 1D-BPP to the
  broader cutting-and-packing problem family (2D, 3D variants) before moving to
  algorithms.
- **How it's organized:** ~2 pages. Opens by placing BPP inside Dyckhoff's
  cutting-and-packing taxonomy (small objects into large objects, matched by pattern),
  then three bulleted real-world instantiations of 1D-BPP specifically (vehicle
  loading, cable/stock cutting, processor/job scheduling — each 3–5 sentences), then a
  short paragraph each on the 2D and 3D variants (definitions deferred to citations),
  closing with a paraphrase of Bischoff & Wäscher's three reasons cutting/packing
  problems are worth studying (industrial ubiquity, structural diversity despite
  surface similarity, NP-hardness).
- **Transferable? Yes, structurally** — an applications section that opens broad
  (the problem family) then narrows to 3–4 concrete bulleted use-cases is a reusable
  shape, and Nikola's own Motivation bullet in THESIS_PLAN already lists logistics,
  cutting stock, and memory allocation as candidates for exactly this kind of
  treatment.
- **Plagiarism-risk flag: HIGH** — explicitly flagged in the task brief. This is
  generic, widely-cited application material (same Dyckhoff/Bischoff & Wäscher
  sources Nikola could also cite — Wäscher & Gau 1996 is already in his library) but
  it must be independently written and, ideally, independently selected (he need not
  use the same three bullets — e.g., his own memory-allocation example is not one of
  hers and is worth leading with).

### 2. O algoritmima korišćenim u rešavanju problema pakovanja (Algorithms used)

**2.1 Heuristike (Heuristics: FFD, BFD, NFD, WFD)**
- **Purpose:** Formally define the four classical decreasing-order heuristics that
  will later serve as ACO's "heuristic information" input, and demonstrate they can
  diverge on a shared example.
- **How it's organized:** ~4 pages, one dedicated subsection per heuristic (FFD →
  BFD → NFD → WFD), each following an identical micro-structure: one paragraph of
  verbal definition, a boxed pseudocode listing (`Algoritam 2.1`–`2.4`), then one
  sentence on worst-case bound and time complexity. This is followed by a single
  shared worked example (§2.1.5): one concrete item list and bin capacity, packed by
  hand under FFD and NFD side by side, illustrated with a bin-diagram figure, showing
  the two heuristics produce different results (BFD/WFD are noted to coincide with FFD
  on this particular example, so are skipped).
- **Transferable? Yes — this is the single most directly reusable structural idea in
  the whole thesis.** Nikola's own heuristics chapter needs the same shape: one
  subsection per heuristic (his FF, BF, NF, Max-Rest, plus their decreasing variants)
  with definition + pseudocode + complexity, closed by one shared worked numeric
  example that shows two heuristics diverging. He in fact has a *stronger* example
  available than hers: his own Status notes document a real divergence (FFD using
  *more* bins than plain FF on Falkenauer triplet instances) — a genuinely interesting,
  literature-grounded divergence he can walk through by hand, rather than an arbitrary
  illustrative list.
- **Plagiarism-risk flag: HIGH.** Explicitly flagged in the task brief. This is the
  section covering the exact same four (or five, in Nikola's case with Max-Rest)
  algorithms his thesis defines. His pseudocode must be transcribed from his own
  working `heuristic.py` (which also has engineered lookup/PQ variants she doesn't
  have — an easy point of genuine differentiation), and his worked example must use
  his own numbers.

**2.2 Metaheuristike (Metaheuristics — general, then ACO, ACO-for-TSP, local search)**
- **Purpose:** Introduce metaheuristics as a class (above ordinary heuristics), then
  present ACO in full generality, its foundational application (TSP) as a worked
  precedent, and local search as a companion technique — all still *problem-agnostic*,
  before Chapter 3 specializes everything to BPP.
- **How it's organized:** ~8 pages across four subsections:
  - General metaheuristics intro (~1 page): etymology, one-line definition, the
    "heuristics work on one item, metaheuristics work on a collection and often
    delegate to a heuristic for decoding" distinction, a taxonomy note (nature-inspired
    metaheuristics), and the memory/no-memory dichotomy.
  - **2.2.1 ACO** (~4 pages): the ant-foraging metaphor with a figure, a boxed
    general-ACO pseudocode (`Algoritam 2.5`), then three named building blocks —
    solution construction, pheromone reinforcement (with two sub-phases: evaporation
    and reinforcement, the latter with four named strategies a–d) — closing with the
    "three central design decisions" summary and a pointer to convergence theory.
  - **2.2.2 ACO applied to TSP** (~3 pages): the original/foundational ACO
    application, presented as a fully worked instantiation of the general pattern —
    boxed pseudocode, concrete pheromone-trail definition, concrete construction
    probability formula, concrete reinforcement formula — closing with a list of other
    problems ACO has been adapted to and a small parameter table (β, ρ, ant count) with
    practical value ranges.
  - **2.2.3 Local search** (~2 pages): definition, a figure (local vs. global optimum),
    three search strategies (best-improvement, first-improvement, random), boxed
    pseudocode, and a note on its main weakness (local-optimum convergence) plus four
    named escape strategies.
- **Transferable? Partly — shape only, not content.** The "general metaheuristic →
  the chosen one in general/canonical form → a worked precedent application → an
  auxiliary technique used later" arc is a solid four-part template for a Chapter 2.
  For Nikola this maps to: general evolutionary-computation framing → GA in canonical
  form (encoding/selection/crossover/mutation/elitism, not yet BPP-specific) → a
  worked precedent (Falkenauer's grouping GA / GGA, already positioned in his
  THESIS_PLAN as the "heavyweight alternative" — exactly the same narrative role
  ACO-for-TSP plays here: an established prior application of the metaheuristic family
  worth walking through before his own adaptation) → an auxiliary technique slot,
  which for him could be heuristic decoding itself (FF as a decoder) rather than local
  search, since his design doesn't currently include a dedicated post-hoc local-search
  step. None of the ACO-specific content (pheromone mechanics, ant metaphor) transfers
  at all — it fills the *same chapter slot*, not the same idea.
- **Plagiarism-risk flag:** Low — this is ACO machinery Nikola's thesis does not use,
  so there is little practical temptation to reuse text here. The local-search
  subsection (§2.2.3) is the one piece of generically-transferable technique
  (best/first-improvement, escape strategies) if he ever wants to frame his mutation
  operator in those terms — treat with the same "own words" discipline as any other
  shared concept.

### 3. Prilagođavanje algoritama jednodimenzionom problemu pakovanja (Adapting the algorithms to 1D-BPP)

This chapter is the methodological core of her thesis — where the general ACO
machinery from Chapter 2 gets specialized to BPP — and it is **the single most
valuable structural template for Nikola's own Methodology chapter**, because his
THESIS_PLAN §3 already enumerates almost exactly this same slot-by-slot breakdown
(Encoding / Decoder / Genetic Operators / Fitness / Initialization) for his GA. See
the mapping table in Part 2 below for the component-by-component correspondence.

**3.1 Trag feromona (Pheromone trail, BPP-specific)**
- **Purpose:** Redefine the abstract "pheromone" concept from Chapter 2 concretely for
  BPP: τ(i,j) = the learned bias that two items of sizes i and j should end up in the
  same bin, rather than TSP's city-adjacency bias.
- **How it's organized:** Short (~1 page): one motivating sentence (grouping problem,
  not an ordering problem — a deliberate contrast with TSP), the new definition, and
  two bullets on why this particular definition was chosen (compact matrix; reusable
  learned "good pattern" once found).
- **Transferable? Yes, as a structural slot** — "what carries structural memory
  forward" is a question Nikola's Methodology chapter also has to answer, but the
  ACO answer (a shared pheromone matrix) and the GA answer (a permutation chromosome
  encoding + elitism) are mechanically unrelated — no content transfers.
- **Plagiarism-risk flag:** Low — mechanically specific to ACO.

**3.2 Heuristika (which heuristic feeds construction)**
- **Purpose:** State that FFD/NFD/BFD/WFD (from §2.1) each supply the "heuristic
  information" term μ(j) in the ant's construction probability, and that all four will
  be compared empirically in Chapter 4.
- **How it's organized:** ~1 page: restates how FFD/NFD differ mechanically from
  BFD/WFD (single pass vs. residual-space bookkeeping), then states μ(j) = item size.
- **Transferable?** Partly, as a slot — Nikola's Decoder subsection plays a related
  role (it also decides how a candidate solution gets turned into bins), but his
  design uses exactly one decoder (First-Fit) rather than four interchangeable
  heuristic-information sources compared head-to-head at this stage — his equivalent
  ablation (which seed heuristic feeds initialization) belongs later, at §5.3 in the
  proposed skeleton below.
- **Plagiarism-risk flag:** Low.

**3.3 Izgradnja rešenja (Solution construction — the probability formula)**
- **Purpose:** Give the exact formula an ant uses to pick which item to place next
  (a normalized product of pheromone and heuristic value over the feasible remaining
  items), plus how a bin's aggregate pheromone value is computed.
- **How it's organized:** ~1 page, two numbered formulas with a one-paragraph gloss
  each.
- **Transferable? Yes, as a slot — this is functionally "how does an abstract
  representation become a concrete packing,"** which is exactly the job Nikola's
  Decoder (First-Fit) subsection does. No formula content transfers (his decoder is
  deterministic given an order, not probabilistic), but the slot-position — right
  after "what carries memory" and "what heuristic informs it," right before "how is
  memory reinforced" — is a good ordering to imitate.
- **Plagiarism-risk flag:** Low — formula is ACO-specific.

**3.4 Pojačavanje feromona (Pheromone reinforcement)**
- **Purpose:** Specify the reinforcement rule actually used (an adaptation of Stützle
  & Hoos's Max-Min Ant System), including the BPP-specific twist that item pairs can
  co-occur multiple times in the best solution, and the γ parameter controlling
  iteration-best vs. global-best alternation.
- **How it's organized:** ~1.5 pages: one evaporation-and-reinforcement formula, a
  paragraph explaining the "only the best ant reinforces" design choice and its
  aggressiveness trade-off, then the γ-parameter explanation.
- **Transferable? Yes, as a slot** — this is "how does good structure propagate to
  influence the next round," which for Nikola is the job of his Genetic Operators
  subsection (selection + elitism specifically — elitism is the direct mechanical
  analog of "the best individual gets to influence the future," selection is the
  analog of the reinforcement probability). No formula content transfers.
- **Plagiarism-risk flag:** Low.

**3.5 Funkcija prilagođavanja (Fitness function)**
- **Purpose:** Justify why a naive "1/number-of-bins" fitness is inadequate (too many
  ties among equally-bin-count solutions) and present Falkenauer's z-power fitness as
  the fix, explaining the z parameter's role and citing z=2 as empirically optimal.
- **How it's organized:** ~1.5 pages: motivating problem (ties → no gradient) →
  Falkenauer & Delchambre's formula (numbered) → parameter interpretation (z=1 is
  trivial/equivalent to bin-count, larger z rewards uneven fill more) → z=2 justified
  by citation → two bullets on the fitness function's dual role in ACO (comparing ants;
  weighting reinforcement).
- **Transferable? Yes — and this is a point of DIRECT content correspondence, not
  just structural analogy**, since Nikola's own fitness function (per his
  THESIS_PLAN §3) is the *same* Falkenauer k-power objective, from the *same* source
  (Falkenauer & Delchambre 1992 / Falkenauer 1996).
- **Plagiarism-risk flag: HIGH — add this to the task brief's three named risk
  sections as a fourth.** Because both theses cite the identical formula from the
  identical source, the temptation to lightly reword her explanation of *why* the
  naive fitness fails and *why* z=2 is optimal will be strong. Write this
  independently from Falkenauer (1996)/Falkenauer & Delchambre (1992) directly —
  Nikola's own framing can differ (e.g., he can motivate it via his own FF-decoder
  angle: rewarding fuller bins guides the search toward orderings that pack well
  under FF, which is a genuinely different motivating narrative than hers).

**3.6 Lokalno pretraživanje (Local search, BPP-adapted) + 3.6.1 worked example**
- **Purpose:** Adapt generic local search (from §2.2.3) into a BPP-specific
  neighborhood move — empty the `loc` least-full bins, try to re-pack their freed
  items into the remaining bins for a tighter fit, then FFD the leftovers — and prove
  the mechanism with a fully worked numeric example (bin-by-bin before/after tables).
- **How it's organized:** ~2.5 pages: procedure description (~1 page: why an ACO
  solution benefits from post-hoc refinement, how the initial-solution problem is
  solved by letting ACO supply it, the `loc` parameter, the swap-until-no-improvement
  stopping rule, an explicit nod to Martello & Toth's dominance criterion as
  inspiration) followed by §3.6.1 (~1.5 pages), a fully concrete example: capacity 10,
  a 9-item list, `loc=2`, shown as a sequence of labeled bin-diagrams (before →
  bins-emptied/items-freed → per-bin swap attempts → FFD-mop-up → final result),
  ending with an explicit bin-count and "loss" (wasted-capacity) tally before and
  after.
- **Transferable? Partly, as a device — Nikola has no local-search component in his
  current design** (his THESIS_PLAN's Methodology stops at heuristic-seeded
  initialization + standard GA operators; no dedicated post-hoc refinement step), so
  this section's *content* has no home in his thesis. What is transferable is the
  **device**: a fully worked, bin-diagram-by-bin-diagram numeric example demonstrating
  one operator end-to-end is an excellent way to make an abstract mechanism concrete,
  and Nikola's Methodology chapter would benefit from the same device applied to his
  own heuristic-seeding step (walk through, on one small triplet-style instance, why
  seeding with unsorted-FF matters because FFD would do worse — this is a natural,
  already-motivated analog).
- **Plagiarism-risk flag: Moderate** if reused as a device — the specific numbers
  (capacity 10, that exact 9-item list) must not be recycled; construct an
  independent example, ideally one genuinely tied to his own triplet-instance finding
  rather than an arbitrary list.

### 4. Eksperimentalni rezultati (Experimental Results)

**4.1 Vrednosti parametara (Parameter values)** — six sub-subsections
(`br_mrava`/ant count, β, z, γ, ρ, `loc`)
- **Purpose:** Justify every tunable parameter's chosen value empirically before using
  it in the head-to-head comparisons that follow.
- **How it's organized:** ~4 pages, one near-identical micro-structure repeated six
  times: a paragraph on the parameter's role → a table of runtime (seconds) across
  four instance sizes (u120/u250/u500/u1000) and several candidate values → a closing
  sentence naming the chosen value and a one-line justification (sometimes purely
  empirical stability, sometimes tied to a cited theoretical result, e.g. z=2 sourced
  to Falkenauer). No bin-count/quality tables here — this subsection is about runtime
  behavior and parameter stability only; solution quality comparisons are deferred to
  §4.2–§4.4.
- **Transferable? Yes, directly** — Nikola's own experimental chapter needs exactly
  this move for POP_SIZE/GENERATIONS (and any operator-rate parameters he reports),
  and per the Status notes he has *already done* a version of this (the 40/50 vs.
  60/80 two-config comparison that locked POP_SIZE=40/GENERATIONS=50) — this section
  gives him a ready template for writing that comparison up formally, one
  parameter-value-vs-runtime(-or-quality) table per tunable parameter.
- **Plagiarism-risk flag:** Low — all numbers are hers, specific to her hardware and
  algorithm; no content overlap, only a reusable presentational template (one
  parameter per subsection, one table, one justified choice).

**4.2 Poređenje brzih heuristika (Comparison of the fast heuristics alone)**
- **Purpose:** Establish the baseline — compare FFD/NFD/BFD/WFD against each other
  (and against the theoretical optimum) purely as heuristics, with no metaheuristic
  involved yet, to motivate why a metaheuristic on top is worth the added cost.
- **How it's organized:** ~2 pages: a runtime table across instance sizes, a
  "solutions vs. optimum" table (`Opt+x` notation), a bar chart of the runtime table,
  and interpretive prose that never repeats the table's numbers, instead drawing the
  conclusion (FFD fastest and best quality; BFD/WFD much slower for no quality gain;
  none reach the theoretical optimum alone).
- **Transferable? Yes, directly — this is precisely the section Nikola's THESIS_PLAN
  already sketches** (his own FF/BF/NF/Max-Rest + FFD/BFD/NFD/MRD comparison table, for
  which `experiment_results.xlsx` already contains real data). The table-then-bar-chart
  presentation and the MSNR-compliant "interpret, don't repeat" prose discipline are a
  good model to imitate directly.
- **Plagiarism-risk flag:** Low — his numbers are entirely his own, from his own runs;
  only the presentational shape (table + chart + one-paragraph interpretation) carries
  over.

**4.3 Efikasnost ACO algoritma kombinovanog sa različitim heuristikama (ACO efficiency
combined with different heuristics)**
- **Purpose:** The core ablation of the thesis — show how much the *choice of
  heuristic feeding the metaheuristic* matters, both for runtime and for how close to
  optimal the combined method gets.
- **How it's organized:** ~2 pages: a runtime table (ACO+FFD, ACO+NFD, ACO+BFD,
  ACO+WFD, across instance sizes), a ranked ordering derived from it, then a second
  table showing bin-count-vs-optimum for the same four combinations, with prose
  explaining *why* FFD/NFD are faster (single-pass) yet a slower heuristic can still
  occasionally out-perform on quality — reconciling the runtime story with the
  quality story rather than conflating them.
- **Transferable? Yes — this is the single best structural match to a genuinely novel
  part of Nikola's own design.** His heuristic-seeded initialization (seeding the
  initial GA population with unsorted-FF, FFD, and BFD-grouping orders) is directly
  analogous to her "which heuristic feeds the metaheuristic" ablation — he can (and
  per his THESIS_PLAN implicitly should) report a comparable table: GA performance
  when seeded with only-FF vs. only-FFD vs. only-BFD vs. his actual all-three-combined
  seeding, isolating how much each seed source contributes. This section is the
  strongest ready-made template in the whole document for that experiment.
- **Plagiarism-risk flag:** Low — again, all numbers and the specific comparison are
  hers; the *idea* of running this ablation and the two-tables-plus-reconciling-prose
  shape are what transfers.

**4.4 Poređenje ACO algoritma sa drugim pristupima BPP-u (ACO vs. other approaches)**
- **Purpose:** Position the proposed hybrid against (a) other published algorithms for
  the same benchmark instances (MTP, HGGA, an "AP" algorithm) and (b) an exact
  integer-programming solver (AMPL, with CPLEX and Gurobi backends), to show
  competitiveness with the literature and near-exact solution quality.
- **How it's organized:** ~3 pages: runtime table + bin-count table + bar chart for
  the literature comparison (with an explicit CPU-scaling caveat since the algorithms
  ran on different machines), followed by a separate runtime-only table against
  AMPL/CPLEX/Gurobi on small instances (noting the solver's problem-size ceiling under
  a student license) with a short paragraph distinguishing what CPLEX vs. Gurobi vs.
  Minos can and cannot solve exactly.
- **Transferable? Yes, directly, and this is where Nikola's design already has a
  built-in equivalent.** Comparing against literature numbers maps to comparing
  against Falkenauer's/other published GGA results; comparing against an exact solver
  maps to Nikola's `Solutions.xlsx` lookup of 6195 known optimal/best solutions
  (already integrated via `solution_manager.py`) — functionally the same role as her
  live AMPL run, except he already has the ground truth pre-computed rather than
  needing to solve instances exactly himself. His methods/results chapters can
  present the "gap to known-optimal" comparison as the direct analog of her §4.4
  AMPL table, without needing an exact solver at all.
- **Plagiarism-risk flag:** Low — no shared numbers; only the two-pronged
  "literature + exact-ground-truth" comparison shape transfers.

### 5. Zaključak (Conclusion)
- **Purpose:** Recap the problem's everyday relevance, summarize that the proposed
  hybrid (heuristic + ACO + local search) achieves excellent/near-optimal results
  competitive with the best prior methods, and name a direction for future work.
- **How it's organized:** ~1.5 pages, two paragraphs: the first opens broadly
  (packing/scheduling problems as a source of everyday inefficiency — trains, buses,
  class schedules — before narrowing back to the mathematical framing and the range of
  applications covered in Chapter 1), the second is the technical recap (confirms the
  hybrid method matches/beats prior best methods) plus one closing sentence on future
  work (further combining fast/efficient algorithms).
- **Transferable? Partly.** The technical-recap paragraph's shape (state what was
  tested → state the honest result → name the trade-off/limitation → point to future
  work) matches good practice and already matches the tone of Nikola's own Status-note
  conclusion draft ("dominates by construction... trade-off is runtime..."). The
  broad-then-narrow rhetorical opening (everyday-life framing of packing problems) is
  a stylistic choice specific to her, not a structural necessity — MSNR explicitly
  warns against stock/empty openers, so this particular move is one to consciously
  *not* imitate rather than adapt.
- **Plagiarism-risk flag:** Moderate on the opening rhetorical flourish specifically —
  low temptation on the technical recap, since Nikola's results are entirely his own
  and already drafted independently in THESIS_PLAN §6.

### Bibliografija (Bibliography)
- **Purpose:** List all 30 cited works.
- **How it's organized:** Sorted by first initial of the lead author's given name (an
  unusual but internally consistent scheme — not strictly alphabetical by surname),
  each entry giving authors, title, venue/publisher, year, and pages — numeric
  in-text citation style throughout (`[3]`, `[12]`, etc.).
- **Transferable? Yes, as a formatting convention** — MSNR requires picking one
  citation style and being consistent (§2.7); numeric bracketed citation with a
  matching numbered reference list is one of MSNR's three sanctioned styles and is
  what her thesis uses throughout. Nikola's own reference management (BibTeX, per
  MSNR's recommendation) makes this largely automatic regardless of which style he
  picks.
- **Plagiarism-risk flag:** None — a reference list is not prose to plagiarize; it's
  the citation contents that matter, and Nikola's own reference list (THESIS_PLAN §7)
  is already independently populated from his own Zotero library.

---

## 2. GA-adaptation mapping: Rajačić's ACO components → Nikola's GA analogs

| # | Rajačić (ACO) — section | Structural role it fills | Nikola (GA) analog | Correspondence |
|---|---|---|---|---|
| 1 | §3.1 Trag feromona — τ(i,j): learned bias that item-sizes i,j co-occur in a bin | Persistent memory of "good structure" carried across iterations | **Permutation encoding** (chromosome = item order) reinforced by **elitism** | Analogy only — ACO's memory is an explicit shared matrix updated every iteration; the GA's memory is implicit, carried by which chromosomes survive |
| 2 | §3.2 Heuristika — μ(j) = item size feeds each construction step | Injects domain/greedy bias into every construction decision | **Heuristic-seeded initialization** (population seeded with unsorted-FF, FFD, BFD-grouping orders) | Analogy, different timing — ACO re-injects the heuristic bias probabilistically at *every* step of *every* iteration; the GA injects it *once*, at population initialization, then leaves it to selection/crossover/mutation |
| 3 | §3.3 Izgradnja rešenja — probabilistic bin-filling formula | Turns the abstract representation into a concrete packing | **Decoder = First-Fit (FF)** | Direct structural analog — "how do you turn the representation into bins" — though the GA's decoder is deterministic given an order, not probabilistic |
| 4 | §3.4 Pojačavanje feromona — Max-Min AS reinforcement, iteration-best vs. global-best | Propagates the best-found structure forward to bias future generations | **Genetic operators: tournament selection + elitism** | Analogy — both answer "how does the best solution influence what comes next," by different mechanisms (shared-matrix reinforcement vs. chromosome survival/selection pressure) |
| 5 | §3.5 Funkcija prilagođavanja — Falkenauer's z-power fitness | Quality signal driving comparison and reinforcement/selection | **Fitness function — the same Falkenauer k-power fitness** | **Direct correspondence** — identical formula, same source (Falkenauer & Delchambre); the one component with genuine content overlap, hence flagged HIGH RISK above |
| 6 | §3.6 Lokalno pretraživanje — `loc`-bin-emptying post-hoc refinement | Local refinement of each constructed solution before evaluation/reinforcement | *No direct analog in the current design* — closest role split across **crossover** (recombination) and **mutation** (small perturbation) | Genuine gap, not a hidden equivalence — worth naming explicitly as a possible future-work extension rather than implying his GA already does this |
| — | *(no ACO equivalent — she constructs from scratch every iteration)* | — | **Heuristic-seeded initialization** as a one-time population-construction step | Nikola-side addition with no structural slot in her thesis — a genuine point of departure worth stating plainly, not squeezed into the mapping above it |

---

## 3. Proposed chapter skeleton for Nikola's GA thesis

Modeled on Rajačić's proven shape, adapted for GA content, and cross-checked against
`THESIS_PLAN.md` and the MSNR structure (`writing/msnr-style-guide.md`: Title →
Abstract+keywords → TOC → Introduction → Elaboration → Conclusions → Acknowledgments
(optional) → Literature → Appendices (optional)).

**Predgovor (Preface)** — optional acknowledgments; no technical content.

**Uvod (Introduction)** — one line: problem + NP-hardness + why a GA over plain
classical heuristics + one-paragraph roadmap of the chapters below. (Write last, per
MSNR §3.)

**1. Jednodimenzioni problem pakovanja (The 1D Bin Packing Problem)**
- *1.1 Matematička formulacija problema* — the standard Garey & Johnson/Martello &
  Toth formalization, written from the primary sources.
- *1.2 Dosadašnji pristupi rešavanju BPP-a* — exact methods → classical fast
  heuristics → Falkenauer's HGGA → other metaheuristics (ACO/Rajačić, PSO, etc. per
  Munien 2020) — his own related-work survey.
- *1.3 Primene* — a short, independently-chosen set of real-world use cases (logistics,
  cutting stock, memory/CPU allocation are already his own candidates per THESIS_PLAN).

**2. Algoritmi za rešavanje BPP (Algorithms for solving BPP)**
- *2.1 Klasične heuristike* — FF, BF, NF, Max-Rest + their decreasing variants
  (FFD/BFD/NFD/MRD), one subsection each (definition + his own pseudocode, grounded in
  `heuristic.py`, incl. the engineered lookup/PQ variants) + one shared worked example
  demonstrating a real divergence (ideally the documented FF-vs-FFD triplet-instance
  finding from his Status notes).
- *2.2 Genetski algoritmi u opštem obliku* — GA as a metaheuristic family in canonical
  form (encoding, selection, crossover, mutation, elitism), not yet BPP-specific — the
  general-metaheuristic-then-worked-precedent slot.
- *2.3 Grupišući genetski algoritam (Falkenauer's GGA)* — the established "heavyweight"
  prior application of GAs to BPP, presented as a worked precedent before his own
  adaptation (fills the role her ACO-for-TSP subsection plays: a concrete, well-known
  instantiation of the metaheuristic family, on a related problem/approach, before he
  narrows to his own design).

**3. Metodologija: Hibridni permutacioni GA za BPP (Methodology)** — the core chapter,
mirroring Rajačić's Chapter 3 slot-by-slot (see mapping table above):
- *3.1 Kodiranje rešenja* — permutation chromosome.
- *3.2 Dekoder: First-Fit* — how a permutation becomes a packing.
- *3.3 Genetski operatori* — tournament selection, order/PMX crossover, swap/inversion
  mutation, elitism.
- *3.4 Funkcija prilagođavanja* — Falkenauer's k-power fitness, independently derived
  and motivated via his own FF-decoder framing.
- *3.5 Inicijalizacija: heurističko zasejavanje populacije* — his genuinely novel
  component (seeding with unsorted-FF/FFD/BFD-grouping orders + elitism guarantee),
  with its own small worked example analogous in *device* (not content) to her
  §3.6.1 — why the unsorted-FF seed specifically matters on triplet instances.

**4. Implementacija (Implementation)** — language/platform (Python), data structures
(Chromosome class), the `construct_bins` Next-Fit→First-Fit upgrade, visualization.
No direct Rajačić-chapter equivalent — an addition consistent with MSNR's Elaboration
allowing an explicit implementation component.

**5. Eksperimentalni rezultati (Experimental Results)** — mirrors Rajačić's Chapter 4
slot-by-slot:
- *5.1 Vrednosti parametara* — POP_SIZE/GENERATIONS (already empirically locked at
  40/50 per the Status notes; write up that comparison formally), plus any
  operator-rate parameters, one table per parameter as she does.
- *5.2 Poređenje klasičnih heuristika* — FF/BF/NF/Max-Rest + decreasing variants,
  runtime + bin-count tables (data already in `experiment_results.xlsx`), direct
  structural analog of her §4.2.
- *5.3 Efikasnost GA u odnosu na različita zasejavanja* — the heuristic-seeding
  ablation (GA seeded with only-FF vs. only-FFD vs. only-BFD vs. his actual combined
  seeding) — direct structural analog of her §4.3, and arguably the strongest
  ready-made template in this whole mapping for a genuinely novel part of his design.
- *5.4 Poređenje GA sa drugim pristupima* — vs. literature GGA/heuristic numbers, and
  vs. `Solutions.xlsx`'s 6195 known-optimal/best solutions as the ground-truth
  baseline — direct structural analog of her §4.4 (literature comparison + exact-solver
  comparison), except his "exact solver" is a pre-computed lookup rather than a live
  AMPL run.

**Zaključak (Conclusion)** — technical recap (GA dominates FF/FFD/BFD by construction;
matches/improves on First-Fit on tested instances; trade-off is runtime, not quality)
already drafted in THESIS_PLAN §6 in the right register — keep that honest,
non-rhetorical tone rather than adopting her broad-to-narrow philosophical opening.

**Bibliografija** — already populated per THESIS_PLAN §7, managed via BibTeX per MSNR.

---

*Compiled from a full read of `RajacicJasna.pdf` (all 52 pages, via
`zotero_read_pdf_pages` against the file at
`C:\Users\thegr\Zotero\storage\A4TXVCY7\RajacicJasna.pdf` — the Zotero metadata/fulltext
tools could not resolve this item directly because it is a bare, parent-less attachment
currently in the Zotero Trash; see the note below and in CLAUDE.md's known-gaps list).*
