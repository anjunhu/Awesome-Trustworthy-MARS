# Crawler Workflow

This document describes how the reading list in `README.md` is maintained.

## Pipeline

### Stage 1 — High-recall crawl → `raw_crawl.json`

```bash
python3 crawler.py --from YYYYMMDD --to YYYYMMDD --save-raw raw_crawl.json --no-commit
```

Queries arXiv, HuggingFace Papers, and OpenReview (if credentials set) with broad keyword combinations from `SEARCH_GROUPS`. No relevance filtering is applied. All results are written to `raw_crawl.json` with `is_relevant` pre-scored but not used to exclude anything. This is the audit trail of everything the crawler saw.

### Stage 2 — Relevance filter + tagging → `papers.json`

Runs automatically as part of Stage 1 when `--save-raw` is used. Papers in `raw_crawl.json` with `is_relevant=True` (must match at least one term from `RELEVANCE_SYSTEM` **and** one from `RELEVANCE_RISK`) are classified by `classify_paper()` into section, scope, threat\_tier, and risk\_type, then appended to `papers.json`.

### Stage 3 — README regeneration → `README.md`

Also runs automatically. `generate_readme()` reads `papers.json` and rebuilds `README.md` from scratch, grouped by taxonomy section.

### Stage 4 — Commit

```bash
git add raw_crawl.json papers.json README.md
git commit -m "docs: crawler update YYYY-MM-DD (+N new papers)"
```

## Date windows

Always set `--from` to the date of the last crawl and `--to` to today, so no window is missed or double-counted. The last crawl date can be read from the **Last updated** line at the top of `README.md`.

## Manual additions

To add a paper without crawling, edit `papers.json` directly and run:

```bash
python3 crawler.py --no-crawl --no-commit
```

This regenerates `README.md` from the updated `papers.json`.

## OpenReview

Set `OPENREVIEW_USERNAME` and `OPENREVIEW_PASSWORD` environment variables to enable OpenReview crawling. Without them, that source is silently skipped.

## Scheduled runs

`.github/workflows/crawl.yml` runs the crawler automatically on a schedule. It uses the same pipeline above.
