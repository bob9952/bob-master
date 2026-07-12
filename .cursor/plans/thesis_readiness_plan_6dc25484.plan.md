---
name: Thesis Readiness Plan
overview: Assess current 1D-BPP implementation against thesis requirements, then close the highest-impact gaps in scientific rigor, reproducibility, and reporting so the work is defensible for a Master thesis.
todos:
  - id: protocol
    content: Define deterministic benchmark protocol (seeded sampling + 10 runs/instance + metadata capture).
    status: pending
  - id: schema
    content: Extend experiment outputs with per-heuristic gap metrics and aggregated summary sheets in Excel.
    status: pending
  - id: stats
    content: Add GA-vs-baseline statistical comparison (win/tie/loss, mean/std, optional Wilcoxon).
    status: pending
  - id: plots
    content: Add thesis-grade plots (boxplots, convergence summary, speed-quality tradeoff).
    status: pending
  - id: docs
    content: Document heuristic-variant mapping and reproducibility instructions for thesis appendix.
    status: pending
isProject: false
---

# Thesis Readiness and Improvement Plan

## Current Status (What Is Already Strong)

- Core pipeline is in place and coherent: parser + heuristics + GA + solution lookup + experiment runner + plotting.
- Implemented baselines already cover your thesis proposal scope and more: FF/BF/NF/MR and decreasing/optimized variants in [project/src/heuristic.py](project/src/heuristic.py).
- Data ingestion supports mixed BPPLIB formats (single and Falkenauer multi-instance) in [project/src/parser.py](project/src/parser.py).
- Best-known values are loaded from all `Solutions.xlsx` sheets in [project/src/solution_manager.py](project/src/solution_manager.py).
- Experiment/report outputs are already thesis-usable (`.xlsx`, `.txt`, plots) via [project/run_experiments.py](project/run_experiments.py) and [project/plot_results.py](project/plot_results.py).

## Main Gaps To Close Before Thesis Submission

- **Scientific rigor gap**: experiments currently use `RUNS_PER_INSTANCE = 1` and random sampling; thesis needs repeated runs, fixed seeds, and uncertainty reporting.
- **Comparability gap**: console/report focus on raw bins/time, but thesis needs normalized metrics (avg gap %, std, win-rate, rank).
- **Methodology clarity gap**: naming/variant mapping (FF/FFL/FFD+ etc.) should be explicitly documented and aligned with your literature table.
- **Reproducibility gap**: no explicit experiment configuration manifest (seed list, selected instances, GA params) saved per run.

## Implementation Plan

### 1) Freeze a Reproducible Benchmark Protocol

- Add a deterministic experiment mode in [project/run_experiments.py](project/run_experiments.py):
  - global seed, per-instance seed list, and saved sampled-instance list.
  - configurable `runs_per_instance` (e.g., 10 like Munien-style protocol).
- Persist a `metadata` sheet in `experiment_results.xlsx` containing:
  - timestamp, git/hash (if available), GA parameters, seed policy, dataset selection.

### 2) Upgrade Result Schema for Thesis Statistics

- Extend row schema in [project/run_experiments.py](project/run_experiments.py) to include:
  - per-heuristic gap (`Gap_FF`, `Gap_FFD`, ...), relative gap %, and best-algorithm flag.
- Add aggregated sheets in the same Excel file:
  - `instance_level`, `category_summary`, `algorithm_summary`.
- Include mean/std/min/max for both bins and time across repeated GA runs.

### 3) Add Statistical Comparison Layer

- Create a lightweight analysis script (new file, e.g. `project/analyze_results.py`) that computes:
  - paired comparison GA vs key baselines (FFD, BFD, BFL, MR+),
  - win/tie/loss counts by category,
  - optional non-parametric test (Wilcoxon signed-rank) when dependencies are available.
- Export a thesis-ready text summary and one compact table for direct insertion in chapter “Results and Discussion”.

### 4) Improve Visualization for Thesis Narrative

- Extend [project/plot_results.py](project/plot_results.py) with:
  - boxplots of gap by algorithm and category,
  - GA convergence summary (median + quartiles across selected instances),
  - speed-quality scatter (`time` vs `gap`) to show tradeoff.
- Keep existing bar plots, but add consistent ordering and labels matching thesis notation.

### 5) Validate Heuristic Variant Mapping and Documentation

- In [project/src/heuristic.py](project/src/heuristic.py), explicitly document mapping to literature labels:
  - `MR`, `MR+`, `FF`, `FFL (FF++)`, `FFD`, `FFD+`, `NF`, `NFD`, `NFD+`, `BF`, etc.
- Add a small reference section in thesis docs (`THESIS_PLAN.md` update) that states exactly which variants are implemented vs deferred (e.g., segment-tree/BST variants).

### 6) Final Thesis Packaging

- Prepare final “experiment pack” folder under `project/results/`:
  - final Excel, final TXT summary, plots, selected instance list, config metadata.
- Add a short `REPRODUCIBILITY.md` with exact run commands and expected outputs for supervisor review.

## Scope Recommendation

- **Enough for thesis now?** Yes, for implementation scope.
- **Needed to make it academically strong?** Add reproducibility + repeated-run statistics + statistical comparison before writing final conclusions.

## Minimal Priority Path (If Time Is Tight)

- Implement Steps 1, 2, and part of 4 first.
- Then run one final large benchmark and lock the results as “thesis final”.

