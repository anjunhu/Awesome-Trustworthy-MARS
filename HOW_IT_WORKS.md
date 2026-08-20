# How the Crawler Works

> The full reading list is maintained in [README.md](README.md).

The crawler (`crawler.py`) runs weekly via GitHub Actions and keeps the reading list up to date automatically. It has four stages.

---

## Stage 1 — Crawl

Three sources are queried:

1. **arXiv** — iterates every query in `SEARCH_GROUPS` (system, risk, and defence terms) against the arXiv API with a configurable `submittedDate` window (default: 2025-01-01 to 2026-08-16), fetching up to 25 results per query, newest first. Requests are spaced `ARXIV_DELAY` seconds apart (default 20) with up to `ARXIV_RETRIES` attempts (default 5) and exponential backoff.

   > **Pacing matters.** A tier crawl issues ~20 queries back-to-back. At the previous 8 s spacing this reliably tripped HTTP 429, and because a query that exhausts its retries returns an empty list, whole queries were dropped *silently* — which looks identical to "no papers matched that year" and corrupts the figure counts. Always check the run log for `request failed` before trusting a crawl.

2. **OpenReview** — fetches all submissions from three hardcoded venues (`NeurIPS.cc/2025`, `ICLR.cc/2026`, `RecSys.org/2025`). Requires `OPENREVIEW_USERNAME` and `OPENREVIEW_PASSWORD` environment variables.

3. **HuggingFace Papers** — uses `HfApi.list_papers()` with four keywords (`multi-agent`, `recommender`, `LLM agent`, `agentic`), up to 50 results each.

Sources 2 and 3 are queried **only** in default mode. Any tier flag (`--classical`/`--loa2`/`--loa3`) implies arXiv-only, and `--arxiv-only` forces it in default mode too. The figure crawls are arXiv-only by design: it needs no auth and is the most reliable of the three.

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
python3 crawler.py --from 20250101 --to 20260816  # custom date window
python3 crawler.py --arxiv-only           # skip OpenReview + HuggingFace
ARXIV_DELAY=30 python3 crawler.py         # slow the crawl further if 429s appear
```

---

## Adding a paper manually

Edit `papers.json` directly, then run:

```
python3 crawler.py --no-crawl --no-commit
```
