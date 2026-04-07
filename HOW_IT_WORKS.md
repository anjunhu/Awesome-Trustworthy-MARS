# How the Crawler Works

> The full reading list is maintained in [README.md](README.md).

The crawler (`crawler.py`) runs weekly via GitHub Actions and keeps the reading list up to date automatically. It has four stages.

---

## Stage 1 — Crawl

Three sources are queried:

1. **arXiv** — iterates every query in `SEARCH_GROUPS` (system, risk, and defence terms) against the arXiv API with a configurable `submittedDate` window (default: 2025-01-01 to 2026-03-31), fetching up to 15 results per query. Requests are spaced 5 s apart with exponential backoff on rate limits.

2. **OpenReview** — fetches all submissions from three hardcoded venues (`NeurIPS.cc/2025`, `ICLR.cc/2026`, `RecSys.org/2025`). Requires `OPENREVIEW_USERNAME` and `OPENREVIEW_PASSWORD` environment variables.

3. **HuggingFace Papers** — uses `HfApi.list_papers()` with four keywords (`multi-agent`, `recommender`, `LLM agent`, `agentic`), up to 50 results each.

---

## Stage 2 — Filter

`is_relevant(title, abstract)` applies **AND logic** across two keyword lists:

- **System terms** — must match at least one (e.g. `"recommender system"`, `"multi-agent llm"`)
- **Risk terms** — must match at least one (e.g. `"prompt injection"`, `"guardrail"`, `"safety"`)

Run with `--save-raw FILE` to save all unfiltered results first, then apply the relevance filter in a second pass. Duplicates are removed by checking both `id` and `arxiv_id` against existing entries in `papers.json`.

---

## Stage 3 — Tag

`classify_paper(title, abstract)` assigns four tags by first-match on keyword rules:

| Field | What it captures | Default |
|-------|-----------------|---------|
| `section` | Reading list section (e.g. `rf1_injection`, `rf3_interagent`, `defence`) | `misc` |
| `scope` | Evaluation scope: `composition`, `interaction`, or `component` | `component` |
| `threat_tier` | Threat driver: `compromise`, `misalignment`, or `drift` | `drift` |
| `risk_type` | `E` (emergent) or `A` (amplified) | `None` |

---

## Stage 4 — Write

- **`papers.json`** — new entries appended and saved
- **[README.md](README.md)** — fully regenerated: papers grouped by `section`, one Markdown table per section, taxonomy overview prepended
- **Git commit** — message format `docs: weekly crawler update YYYY-MM-DD (+N new papers)` (skip with `--no-commit`)

---

## CLI flags

```
python3 crawler.py                        # full run
python3 crawler.py --dry-run              # crawl only, no writes
python3 crawler.py --no-crawl             # regenerate README from existing papers.json
python3 crawler.py --no-commit            # write files, skip git commit
python3 crawler.py --save-raw raw.json    # save unfiltered crawl before filtering
python3 crawler.py --from 20250101 --to 20260331  # custom date window
```

---

## Adding a paper manually

Edit `papers.json` directly, then run:

```
python3 crawler.py --no-crawl --no-commit
```
