#!/usr/bin/env python3
"""
Compile per-year raw crawl JSONs into per-tier counts for the figure.

Architecture:
  loa{N}_YYYY_raw.json  — broad crawl (panel b scope, no RecSys restriction)
  loa{N}_YYYY.json      — filtered to is_relevant=True (also panel b)
  loa{N}_counts.json    — per-year: panel_b (all relevant) + panel_a (RecSys+IR subset)

Panel (a) is always a strict subset of panel (b):
  panel_b = all papers where is_relevant=True, after priority deduplication
  panel_a = panel_b ∩ RECSYS_IR_FILTER

Priority deduplication (applied per year to panel_b):
  A paper belongs exclusively to its highest applicable tier.
  LoA-3 > LoA-2 > LoA-1: if a paper appears in both LoA-1 and LoA-2 for
  the same year, it is counted only in LoA-2.
"""
import json, sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))
from crawler import RECSYS_IR_FILTER   # kept for reference; is_recsys_ir uses a two-tier version

CACHE = Path(__file__).parent
YEARS = [2020, 2021, 2022, 2023, 2024, 2025, 2026]

# Two-tier RecSys/IR filter:
#   STRONG  — specific enough to accept in title OR abstract (any count)
#   REPEATED — accept in title, or if appearing ≥2× in abstract to rule out
#              one-sentence incidental mentions in general surveys
#   TITLE_ONLY — too generic for abstract: "matrix factorization" is NMF/NNMF in
#                image/medical papers; only trusted when it appears in the title
RECSYS_IR_STRONG = [
    "recsys",
    "collaborative filtering", "rating prediction",
    "user-item", "item recommendation", "personalized recommendation",
    "search ranking", "document ranking",
    "shilling attack",              # RecSys-specific attack term
    "sequential recommendation",
    "information retrieval",        # includes music/audio IR — intentionally broad
    "retrieval system",
]
RECSYS_IR_REPEATED = [
    "recommender system",           # require ≥2× in abstract to exclude one-sentence
    "recommendation system",        # incidental mentions in general surveys
]
RECSYS_IR_TITLE_ONLY = [
    "matrix factorization",         # NMF/NNMF is used in image/neuro decomposition;
                                    # only trusted when focal in the title
]

# Later re-submissions of papers already counted in an earlier year bucket.
# Keep the earliest arXiv ID; exclude these duplicates from counting.
KNOWN_DUPES = {
    "2511.06143",  # duplicate of 2409.19096 ("Enhancing Robustness of GNNs through p-Laplacian")
}

# Historical floors: LLM-agent safety research did not meaningfully exist before these years.
# Years before the floor are forced to zero to avoid false positives from classical MARL / NLP.
#   LoA-2 (single-agent LLM): ChatGPT / GPT-3.5 era → 2022
#   LoA-3 (multi-agent LLM): GPT-4 multi-agent era  → 2023
LOA_MIN_YEAR = {1: 2020, 2: 2022, 3: 2023}

LOA_META = {
    1: {
        "label": "Pre-LLM+ICL adversarial RecSys/IR",
        "description": (
            "Broad crawl: adversarial attacks on classical retrieval/ranking/RecSys. "
            "panel_b = relevant papers not claimed by LoA-2/3; panel_a = RecSys+IR subset."
        ),
    },
    2: {
        "label": "Single-agent LLM systems",
        "description": (
            "Broad crawl: single-agent LLM safety (any domain, multi-agent excluded). "
            "panel_b = relevant papers not claimed by LoA-3; panel_a = RecSys+IR subset."
        ),
    },
    3: {
        "label": "Multi-agent LLM systems",
        "description": (
            "Broad crawl: multi-agent LLM safety (any domain). "
            "panel_b = all relevant; panel_a = RecSys+IR subset via RECSYS_IR_FILTER."
        ),
    },
}


def is_recsys_ir(paper: dict) -> bool:
    title    = paper.get('title', '').lower()
    abstract = paper.get('abstract', '').lower()
    combined = f"{title} {abstract}"
    if any(kw in combined for kw in RECSYS_IR_STRONG):
        return True
    for kw in RECSYS_IR_REPEATED:
        if kw in title:
            return True
        if abstract.count(kw) >= 2:   # ≥2 occurrences rules out one-sentence survey mentions
            return True
    if any(kw in title for kw in RECSYS_IR_TITLE_ONLY):
        return True
    return False


