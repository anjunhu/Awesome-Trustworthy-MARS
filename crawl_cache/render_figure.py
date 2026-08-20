#!/usr/bin/env python3
"""
Regenerate the three data panels of Figure 1 in the CIKM cam-ready from the
crawl cache + papers.json, and patch them into the .tex in place.

Panels (a)/(b): stacked bars, loa{1,2,3}_counts.json (panel_a / panel_b keys)
Panel (c):      cumulative risk_type A/E lines, papers.json

Axis scales are chosen from the data so the tallest bar sits comfortably under
the top tick; the hand-tuned styling (bold orange top tick, legend placement,
rotated labels) is reproduced rather than discarded.

Usage:
  python3 crawl_cache/render_figure.py            # dry-run, prints numbers + diff stat
  python3 crawl_cache/render_figure.py --apply    # patch the .tex
"""
import json, re, sys, os, argparse, math
from pathlib import Path
from collections import defaultdict

CACHE = Path(__file__).parent
REPO  = CACHE.parent
TEX   = Path(os.environ.get("FIG_TEX", REPO.parent / "cacr-tutorial" / "tutorial_proposal_cikm_camready.tex"))
YEARS = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
X     = {y: 0.925 + 1.1*i for i, y in enumerate(YEARS)}
HALF, STRETCH = 0.425, 1.35
AXIS_TOP = 2.700          # y of the bold top tick, fixed by the layout

def nice_scale(maxval, n_units=2.0):
    """Pick a round papers-per-unit so maxval lands under AXIS_TOP."""
    raw = maxval / (AXIS_TOP / STRETCH)
    for step in (5,10,20,25,30,40,50,60,70,75,80,100,125,150,200,250,300,400,500):
        if step >= raw: return step
    return int(math.ceil(raw/500)*500)


