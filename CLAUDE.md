# Master Thesis: 1D Bin Packing Problem via Genetic Algorithm

Nikola Subotic's master's thesis at University of Belgrade, Faculty of Mathematics:
**"Solving the One-Dimensional Bin Packing Problem Using a Genetic Algorithm"** — a
Permutation GA (First-Fit decoder) benchmarked against classical heuristics (FF, BF, NF,
Max-Rest and their decreasing variants).

## Document roles — read this before editing any thesis doc

- **`MasteThesis.md`** — the translated, **already-submitted** official thesis proposal.
  This is the ground-truth scope/topic. **Do not edit it.** If working docs drift from it,
  fix the working docs to match — additively, never by removing what's already there.
- **`THESIS_PLAN.md`**, **`IMPLEMENTATION_PLAN.md`** — working/planning docs, safe to edit.
  Keep them aligned with `MasteThesis.md`'s scope (FF, BF, NF, Max-Rest + FFD/NFD, plus
  BFD as an extra the working docs added on top — that extra is fine, just don't drop the
  official ones).
- **`cursor_master_thesis_implementation_pla.md`** — a raw ~30k-line Cursor chat transcript
  documenting the GA/heuristics build history. Reference only, not a planning doc.

## Code (`project/`)

- `src/heuristic.py` — `first_fit`, `next_fit`, `best_fit`, `max_rest` (all real, not
  stubs), plus engineered lookup/PQ variants `first_fit_lookup`, `best_fit_lookup`,
  `max_rest_pq` for speed, and `counting_sort` for the decreasing-order pre-sort (→ FFD,
  BFD, NFD, MRD).
- `src/ga.py`, `src/chromosome.py` — permutation-encoded GA, FF decoder, Falkenauer's
  k²-fill-ratio fitness, tournament selection, order-crossover (cut-and-fill), swap
  mutation, elitism.
- `src/parser.py` — reads both Falkenauer multi-instance and Scholl/Hard28 single-instance
  BPPLIB formats.
- `src/solution_manager.py` — loads `data/Solutions.xlsx` (6195 known optimal/best
  solutions across 9 sheets), matches 1255/1263 local instance files (99.4%).
- `run_experiments.py` — current params are a **smoke test**, explicitly commented
  "Reduced for faster testing": `POP_SIZE=40, GENERATIONS=50, RUNS_PER_INSTANCE=1`. Not a
  tuned final run.
- Python env: `.cursorrules` says `conda activate ai`, but that **FAILS in non-interactive
  shells** ("Run 'conda init' before 'conda activate'"). The working invocation is to call the
  env's python directly: `G:\Users\thegr\miniconda3\envs\ai\python.exe <script>` (miniconda is
  on the **G:** drive, not C:). The `experiment-analyst` agent knows this workaround.

## Data source

All benchmark instances (Falkenauer, Scholl, Wäscher, Schoenfield/Hard28 — 1263 files
total) come from **BPPLIB** (Delorme, Iori & Martello, 2018), which is checked in as a git
submodule at `BPPLIB/`. BPPLIB's own citation requirement: cite Delorme/Iori/Martello 2018
whenever using their material — this is now in `THESIS_PLAN.md`/`IMPLEMENTATION_PLAN.md`
references.

## Zotero

- MCP server registered in `.mcp.json` (project-scoped), connects to the running Zotero
  desktop app's local API. **Local-only mode: read/search works, but writes (new items,
  new collections, metadata edits) require a Web API key**, which Nikola has declined to
  set up for now — so all Zotero writes must happen manually in Zotero desktop.
- All thesis literature lives in the **"master"** collection (key `QPVIL3YR`), 31 items.
- **RajacicJasna in Zotero — RESOLVED (2026-07-10):** now a proper item `SJPC9D5E`
  ("Rajacic Jasna master 2013", type document, 2013) — searchable and usable by the
  plagiarism-guard. The PDF physically lives at `storage\A4TXVCY7\RajacicJasna.pdf` (the
  old bare/trashed attachment); if MCP fulltext won't resolve, read it via
  `zotero_read_pdf_pages`. Citation verified: "Rešavanje jednodimenzionog problema
  pakovanja kombinovanjem optimizacionih metoda", Rajačić Jasna, 2013.
