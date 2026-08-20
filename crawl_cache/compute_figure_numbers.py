#!/usr/bin/env python3
"""
Compute every number in Figure 1 of the CIKM cam-ready from the crawl cache
and papers.json. Replaces the stale patch_figure.py (which targeted a
now-renamed .tex, read a `relevant` key the counts files no longer emit,
and predates the three-panel layout).

Panels (a)/(b): loa{1,2,3}_counts.json  -> panel_a / panel_b
Panel (c):      papers.json             -> cumulative risk_type A / E

Run:  python3 crawl_cache/compute_figure_numbers.py
"""
import json, re
from pathlib import Path
from collections import defaultdict

CACHE = Path(__file__).parent
REPO  = CACHE.parent
YEARS = [2020, 2021, 2022, 2023, 2024, 2025, 2026]

# TikZ geometry of the cam-ready figure (unchanged by this script)
X_POS   = {2020: 0.925, 2021: 2.025, 2022: 3.125, 2023: 4.225,
           2024: 5.325, 2025: 6.425, 2026: 7.525}
BAR_HALF = 0.425
STRETCH  = 1.35          # all y-coords are (count/scale) * 1.35
SCALE_A, SCALE_B, SCALE_C = 30, 200, 40

def y(count, scale):
    return round(count / scale * STRETCH, 3)

# ── panels (a)/(b) ────────────────────────────────────────────────────────────
counts = {}
for loa in (1, 2, 3):
    counts[loa] = json.loads((CACHE / f"loa{loa}_counts.json").read_text())["years"]

def cell(loa, yr, key):
    return counts[loa].get(str(yr), {}).get(key, 0)

# ── panel (c) ─────────────────────────────────────────────────────────────────
papers = json.loads((REPO / "papers.json").read_text())

def get_year(p):
    """arXiv id encodes YYMM; fall back to a 20xx in venue, then to `year`."""
    m = re.match(r"^(\d{2})(\d{2})\.", str(p.get("id") or ""))
    if m:
        return 2000 + int(m.group(1))
    m = re.search(r"(20\d\d)", str(p.get("venue") or ""))
    if m:
        return int(m.group(1))
    if p.get("year"):
        return int(p["year"])
    return None

annual = defaultdict(lambda: defaultdict(int))
unattributed = []
for p in papers:
    rt = p.get("risk_type")
    if rt not in ("A", "E"):
        continue
    yr = get_year(p)
    if yr is None:
        unattributed.append(p.get("title", "?")[:60]); continue
    annual[yr][rt] += 1

# ── report ────────────────────────────────────────────────────────────────────
print(f"Panel (a) RecSys+IR   [1 unit = {SCALE_A} papers, x{STRETCH}]")
print(f"  {'Year':>5} {'L1':>4} {'L2':>4} {'L3':>4} | {'ya':>6} {'yb':>6} {'yc':>6}")
for yr in YEARS:
    a, b, c = (cell(l, yr, "panel_a") for l in (1, 2, 3))
    print(f"  {yr:>5} {a:>4} {b:>4} {c:>4} | {y(a,SCALE_A):>6.3f} "
          f"{y(a+b,SCALE_A):>6.3f} {y(a+b+c,SCALE_A):>6.3f}")

print(f"\nPanel (b) all agentic AI safety   [1 unit = {SCALE_B} papers, x{STRETCH}]")
print(f"  {'Year':>5} {'L1':>4} {'L2':>4} {'L3':>4} | {'ya':>6} {'yb':>6} {'yc':>6}")
for yr in YEARS:
    a, b, c = (cell(l, yr, "panel_b") for l in (1, 2, 3))
    print(f"  {yr:>5} {a:>4} {b:>4} {c:>4} | {y(a,SCALE_B):>6.3f} "
          f"{y(a+b,SCALE_B):>6.3f} {y(a+b+c,SCALE_B):>6.3f}")

print(f"\nPanel (c) cumulative risk class   [1 unit = {SCALE_C} papers, x{STRETCH}]")
print(f"  {'Year':>5} {'A':>3} {'E':>3} {'cumA':>5} {'cumE':>5} | {'yA':>6} {'yE':>6}")
ca = ce = 0
for yr in YEARS:
    ca += annual[yr]["A"]; ce += annual[yr]["E"]
    print(f"  {yr:>5} {annual[yr]['A']:>3} {annual[yr]['E']:>3} {ca:>5} {ce:>5} | "
          f"{y(ca,SCALE_C):>6.3f} {y(ce,SCALE_C):>6.3f}")

# ── headroom checks: do the hand-set axis maxima still fit? ────────────────────
max_a = max(sum(cell(l, yr, "panel_a") for l in (1,2,3)) for yr in YEARS)
max_b = max(sum(cell(l, yr, "panel_b") for l in (1,2,3)) for yr in YEARS)
print(f"\nHeadroom  panel(a) max={max_a} (top tick 60)"
      f"  panel(b) max={max_b} (top tick 400)  panel(c) cumA={ca} (top tick 80)")
for lbl, mx, top in (("a", max_a, 60), ("b", max_b, 400), ("c", ca, 80)):
    if mx > top:
        print(f"  !! panel ({lbl}) exceeds its top tick ({mx} > {top}) — rescale needed")
if unattributed:
    print(f"\n{len(unattributed)} tagged paper(s) with no recoverable year:")
    for t in unattributed: print(f"  - {t}")