def nice_ticks(scale):
    """Round gridline values below the top tick, with a legible gap from it."""
    top = AXIS_TOP/STRETCH*scale
    for step in (1,2,5,10,20,25,50,100,200,250,500,1000):
        n = int(top // step)
        if 3 <= n <= 6:
            break
    else:
        step = max(int(top//4), 1)
    # keep a visual gap so the last gridline label cannot touch the bold top tick
    return [t for t in range(0, int(top)+1, step)
            if t/scale*STRETCH < AXIS_TOP - 0.18]

# ── data ──────────────────────────────────────────────────────────────────────
counts = {l: json.loads((CACHE/f"loa{l}_counts.json").read_text())["years"] for l in (1,2,3)}
def c(l, y, k): return counts[l].get(str(y), {}).get(k, 0)

papers = json.loads((REPO/"papers.json").read_text())
def year_of(p):
    m = re.match(r"^(\d{2})(\d{2})\.", str(p.get("id") or ""))
    if m: return 2000+int(m.group(1))
    m = re.search(r"(20\d\d)", str(p.get("venue") or ""))
    return int(m.group(1)) if m else None
ann = defaultdict(lambda: defaultdict(int))
for p in papers:
    rt = p.get("risk_type")
    if rt in ("A","E"):
        y = year_of(p)
        if y: ann[y][rt] += 1

# ── panel renderers ───────────────────────────────────────────────────────────
def render_bars(key, scale, xshift, caption, legend_lbls):
    L = lambda y: (c(1,y,key), c(2,y,key), c(3,y,key))
    Y = lambda v: round(v/scale*STRETCH, 3)
    out = [f"  %% ── Panel ({caption[0]}): {caption[1]} ──",
           f"  %%   scale 1 unit = {scale} papers; y = count/{scale} x {STRETCH}",
           f"  %%   Year  L1   L2   L3    ya      yb      yc"]
    for y in YEARS:
        a,b,d = L(y)
        out.append(f"  %%   {y} {a:4d} {b:4d} {d:4d}  {Y(a):.3f}  {Y(a+b):.3f}  {Y(a+b+d):.3f}")
    out.append(f"  \\begin{{scope}}[xshift={xshift}cm, yshift=0cm]")
    out.append( "    \\draw[thick,axgray] (0,0) -- (8.5,0) node[right,axgray]{\\small Year};")
    out.append( "    \\draw[thick,axgray] (0,0) -- (0,3.24)")
    out.append( "      node[above,axgray,align=center]{\\small arXiv~count};")
    # gridlines below the top tick
    ticks = nice_ticks(scale)
    out.append("    \\foreach \\y/\\lbl in {" + ", ".join(f"{Y(t):.3f}/{t}" for t in ticks) + "}{")
    out.append("      \\draw[axgray!50,thin] (0,\\y) -- (8.2,\\y);")
    out.append("      \\node[left,axgray,font=\\sffamily\\footnotesize] at (-0.1,\\y) {\\lbl};")
    out.append("    }")
    top = int(round(AXIS_TOP/STRETCH*scale))
    out.append(f"    \\draw[axgray!50,thin] (0,{AXIS_TOP:.3f}) -- (8.2,{AXIS_TOP:.3f});")
    out.append(f"    \\node[left,font=\\sffamily\\footnotesize\\bfseries,loa3col] "
               f"at (-0.1,{AXIS_TOP:.3f}) {{\\textbf{{{top}}}}};")
    out.append("")
    for y in YEARS:
        a,b,d = L(y); xl,xr,xm = X[y]-HALF, X[y]+HALF, X[y]
        ya,yb,yc = Y(a), Y(a+b), Y(a+b+d)
        out.append(f"    %% {y}: L1={a} L2={b} L3={d}")
        if a: out.append(f"    \\fill[loa1col] ({xl:.3f},0) rectangle ({xr:.3f},{ya:.3f});")
        if b: out.append(f"    \\fill[loa2col] ({xl:.3f},{ya:.3f}) rectangle ({xr:.3f},{yb:.3f});")
        if d: out.append(f"    \\fill[loa3col] ({xl:.3f},{yb:.3f}) rectangle ({xr:.3f},{yc:.3f});")
        # label a segment only when it is tall enough to hold text
        if a and ya > 0.28:
            out.append(f"    \\node[font=\\sffamily\\scriptsize,axgray!80!black,rotate=90] "
                       f"at ({xm:.3f},{ya/2:.3f}) {{{a}}};")
        if b and (yb-ya) > 0.28:
            out.append(f"    \\node[font=\\sffamily\\scriptsize\\bfseries,white] "
                       f"at ({xm:.3f},{(ya+yb)/2:.3f}) {{{b}}};")
        if d and (yc-yb) > 0.28:
            out.append(f"    \\node[font=\\sffamily\\scriptsize\\bfseries,white] "
                       f"at ({xm:.3f},{(yb+yc)/2:.3f}) {{{d}}};")
        out.append("")
    out.append("    \\foreach \\xi/\\yr in {" +
               ", ".join(f"{X[y]:.3f}/{'{2026*}' if y==2026 else y}" for y in YEARS) + "}{")
    out.append("      \\node[below,axgray,font=\\sffamily\\footnotesize,rotate=30,anchor=north east]")
    out.append("        at (\\xi,-0.05) {\\yr};")
    out.append("    }")
    for (lx, col, lbl) in legend_lbls:
        out.append(f"    \\fill[{col}] ({lx},2.943) rectangle ({lx+0.4},3.063);")
        out.append(f"    \\node[right,font=\\sffamily\\footnotesize] at ({lx+0.45},3.003) {{{lbl}}};")
    out.append(f"    \\node[font=\\sffamily\\footnotesize\\bfseries,axgray] at (4.25,-0.9)")
    out.append(f"      {{({caption[0]}) {caption[2]}}};")
    out.append("  \\end{scope}")
    return "\n".join(out)

def render_lines(scale, xshift):
    cum, pts = {"A":0,"E":0}, {"A":[], "E":[]}
    for y in YEARS:
        for k in ("A","E"):
            cum[k] += ann[y][k]; pts[k].append((X[y], round(cum[k]/scale*STRETCH,3)))
    out = [f"  %% ── Panel (c): Cumulative amplified vs emergent risks ──",
           f"  %%   scale 1 unit = {scale} papers; y = count/{scale} x {STRETCH} (papers.json)",
           f"  %%   cumA: " + "/".join(str(v) for v in _cumlist('A')),
           f"  %%   cumE: " + "/".join(str(v) for v in _cumlist('E')),
           f"  \\begin{{scope}}[xshift={xshift}cm, yshift=0cm]",
            "    \\draw[thick,axgray] (0,0) -- (8.5,0) node[right,axgray]{\\small Year};",
            "    \\draw[thick,axgray] (0,0) -- (0,3.40)",
            "      node[above,axgray,align=center]{\\small Cumulative\\\\\\small papers};"]
    half = max(scale//2, 1)
    ticks=[t for t in nice_ticks(scale) if t]
    out.append("    \\foreach \\y/\\lbl in {0.0/0, " +
               ", ".join(f"{t/scale*STRETCH:.3f}/{t}" for t in ticks) + "}{")
    out.append("      \\draw[axgray!50,thin] (0,\\y) -- (8.2,\\y);")
    out.append("      \\node[left,axgray,font=\\sffamily\\footnotesize] at (-0.1,\\y) {\\lbl};")
    out.append("    }")
    top=int(round(AXIS_TOP/STRETCH*scale))
    out.append(f"    \\draw[axgray!50,thin] (0,{AXIS_TOP:.3f}) -- (8.2,{AXIS_TOP:.3f});")
    out.append(f"    \\node[left,axgray,font=\\sffamily\\footnotesize] at (-0.1,{AXIS_TOP:.3f}) {{{top}}};")
    for col,key in (("riskAcol","A"),("riskEcol","E")):
        coords=" -- ".join(f"({x:.3f},{y:.3f})" for x,y in pts[key])
        out.append(f"    \\draw[{col}, very thick, rounded corners=2pt]")
        out.append(f"      {coords};")
        out.append("    \\foreach \\x/\\y in {" +
                   ", ".join(f"{x:.3f}/{y:.3f}" for x,y in pts[key]) + "}{")
        out.append(f"      \\fill[{col}] (\\x,\\y) circle (3pt); }}")
    out.append("    \\foreach \\xi/\\yr in {" +
               ", ".join(f"{X[y]:.3f}/{'{2026*}' if y==2026 else y}" for y in YEARS) + "}{")
    out.append("      \\node[below,axgray,font=\\sffamily\\footnotesize,rotate=30,anchor=north east]")
    out.append("        at (\\xi,-0.05) {\\yr};")
    out.append("    }")
    out.append("    \\draw[riskAcol,very thick] (0.2,3.173) -- (0.8,3.173);")
    out.append("    \\fill[riskAcol] (0.5,3.173) circle (3pt);")
    out.append("    \\node[right,font=\\sffamily\\footnotesize] at (0.85,3.173) {Amplified risks};")
    out.append("    \\draw[riskEcol,very thick] (0.2,2.943) -- (0.8,2.943);")
    out.append("    \\fill[riskEcol] (0.5,2.943) circle (3pt);")
    out.append("    \\node[right,font=\\sffamily\\footnotesize] at (0.85,2.943) {Emergent risks};")
    out.append("    \\node[font=\\sffamily\\footnotesize\\bfseries,axgray] at (4.25,-0.9)")
    out.append("      {(c) Cumulative: amplified vs.\\ emergent risks};")
    out.append("  \\end{scope}")
    return "\n".join(out)

def _cumlist(k):
    t=0; o=[]
    for y in YEARS: t+=ann[y][k]; o.append(t)
    return o

# ── choose scales ─────────────────────────────────────────────────────────────
max_a = max(sum(c(l,y,"panel_a") for l in (1,2,3)) for y in YEARS)
max_b = max(sum(c(l,y,"panel_b") for l in (1,2,3)) for y in YEARS)
max_c = max(_cumlist("A")[-1], _cumlist("E")[-1])
sa, sb, sc = nice_scale(max_a), nice_scale(max_b), nice_scale(max_c)
print(f"max a={max_a} b={max_b} c={max_c}  ->  scales 1u={sa}/{sb}/{sc} papers "
      f"(top ticks {int(AXIS_TOP/STRETCH*sa)}/{int(AXIS_TOP/STRETCH*sb)}/{int(AXIS_TOP/STRETCH*sc)})")

new_a = render_bars("panel_a", sa, "0",
                    ("a","RecSys+IR scope","RecSys\\,+\\,IR scope"),
                    [(0.2,"loa1col","Non-agentic (Pre-LLM + ICL)"),
                     (4.5,"loa2col","Single-agent"),(6.6,"loa3col","Multi-agent")])
new_b = render_bars("panel_b", sb, "9.5",
                    ("b","all agentic AI safety","All agentic AI safety scope"),
                    [(0.2,"loa1col","Non-agentic (Pre-LLM + ICL)"),
                     (4.5,"loa2col","Single-agent"),(6.6,"loa3col","Multi-agent")])
new_c = render_lines(sc, "19")

ap=argparse.ArgumentParser(); ap.add_argument("--apply",action="store_true")
if not ap.parse_args().apply:
    print("\n[dry-run] rendered "
          f"{len(new_a.splitlines())}/{len(new_b.splitlines())}/{len(new_c.splitlines())} lines "
          "for panels a/b/c; pass --apply to patch the .tex")
    sys.exit()

tex = TEX.read_text()
blocks = list(re.finditer(r'  %% ── Panel \((\w)\).*?\\end\{scope\}', tex, re.S))
assert len(blocks)==3, f"expected 3 panel blocks, found {len(blocks)}"
for m, new in zip(reversed(blocks), (new_c, new_b, new_a)):
    tex = tex[:m.start()] + new + tex[m.end():]
TEX.write_text(tex)
print(f"patched {TEX}")