# ── Step 1: load raw relevant sets per tier per year ──────────────────────────
raw_relevant = {loa: {} for loa in LOA_META}
raw_counts   = {loa: {} for loa in LOA_META}

for loa in LOA_META:
    for year in YEARS:
        raw_path = CACHE / f"loa{loa}_{year}_raw.json"
        if not raw_path.exists():
            raw_relevant[loa][year] = []
            raw_counts[loa][year]   = 0
            continue
        raw = json.loads(raw_path.read_text())
        raw_counts[loa][year] = len(raw)
        if year < LOA_MIN_YEAR[loa]:
            raw_relevant[loa][year] = []   # pre-LLM era: no valid L2/L3 papers
        else:
            raw_relevant[loa][year] = [
                p for p in raw
                if p.get("is_relevant", False) and p.get("id") not in KNOWN_DUPES
            ]

# ── Step 2: priority deduplication per year ───────────────────────────────────
# LoA-3 owns its papers; LoA-2 owns its papers minus LoA-3; LoA-1 gets the rest.
deduped = {loa: {} for loa in LOA_META}
removed = defaultdict(lambda: defaultdict(int))   # removed[loa][year] = count

for year in YEARS:
    ids3 = {p["id"] for p in raw_relevant[3][year]}
    ids2 = {p["id"] for p in raw_relevant[2][year]}

    loa3 = raw_relevant[3][year]
    loa2 = [p for p in raw_relevant[2][year] if p["id"] not in ids3]
    loa1 = [p for p in raw_relevant[1][year] if p["id"] not in ids2 and p["id"] not in ids3]

    removed[2][year] = len(raw_relevant[2][year]) - len(loa2)
    removed[1][year] = len(raw_relevant[1][year]) - len(loa1)

    deduped[3][year] = loa3
    deduped[2][year] = loa2
    deduped[1][year] = loa1

# ── Step 3: compute counts and write filtered JSONs ───────────────────────────
all_counts = {loa: {} for loa in LOA_META}

for loa, meta in LOA_META.items():
    print(f"\n{'='*60}")
    print(f"  LoA-{loa}: {meta['label']}")
    print(f"{'='*60}")

    for year in YEARS:
        relevant = deduped[loa][year]
        recsys   = [p for p in relevant if is_recsys_ir(p)]

        filtered_path = CACHE / f"loa{loa}_{year}.json"
        filtered_path.write_text(json.dumps(relevant, indent=2))

        dup_note = f"  (-{removed[loa][year]} dedup)" if removed[loa][year] else ""
        all_counts[loa][year] = {
            "raw":     raw_counts[loa][year],
            "panel_b": len(relevant),
            "panel_a": len(recsys),
        }
        print(f"  [{year}]  raw={raw_counts[loa][year]:4d}  panel_b={len(relevant):4d}"
              f"  panel_a={len(recsys):4d}{dup_note}")

    counts_out = {
        "description": meta["description"],
        "generated": "2026-06-17",
        "years": {str(y): all_counts[loa][y] for y in YEARS},
    }
    (CACHE / f"loa{loa}_counts.json").write_text(json.dumps(counts_out, indent=2))
    print(f"  → loa{loa}_counts.json")

# ── Validation: confirm no cross-tier duplicates remain ───────────────────────
print("\n" + "="*72)
print("  Post-dedup cross-tier overlap check (all should be 0)")
print("="*72)
for year in YEARS:
    i1 = {p["id"] for p in deduped[1][year]}
    i2 = {p["id"] for p in deduped[2][year]}
    i3 = {p["id"] for p in deduped[3][year]}
    o12, o13, o23 = len(i1&i2), len(i1&i3), len(i2&i3)
    flag = " FAIL" if (o12 or o13 or o23) else " ok"
    print(f"  {year}  L1∩L2={o12}  L1∩L3={o13}  L2∩L3={o23}{flag}")

# ── Figure validation table ───────────────────────────────────────────────────
print("\n" + "="*72)
print("  Figure validation: panel (a) and (b) counts by LoA and year")
print("="*72)
header = f"{'Year':>6}  {'(a)L1':>6} {'(b)L1':>6}  {'(a)L2':>6} {'(b)L2':>6}  {'(a)L3':>6} {'(b)L3':>6}"
print(header)
print("-"*72)
for year in YEARS:
    row = f"{year:>6}"
    for loa in [1, 2, 3]:
        c = all_counts[loa].get(year, {})
        row += f"  {str(c.get('panel_a','—')):>6} {str(c.get('panel_b','—')):>6}"
    print(row)
