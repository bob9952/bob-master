Use straightforward, neutral language. Keep explanations concise and direct.

In existing code, inspect the surrounding implementation and follow local patterns. Prefer small, scoped, testable changes over broad rewrites.

For Apollo/Webix work, treat SLC001 metadata as the source of UI structure and behavior. Prefer established BINDVAR, BINDQUERY, backend triggers, post_change, row_changed, button_click, and execute_query patterns.

Avoid unnecessary abstraction. Preserve legacy paths unless the task explicitly targets them. Before changing code, explain the data flow and why the change fits existing behavior; afterwards, run focused validation.

When a `.codegraph/` directory exists at the repository root, use CodeGraph before text search or file reading to locate and understand code. Otherwise, use normal repository search.

# Thesis repository guidance

This repository supports Nikola Subotic's Serbian-language master's thesis on one-dimensional bin packing with a genetic algorithm and heuristic benchmarks.

- Use `supervisor` for research framing and structure, `researcher` for literature records, `plagiarism-guard` for source-overlap review, `copy-editor` for Serbian prose, and `experiment-analyst` for experiment execution and real-result reporting.
- Keep academic work evidence-based: do not invent citations, quotes, page numbers, experiment results, or claims of originality.
- Preserve experiment parameters unless the user explicitly changes them. Every Python experiment command must activate Conda environment `ai` in the same shell invocation.

<!-- BEGIN zotero-cli skill (managed by `zotero-mcp install-skill`) -->

## Zotero library access

Use Zotero from the shell with `zotero-cli` when the task needs library metadata, PDFs, notes, or annotations.

Read `lib/zotero-docs/for-agents.md` and `lib/zotero-docs/cli.md` before using it. Prefer the CLI over a Zotero MCP server when shell access is available: the MCP tool schemas add substantial context on every request.

Quick check that it is set up: `zotero-cli config`. Pass `--json` whenever you will parse the output; check `ok` before using `data`.

Confirm before destructive or broad Zotero writes (deletes, duplicate merges, batch edits, and annotation changes). Zotero writes may sync to the user's other devices.

<!-- END zotero-cli skill -->