- Structural reference for thesis writing: **`writing/rajacic-structure-breakdown.md`** —
  a section-by-section analytical map of Rajacic's thesis (NOT a translation), with an
  ACO→GA component mapping and a proposed MSNR-compliant chapter skeleton for Nikola's GA
  thesis. Reference only; never a source of prose.
- Literature gap analysis + acquire/file checklist lives in **`literature/to-add.md`** — keep
  it as the source of truth for what still needs adding. As of 2026-07-09:
  - Added since first pass: BPPLIB 2018 (`99FRTI6H`), Wäscher & Gau 1996 (`VJSUR4U8`),
    Coffman/Garey/Johnson 1984 (`FRBA429M`, unfiled), Martello & Toth 1990 (`MPPFL5QZ`, unfiled).
  - Just need FILING into "master" collection (manual drag-drop): `FRBA429M`, `MPPFL5QZ`.
    Also a duplicate Falkenauer 1996 — `T6KJYXY8` is TRASHED, `2CV824V5` is live; merge/clean up.
  - Still to ACQUIRE (identifier-import): Falkenauer & Delchambre 1992
    (DOI `10.1109/ROBOT.1992.220088`), Delorme/Iori/Martello 2016 EJOR
    (DOI `10.1016/j.ejor.2016.04.030`), Garey & Johnson 1979 (ISBN `9780716710455`).
  - Schoenfield 2002 — unpublished tech report, no DOI/PDF; manual "Report" item if wanted.
- `literature/sources.json` (+ `literature/README.md`) — structured citation/quote table,
  maintained by the `researcher` subagent. Empty until sources are actually drawn on for
  writing.

## Writing phase — decisions (2026-07-10)

- **The final thesis is written in SERBIAN.** Working/planning docs (THESIS_PLAN.md,
  IMPLEMENTATION_PLAN.md, CLAUDE.md) stay in English; MasteThesis.md is an English
  translation of the submitted Serbian proposal. Draft actual thesis prose in Serbian.
- **Script & terminology (locked 2026-07-10):** thesis prose in **Cyrillic (ћирилица)**;
  core terms **предмет** (item) / **кутија** (bin), used consistently per MSNR. Foreign
  author names and English technical terms stay in Latin within the Cyrillic text
  (bibliography is BibTeX/Latin). Note Rajačić's thesis is in Latin — an extra layer of
  surface distinctness.
- **Chapter drafts** live in `writing/teza/` (readable Cyrillic markdown). **Chapter 1 +
  Увод complete** — `00-uvod.md` (unnumbered intro: motivation + contribution + chapter
  roadmap; roadmap references Ch2–6 which don't exist yet, so it's provisional) and `01-…md`
  (§1.1 formulation, §1.2 prior approaches, §1.3 applications). §1.2 was **strengthened
  (2026-07-11)** to engage Falkenauer's documented critique of the permutation-GA+FF-decoder
  family and frame heuristic seeding as the answer. All of Увод/§1.1/§1.2/§1.3 are
  plagiarism-guard-cleared (incl. the §1.3 Dyckhoff-typology citation fix and the §1.2 "A1"
  GGA-one-liner rewording) and MSNR-polished.
- **Compiled thesis** lives in `writing/master-thesis/` (Filip Marić's official `matfmaster`
  template). xelatex is NOT installed, so it builds with **pdflatex + bibtex** via
  `build.bat <name>` (verified — `master-thesis.pdf` compiles clean, **14 pp** as of 2026-07-11).
  `master-thesis.tex` (main + metadata) `\input`s `uvod.tex` then `poglavlje1.tex` (Увод + Ch1 in
  LaTeX, numeric `\cite` → `master-thesis.bib`, **13 curated refs** — added `johnson1974` primary
  bounds source + `dyckhoff1990` C&P typology on 2026-07-11; `dyckhoff1990` is in the .bib but NOT
  yet in the Zotero "master" collection, add manually if wanted). Title-page metadata (mentor/committee/year), abstract,
  and biografija are TODO placeholders for Nikola to fill/verify. Gotcha: `\begin{english}` is
  xelatex-only — under pdflatex use `\foreignlanguage{english}{…}` or `{\lat …}` for Latin
  snippets. Per-item Zotero BibTeX export mangles dates into invalid keys/years — clean by hand.
