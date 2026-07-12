# literature/sources.json

Structured table of sources cited in the thesis, maintained by the `researcher` subagent
(`.claude/agents/researcher.md`). All 31 reference items already live in the Zotero library,
in the "master" collection (key `QPVIL3YR`) — this file does not duplicate them, it links to
them by `item_key` and records what's actually usable for writing: quotes, locations, and
relevance to specific thesis sections.

## Schema

Each entry in the `sources` array:

- `item_key` — Zotero item key (fetch full metadata/PDF via the zotero MCP tools)
- `title`, `authors`, `year`, `venue`
- `zotero_collection` — which Zotero collection it's filed under
- `tags` — short topical tags (e.g. `"grouping-ga"`, `"encoding"`, `"benchmark"`)
- `relevance` — one or two sentences on why this source matters to the thesis
- `quotes` — array of `{ text, location, note }`; `location` must be a page/section, not a guess
- `cited_in_sections` — thesis sections where this source is (or will be) cited

Entries are added on demand as sources are actually used in writing, not pre-populated for
the whole library — an entry without a real quote/location isn't useful for citation.
