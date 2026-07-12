# MSNR Style Guide — actionable checklist

Distilled from **MSNR** (Metodologija stručnog i naučnog rada, Milena Vujošević
Janičić, Matematički fakultet) — the writing standard for Nikola's master's thesis.
The thesis is written in **Serbian**. This is the checklist the `copy-editor` agent
enforces and that drafting should follow.

## Document structure (§2.1)
Title · Abstract + keywords · Table of contents · Introduction (Uvod) ·
Elaboration (Razrada) · Conclusions (Zaključci) · Acknowledgments (optional) ·
Literature · Appendices (optional).

## Title (§2.2)
Informative, short (a few words), clear (no abbreviations except universally known
e.g. WWW), precise, attractive. Avoid empty openers ("Razmatranje…", "Jedna studija
o…").

## Abstract + keywords (§2.2)
One self-contained paragraph. State the problem and main results; motivate (why the
topic matters); no references, no abbreviations. **Write it LAST.** Keywords = the
terms someone would search to find the work.

## Introduction (§2.3)
Broader area + the specific problem; motivation/justification; summary of relevant
prior work and literature; what is still missing; your goal, approach, and main
results. Intrigue the reader. **Write it near the end**, before the abstract. Intro
and abstract are similar but must NOT repeat each other.

## Elaboration / Razrada (§2.4)
Contains (as relevant): definitions, notation; description of algorithm/formalism/
theorem + proof or proof sketch; properties (complexity, correctness); applications/
consequences; system architecture and design; implementation; experiments, results,
evaluation. Ways to develop a topic: examples, definitions, comparison/contrast,
component analysis, classification, cause-effect.

### Paragraphs (pasus) — strict rules
- Structure: **topic (thesis) sentence** → **supporting sentences** (evidence,
  logical argument, representative examples) → **concluding sentence** → a link
  sentence to the next paragraph.
- **One idea per paragraph.**
- **Never a single-sentence paragraph.**
- **A paragraph is NOT a list/enumeration.**
- A heading must be followed by at least one paragraph of text before any
  subheading (no heading-immediately-under-heading).

### Coherence
One topic per paragraph; consistent style; do **not** mix tenses, do not mix
address, do not mix active/passive.

## Tables and figures (§2.4)
- Every table/figure **must be referenced from the text** ("… prikazano je u
  Tabeli 3 / na Slici 3 …"). In LaTeX use `\label{}` / `\ref{}`.
- Must be **self-contained** — understandable without reading the body text.
- The body text **interprets** the results; it must **not repeat the numbers** from
  the table/figure.
- **Tables**: natural (horizontal/vertical) format; avoid vertical rules between
  columns; avoid unnecessary horizontal rules; for complex tables leave a blank
  line every 5th row; group similar items, separate different ones; align
  comparisons vertically; concise; pull shared content into the header/caption;
  **caption ABOVE the table, no trailing period**; uniform alignment.
- **Figures**: **caption BELOW**; standalone-readable; clear, high resolution;
  avoid overcrowded or empty figures. Graphs: ≤3 lines; mark the points; no 3D;
  connect points only for continuous data (not for discrete). Bar charts for
  comparison; labels unambiguously attached to bars, no connecting lines. Pie
  charts: start at 12 o'clock, largest segment first, 5–7 segments, labels outside.
- Tables emphasize specific values/parameter estimates; figures emphasize general
  relationships between parameters. Choose deliberately.

## Citation (§2.7)
- **Every claim** must be backed either by a citation or by the work's own content
  (results, proven statements, interpretation). Cite near the claim, usually at the
  end of the sentence.
- Styles: numeric `[3]`, author–date `(Lankford, 1975)` / `Wolper (1996a)`, or
  abbreviation `[VW94]`. Pick ONE and be consistent. Manage with BibTeX.
- Reference list sorted alphabetically by first author's surname, or by order of
  appearance. Each entry: authors, title, journal/proceedings, year, pages.

## Plagiarism (§2.7) — see the `plagiarism-guard` agent
- Taking (part of) a text and merely adding a reference is **NOT** proper citation.
- Only small parts may be quoted verbatim, and they must be clearly set apart
  (quotation marks, indentation, italic).
- Everything else must be **retold** — paraphrased into your own words, keeping only
  the essence relevant to your thesis — and cited.

## Language faults to avoid (§3)
Stock phrases/metaphors; redundant words ("potencijalni rizik", "prošla istorija");
colloquialisms ("genijalac", "pomračen um"); word repetition; empty qualifiers
("slabo", "često", "jako", "bezbroj puta", "enormno"); grammatical/stylistic errors
("trebamo da", "mi bi"); naive/arrogant phrasing ("kao što dobro znamo",
"očigledno", "kao što je opšte poznato", "u mnogim slučajevima").

## General writing process (§3)
- **Top-down**: design the structure first, then fill in details.
- **Inside-out**: write the body first, then the introduction and conclusion.
- **Abstract last** (plus keywords).
- Write the first draft fast, then read carefully and polish. Take a 1–2 day break
  to catch errors. Some errors are only visible in print.
- Check all facts and conclusions (do conclusions follow from the facts?). Remove
  redundancy and repetition. Ensure figures/tables are clear and referenced.
- Text should be: clear, concise, correct, efficient, complete, self-contained.
- "If something can be interpreted in more than one way, it is wrong."
- "If you cannot think of a reason to put a comma in, leave it out."

> Writing is learned by READING and WRITING.