- **Paper study-notes** in `literature/digests/` (6 key papers, researcher-made) — **rebuilt
  comprehensive 2026-07-11** (section-by-section walkthroughs, 326–557 lines each, with
  page-located quotes; thin ~70-line versions replaced). Reading material for improving the
  intro; study notes only, not thesis prose. Two findings worth acting on: **Munien 2020 names
  "random initial population" as a future-work gap** (the heuristic seeding fills it — a framing
  point for §1.2/Увод), and **Delorme 2016 relays Gent 1998 that most Falkenauer instances are
  "very easy"** (a caveat for honest Ch5 results framing — lean on Hard28/Schoenfield).
- **Writing standard = MSNR** (Metodologija stručnog i naučnog rada). Full text in
  `MSNR_rules.txt`; actionable checklist distilled in **`writing/msnr-style-guide.md`**
  (structure, paragraph rules, table/figure rules, citation styles, language faults).
  The `copy-editor` agent enforces it.
- **RajacicJasna (Zotero `A4TXVCY7`)** — a Serbian ACO-based 1D-BPP master's thesis,
  structurally close to Nikola's (same problem, same FFD/BFD/NFD/WFD baseline, but ACO
  not GA). Use it **only** as a structural model + citable related-work source. Its prose
  must NOT be translated-and-adapted — that is plagiarism (MSNR "find-and-replace"/
  "remix"). Nikola chose a **structured-understanding** breakdown, not a verbatim
  translation. The `plagiarism-guard` agent exists to enforce this.

## Subagents (`.claude/agents/`)

- **supervisor** — brainstorming/critique partner, no edit access, opus model.
- **researcher** — Zotero-connected (`mcp__zotero__*`), maintains `literature/sources.json`.
- **copy-editor** — suggests Serbian prose fixes + enforces MSNR style (no edit access —
  this is Nikola's writing to own).
- **experiment-analyst** — runs/validates `project/` experiments, writes results from real
  output only.
- **plagiarism-guard** — checks Serbian draft passages against the source corpus (esp.
  RajacicJasna) for too-close text, grounded in MSNR's plagiarism taxonomy; report-only,
  opus model.

## Status as of 2026-07-09 — known open issues

1. **GA-vs-First-Fit: FIXED & CONFIRMED (2026-07-09) via heuristic seeding.** `project/src/ga.py`
   seeds the initial population with the natural-FF, FFD, and BFD-grouping orders (`_seed_orders`,
   `initialize_population`); with elitism this guarantees GA ≤ best-seed-heuristic ≤ FF by
   construction. Config **locked at POP_SIZE=40/GENERATIONS=50** after a 30-instance two-config
   comparison (60/80 gave only 4 bins/2394 = 0.17% at 2.46x runtime — not worth it; see scratchpad
   `config_compare.log`). `experiment_results.xlsx`/`.txt` **regenerated 2026-07-09 23:30 with the
   seeded GA at 40/50** (a fresh 30-instance sample): GA never loses to FF (30/30), ties where FF
   is already optimal, strictly beats FF on 4/30, hits optimum on 17/30. Results table also now
   visibly shows FFD > FF on triplet instances (e.g. Falkenauer_t60: FF 20, FFD 24) — the reason
   the unsorted-FF seed matters.
   - **Still open**: this is the SAMPLED (30-instance) run only — no full 1263-instance sweep yet.
     And `run_experiments.py` uses an UNSEEDED `random.sample`, so every run draws a different 30 —
     **set a fixed random seed before the official thesis run** for reproducibility.
2. `THESIS_PLAN.md` §6 conclusion + §3 methodology (heuristic-seeding) + copy-editor nits
   (§5 "(Yours)"→"(This Work)", §3 "trick" phrasing) were rewritten this session to match the
   seeded-GA reality honestly.
3. Citation coverage was thin (only Falkenauer substantively cited); Scholl, BPPLIB,
   Wäscher & Gau, Schoenfield, and Martello & Toth were added to references in this
   session — see Zotero gap list above for which still need manual library import.
4. `project/results/` (plots, xlsx) may intentionally not be pushed to GitHub yet —
   Nikola was still deciding as of this session; don't assume either way, ask if it comes up.
