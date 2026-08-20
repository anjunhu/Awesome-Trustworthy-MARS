#!/usr/bin/env python3
"""
Top up any query that hit the arXiv result cap during a historical crawl.

arXiv returns newest-first, so a query that fills its page has silently dropped
older matches for that tier-year. This re-runs only those queries at a higher
cap and unions the extra records into the existing loa{N}_{YYYY}_raw.json,
reproducing crawl_arxiv's record shape exactly.

Usage:
  python3 crawl_cache/topup_capbound.py <crawl.log> [--cap 2000] [--apply]
Without --apply it reports what it would fetch and changes nothing.
"""
import json, re, sys, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import crawler

CACHE = Path(__file__).parent

def parse_log(path):
    """Yield (loa, year, date_from, date_to, query) for each CAP-BOUND line."""
    tier = year = dfrom = dto = None
    out = []
    hdr = re.compile(r"LoA-(\d+)\s*\|\s*(\d{4})\s*\((\d{8})\s*→\s*(\d{8})\)")
    cap = re.compile(r"CAP-BOUND: '(.+?)' returned the full")
    for line in Path(path).read_text(errors="replace").split("\n"):
        m = hdr.search(line)
        if m:
            tier, year, dfrom, dto = int(m[1]), int(m[2]), m[3], m[4]
        m = cap.search(line)
        if m and tier:
            out.append((tier, year, dfrom, dto, m[1]))
    return out

def build_record(r, loa):
    kw = {"classical": loa == 1, "loa2": loa == 2, "loa3": loa == 3}
    rel = crawler.is_relevant(r["title"], r["abstract"], **kw)
    tags = crawler.classify_paper(r["title"], r["abstract"])
    if loa == 1:
        tags["risk_type"] = tags.get("risk_type") or "A"
    notes = {1: "classical adversarial RecSys",
             2: "single-agent LLM recommender",
             3: "multi-agent LLM recommender"}[loa]
    return {
        "id": r["id"], "title": r["title"], "abstract": r["abstract"],
        "authors": r["authors"], "venue": f"arXiv {r['published'][:4]}",
        "section": tags["section"], "risk_type": tags["risk_type"],
        "scope": tags["scope"], "threat_tier": tags["threat_tier"],
        "github": None, "doi": None, "notes": notes, "is_relevant": rel,
    }

ap = argparse.ArgumentParser()
ap.add_argument("log"); ap.add_argument("--cap", type=int, default=2000)
ap.add_argument("--apply", action="store_true")
a = ap.parse_args()

jobs = parse_log(a.log)
print(f"{len(jobs)} cap-bound quer{'y' if len(jobs)==1 else 'ies'} to top up "
      f"(cap {a.cap}, apply={a.apply})\n")

for loa, year, dfrom, dto, query in jobs:
    path = CACHE / f"loa{loa}_{year}_raw.json"
    existing = json.loads(path.read_text())
    have = {p["id"] for p in existing}
    print(f"loa{loa} {year}  '{query}'  (currently {len(existing)} raw)")
    if not a.apply:
        print("   [dry-run] would refetch at higher cap\n"); continue
    res = crawler.arxiv_search(query, max_results=a.cap,
                               date_from=dfrom, date_to=dto)
    if len(res) >= a.cap:
        print(f"   !! still cap-bound at {a.cap} — raise further")
    added = [build_record(r, loa) for r in res if r["id"] not in have]
    rel_added = sum(1 for p in added if p["is_relevant"])
    merged = existing + added
    path.write_text(json.dumps(merged, indent=2))
    print(f"   fetched {len(res)}, added {len(added)} new "
          f"({rel_added} relevant) -> {len(merged)} raw\n")
