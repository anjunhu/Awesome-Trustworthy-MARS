#!/usr/bin/env python3
"""
Reads loa1_counts.json (from classical crawl) + papers.json (curated list),
computes all updated figure numbers, then patches the TikZ figure in
cacr-tutorial/tutorial_proposal_cikm.tex in-place.

Run after run_historical_crawl.sh completes.
"""
import json, re, math
from pathlib import Path
from collections import defaultdict

REPO      = Path(__file__).parent.parent
CACHE     = Path(__file__).parent
TEX_FILE  = REPO.parent / "cacr-tutorial" / "tutorial_proposal_cikm.tex"
YEARS     = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
X_POS     = {2020: 0.925, 2021: 2.025, 2022: 3.125,
             2023: 4.225, 2024: 5.325, 2025: 6.425, 2026: 7.525}

# ── Load data ─────────────────────────────────────────────────────────────────

with open(REPO / "papers.json") as f:
    papers = json.load(f)

loa1_file = CACHE / "loa1_counts.json"
if not loa1_file.exists():
    raise SystemExit("loa1_counts.json not found — run run_historical_crawl.sh first")
with open(loa1_file) as f:
    loa1_data = json.load(f)

# ── Classify papers.json entries ──────────────────────────────────────────────

def get_year(p):
    m = re.search(r"(20\d\d)", p.get("venue", ""))
    return int(m.group(1)) if m else None

def classify_loa(p):
    sec   = p.get("section", "")
    notes = str(p.get("notes", "") or "").lower()
    title = (p.get("title", "") or "").lower()
    if sec in ("rf3_interagent", "collusion"):
        return 3
    if sec == "foundational":
        if any(k in title for k in ["multi-agent", "multi agent", "macrec", "macf", "matcha"]):
            return 3
        return 2
    if "classical" in notes:
        return 1
    return 2

RS_TITLE_KW = [
    "recommend", "retriev", "collaborative filter", "ranking", "personali",
    "user-item", "recsys", "item recommendation",
]

def is_recsys(p):
    flag = p.get("recsys")
    if flag is True:
        return True
    if flag is False:
        return False
    # recsys=None → infer from title
    title = (p.get("title", "") or "").lower()
    return any(kw in title for kw in RS_TITLE_KW)

loa2_rs  = defaultdict(int); loa3_rs  = defaultdict(int)
loa2_all = defaultdict(int); loa3_all = defaultdict(int)
annual_A = defaultdict(int); annual_E = defaultdict(int)

for p in papers:
    yr  = get_year(p)
    if not yr or yr < 2020: continue
    loa = classify_loa(p)
    rs  = is_recsys(p)
    rt  = p.get("risk_type")
    if loa == 2:
        loa2_all[yr] += 1
        if rs: loa2_rs[yr] += 1
    elif loa == 3:
        loa3_all[yr] += 1
        if rs: loa3_rs[yr] += 1
    if rt == "A": annual_A[yr] += 1
    if rt == "E": annual_E[yr] += 1

# ── LoA-1 from classical crawl ────────────────────────────────────────────────
# The classical crawler already filters to RecSys keywords, so its `relevant`
# count serves as both panel (a) and panel (b) LoA-1.

loa1 = {}
for yr in YEARS:
    entry = loa1_data["years"].get(str(yr), {})
    loa1[yr] = entry.get("relevant", 0)

# ── Cumulative A/E ────────────────────────────────────────────────────────────
cumA, cumE = 0, 0
cumA_pts = {}; cumE_pts = {}
for yr in YEARS:
    cumA += annual_A[yr]; cumE += annual_E[yr]
    cumA_pts[yr] = cumA; cumE_pts[yr] = cumE

# ── Choose scales ─────────────────────────────────────────────────────────────
# Panel (a): LoA-1+2+3 recsys, scale_a papers per tikz unit
max_a = max(loa1[yr] + loa2_rs[yr] + loa3_rs[yr] for yr in YEARS)
scale_a = max(20, math.ceil(max_a / 2.0 / 5) * 5)   # round to next 5, min 20

# Panel (b): LoA-1+2+3 all, scale_b papers per tikz unit
max_b = max(loa1[yr] + loa2_all[yr] + loa3_all[yr] for yr in YEARS)
scale_b = max(50, math.ceil(max_b / 2.0 / 50) * 50)  # round to next 50, min 50

# Panel (c): cumulative A, scale_c papers per tikz unit
max_c = max(cumA_pts.values())
scale_c = max(25, math.ceil(max_c / 2.0 / 10) * 10)  # round to next 10, min 25

print(f"scale_a=1/{scale_a}  scale_b=1/{scale_b}  scale_c=1/{scale_c}")
print(f"max_a={max_a}  max_b={max_b}  max_c={max_c}")
print()

# ── Print data table ──────────────────────────────────────────────────────────
print("Panel (a) RecSys+IR:")
print(f"  {'Year':>4}  {'L1':>4}  {'L2':>4}  {'L3':>4}  {'total':>5}  {'ya':>6}  {'yb':>6}  {'yc':>6}")
for yr in YEARS:
    a, b, c = loa1[yr], loa2_rs[yr], loa3_rs[yr]
    ya = a / scale_a; yb = (a+b) / scale_a; yc = (a+b+c) / scale_a
    print(f"  {yr:>4}  {a:>4}  {b:>4}  {c:>4}  {a+b+c:>5}  {ya:>6.3f}  {yb:>6.3f}  {yc:>6.3f}")
print()

print("Panel (b) All agentic AI safety:")
print(f"  {'Year':>4}  {'L1':>4}  {'L2':>4}  {'L3':>4}  {'total':>5}  {'ya':>6}  {'yb':>6}  {'yc':>6}")
for yr in YEARS:
    a, b, c = loa1[yr], loa2_all[yr], loa3_all[yr]
    ya = a / scale_b; yb = (a+b) / scale_b; yc = (a+b+c) / scale_b
    print(f"  {yr:>4}  {a:>4}  {b:>4}  {c:>4}  {a+b+c:>5}  {ya:>6.3f}  {yb:>6.3f}  {yc:>6.3f}")
print()

print("Panel (c) Cumulative A/E:")
print(f"  {'Year':>4}  {'cumA':>5}  {'cumE':>5}  {'yA':>6}  {'yE':>6}")
for yr in YEARS:
    cA = cumA_pts[yr]; cE = cumE_pts[yr]
    print(f"  {yr:>4}  {cA:>5}  {cE:>5}  {cA/scale_c:>6.3f}  {cE/scale_c:>6.3f}")
print()

# ── Generate new TikZ for the three active panels ─────────────────────────────

def fmt(v):
    return f"{v:.3f}"

def bar_label(count, rotate=False):
    if rotate:
        return f"\\node[font=\\sffamily\\tiny,axgray!80!black,rotate=90]"
    return f"\\node[font=\\sffamily\\tiny,axgray!80!black,anchor=south]"

# x positions: bars are 0.85 wide, centred at X_POS
BAR_L = {yr: X_POS[yr] - 0.425 for yr in YEARS}
BAR_R = {yr: X_POS[yr] + 0.425 for yr in YEARS}

def panel_a_tikz():
    lines = []
    sc = scale_a
    axis_max = math.ceil(max(loa1[yr]+loa2_rs[yr]+loa3_rs[yr] for yr in YEARS) / sc / 0.5) * 0.5
    # axis ticks every sc papers
    tick_step = sc // 2  # every half scale unit
    tick_vals = list(range(0, int(axis_max * sc) + tick_step, tick_step))

    lines.append(f"  %% ── Panel (a): RecSys+IR, linear ──")
    lines.append(f"  %%   scale: 1 unit = {sc} papers")
    lines.append(f"  %%   Year  LoA-1  LoA-2  LoA-3   ya=a/{sc}  yb=(a+b)/{sc}  yc=(a+b+c)/{sc}")
    for yr in YEARS:
        a, b, c = loa1[yr], loa2_rs[yr], loa3_rs[yr]
        ya = a/sc; yb=(a+b)/sc; yc=(a+b+c)/sc
        lines.append(f"  %%   {yr}   {a:4d}   {b:4d}   {c:4d}   {ya:.3f}   {yb:.3f}   {yc:.3f}")
    lines.append(f"  \\begin{{scope}}[xshift=0cm, yshift=0cm]")
    lines.append(f"    \\draw[thick,axgray] (0,0) -- (8.5,0) node[right,axgray]{{\\footnotesize Year}};")
    lines.append(f"    \\draw[thick,axgray] (0,0) -- (0,2.4)")
    lines.append(f"      node[above,axgray,align=center]{{\\footnotesize arXiv~count}};")
    tick_str = ", ".join(f"{v/sc:.1f}/{v}" for v in tick_vals if v/sc <= 2.1)
    lines.append(f"    \\foreach \\y/\\lbl in {{{tick_str}}}{{")
    lines.append(f"      \\draw[axgray!50,thin] (0,\\y) -- (8.2,\\y);")
    lines.append(f"      \\node[left,axgray,font=\\sffamily\\scriptsize] at (-0.1,\\y) {{\\lbl}};")
    lines.append(f"    }}")
    lines.append(f"")

    for yr in YEARS:
        a, b, c = loa1[yr], loa2_rs[yr], loa3_rs[yr]
        ya = a/sc; yb=(a+b)/sc; yc=(a+b+c)/sc
        xl, xr, xm = BAR_L[yr], BAR_R[yr], X_POS[yr]
        lines.append(f"    %% {yr}: LoA-1={a} LoA-2={b} LoA-3={c}")
        if a > 0:
            lines.append(f"    \\fill[loa1col] ({xl:.3f},0) rectangle ({xr:.3f},{ya:.3f});")
        if b > 0:
            lines.append(f"    \\fill[loa2col] ({xl:.3f},{ya:.3f}) rectangle ({xr:.3f},{yb:.3f});")
        if c > 0:
            lines.append(f"    \\fill[loa3col] ({xl:.3f},{yb:.3f}) rectangle ({xr:.3f},{yc:.3f});")
        total = a + b + c
        top_y = yc if c > 0 else (yb if b > 0 else ya)
        rot = total >= sc  # rotate label if bar is tall
        if total == 0:
            pass
        elif b == 0 and c == 0:
            style = "rotate=90" if rot else "anchor=south"
            lines.append(f"    \\node[font=\\sffamily\\tiny,axgray!80!black,{style}] at ({xm:.3f},{ya/2:.3f}) {{{a}}};")
        else:
            label_parts = []
            if a > 0:
                style = "rotate=90" if a/sc > 0.3 else "anchor=south"
                label_parts.append(f"    \\node[font=\\sffamily\\tiny,axgray!80!black,{style}] at ({xm:.3f},{ya/2:.3f}) {{{a}}};")
            if b > 0:
                col = "white" if b/sc > 0.15 else "loa2col"
                label_parts.append(f"    \\node[font=\\sffamily\\tiny\\bfseries,{col}] at ({xm:.3f},{(ya+yb)/2:.3f}) {{{b}}};")
            if c > 0:
                col = "white" if c/sc > 0.15 else "loa3col"
                label_parts.append(f"    \\node[font=\\sffamily\\tiny\\bfseries,{col}] at ({xm:.3f},{(yb+yc)/2:.3f}) {{{c}}};")
            lines.extend(label_parts)
        lines.append(f"")

    yr_str = ", ".join(f"{X_POS[yr]:.3f}/{yr if yr != 2026 else '{2026*}'}" for yr in YEARS)
    lines.append(f"    \\foreach \\xi/\\yr in {{{yr_str}}}{{")
    lines.append(f"      \\node[below,axgray,font=\\sffamily\\scriptsize,rotate=30,anchor=north east]")
    lines.append(f"        at (\\xi,-0.05) {{\\yr}};")
    lines.append(f"    }}")
    lines.append(f"    %% legend")
    lines.append(f"    \\fill[loa1col] (4.8,2.18) rectangle (5.2,2.30);")
    lines.append(f"    \\node[right,font=\\sffamily\\scriptsize] at (5.25,2.24) {{LoA-1}};")
    lines.append(f"    \\fill[loa2col] (6.1,2.18) rectangle (6.5,2.30);")
    lines.append(f"    \\node[right,font=\\sffamily\\scriptsize] at (6.55,2.24) {{LoA-2}};")
    lines.append(f"    \\fill[loa3col] (7.2,2.18) rectangle (7.6,2.30);")
    lines.append(f"    \\node[right,font=\\sffamily\\scriptsize] at (7.65,2.24) {{LoA-3}};")
    lines.append(f"    \\node[font=\\sffamily\\footnotesize\\bfseries,axgray] at (4.25,-0.9)")
    lines.append(f"      {{(a) RecSys\\,+\\,IR scope (linear)}};")
    lines.append(f"  \\end{{scope}}")
    return "\n".join(lines)

def panel_b_tikz():
    lines = []
    sc = scale_b
    lines.append(f"  %% ── Panel (b): All agentic AI safety, linear ──")
    lines.append(f"  %%   scale: 1 unit = {sc} papers")
    lines.append(f"  %%   Year  LoA-1  LoA-2  LoA-3   ya=a/{sc}  yb=(a+b)/{sc}  yc=(a+b+c)/{sc}")
    for yr in YEARS:
        a, b, c = loa1[yr], loa2_all[yr], loa3_all[yr]
        ya=a/sc; yb=(a+b)/sc; yc=(a+b+c)/sc
        lines.append(f"  %%   {yr}   {a:4d}   {b:4d}   {c:4d}   {ya:.3f}   {yb:.3f}   {yc:.3f}")
    lines.append(f"  \\begin{{scope}}[xshift=9.5cm, yshift=0cm]")
    lines.append(f"    \\draw[thick,axgray] (0,0) -- (8.5,0) node[right,axgray]{{\\footnotesize Year}};")
    lines.append(f"    \\draw[thick,axgray] (0,0) -- (0,2.3)")
    lines.append(f"      node[above,axgray,align=center]{{\\footnotesize arXiv~count}};")
    # ticks at 0, sc/2, sc, 3sc/2, 2sc
    tick_vals = [0, sc//2, sc, sc+sc//2, 2*sc]
    tick_str = ", ".join(f"{v/sc:.1f}/{v}" for v in tick_vals if v/sc <= 2.1)
    lines.append(f"    \\foreach \\y/\\lbl in {{{tick_str}}}{{")
    lines.append(f"      \\draw[axgray!50,thin] (0,\\y) -- (8.2,\\y);")
    lines.append(f"      \\node[left,axgray,font=\\sffamily\\scriptsize] at (-0.1,\\y) {{\\lbl}};")
    lines.append(f"    }}")
    lines.append(f"")

    for yr in YEARS:
        a, b, c = loa1[yr], loa2_all[yr], loa3_all[yr]
        ya=a/sc; yb=(a+b)/sc; yc=(a+b+c)/sc
        xl, xr, xm = BAR_L[yr], BAR_R[yr], X_POS[yr]
        lines.append(f"    %% {yr}: LoA-1={a} LoA-2={b} LoA-3={c}")
        if a > 0:
            lines.append(f"    \\fill[loa1col] ({xl:.3f},0) rectangle ({xr:.3f},{ya:.3f});")
        if b > 0:
            lines.append(f"    \\fill[loa2col] ({xl:.3f},{ya:.3f}) rectangle ({xr:.3f},{yb:.3f});")
        if c > 0:
            lines.append(f"    \\fill[loa3col] ({xl:.3f},{yb:.3f}) rectangle ({xr:.3f},{yc:.3f});")
        if a == 0 and b == 0 and c == 0:
            pass
        elif b == 0 and c == 0:
            rot = a/sc > 0.3
            style = "rotate=90" if rot else "anchor=south"
            lines.append(f"    \\node[font=\\sffamily\\tiny,axgray!80!black,{style}] at ({xm:.3f},{ya/2:.3f}) {{{a}}};")
        else:
            if a > 0:
                rot = a/sc > 0.3
                style = "rotate=90" if rot else "anchor=south"
                lines.append(f"    \\node[font=\\sffamily\\tiny,axgray!80!black,{style}] at ({xm:.3f},{ya/2:.3f}) {{{a}}};")
            if b > 0:
                col = "white" if b/sc > 0.1 else "loa2col"
                lines.append(f"    \\node[font=\\sffamily\\tiny\\bfseries,{col}] at ({xm:.3f},{(ya+yb)/2:.3f}) {{{b}}};")
            if c > 0:
                col = "white" if c/sc > 0.1 else "loa3col"
                lines.append(f"    \\node[font=\\sffamily\\tiny\\bfseries,{col}] at ({xm:.3f},{(yb+yc)/2:.3f}) {{{c}}};")
        lines.append(f"")

    yr_str = ", ".join(f"{X_POS[yr]:.3f}/{yr if yr != 2026 else '{2026*}'}" for yr in YEARS)
    lines.append(f"    \\foreach \\xi/\\yr in {{{yr_str}}}{{")
    lines.append(f"      \\node[below,axgray,font=\\sffamily\\scriptsize,rotate=30,anchor=north east]")
    lines.append(f"        at (\\xi,-0.05) {{\\yr}};")
    lines.append(f"    }}")
    lines.append(f"    \\node[font=\\sffamily\\footnotesize\\bfseries,axgray] at (4.25,-0.9)")
    lines.append(f"      {{(b) All agentic AI safety (linear)}};")
    lines.append(f"  \\end{{scope}}")
    return "\n".join(lines)

def panel_c_tikz():
    sc = scale_c
    lines = []
    lines.append(f"  %% ── Panel (c): Cumulative amplified vs emergent risks ──")
    lines.append(f"  %%   scale: 1 unit = {sc} papers")
    lines.append(f"  %%   cumA: " + "/".join(str(cumA_pts[yr]) for yr in YEARS))
    lines.append(f"  %%   cumE: " + "/".join(str(cumE_pts[yr]) for yr in YEARS))
    lines.append(f"  \\begin{{scope}}[xshift=19cm, yshift=0cm]")
    lines.append(f"    \\draw[thick,axgray] (0,0) -- (8.5,0) node[right,axgray]{{\\footnotesize Year}};")
    lines.append(f"    \\draw[thick,axgray] (0,0) -- (0,2.6)")
    lines.append(f"      node[above,axgray,align=center]{{\\footnotesize Cumulative\\\\\\footnotesize papers}};")
    # axis ticks
    tick_vals = [0, sc, 2*sc]
    tick_str = ", ".join(f"{v/sc:.1f}/{v}" for v in tick_vals)
    lines.append(f"    \\foreach \\y/\\lbl in {{{tick_str}}}{{")
    lines.append(f"      \\draw[axgray!50,thin] (0,\\y) -- (8.2,\\y);")
    lines.append(f"      \\node[left,axgray,font=\\sffamily\\scriptsize] at (-0.1,\\y) {{\\lbl}};")
    lines.append(f"    }}")
    lines.append(f"    \\foreach \\y in {{0.6, 1.4, 2.4}}{{ \\draw[axgray!20,very thin] (0,\\y) -- (8.2,\\y); }}")

    # amplified line
    pts_A = " -- ".join(f"({X_POS[yr]:.3f},{cumA_pts[yr]/sc:.3f})" for yr in YEARS)
    lines.append(f"    \\draw[riskAcol, very thick, rounded corners=2pt]")
    lines.append(f"      {pts_A};")
    dot_A = ", ".join(f"{X_POS[yr]:.3f}/{cumA_pts[yr]/sc:.3f}" for yr in YEARS)
    lines.append(f"    \\foreach \\x/\\y in {{{dot_A}}}{{")
    lines.append(f"      \\fill[riskAcol] (\\x,\\y) circle (3pt); }}")

    # emergent line
    pts_E = " -- ".join(f"({X_POS[yr]:.3f},{cumE_pts[yr]/sc:.3f})" for yr in YEARS)
    lines.append(f"    \\draw[riskEcol, very thick, rounded corners=2pt]")
    lines.append(f"      {pts_E};")
    dot_E = ", ".join(f"{X_POS[yr]:.3f}/{cumE_pts[yr]/sc:.3f}" for yr in YEARS)
    lines.append(f"    \\foreach \\x/\\y in {{{dot_E}}}{{")
    lines.append(f"      \\fill[riskEcol] (\\x,\\y) circle (3pt); }}")

    yr_str = ", ".join(f"{X_POS[yr]:.3f}/{yr if yr != 2026 else '{2026*}'}" for yr in YEARS)
    lines.append(f"    \\foreach \\xi/\\yr in {{{yr_str}}}{{")
    lines.append(f"      \\node[below,axgray,font=\\sffamily\\scriptsize,rotate=30,anchor=north east]")
    lines.append(f"        at (\\xi,-0.05) {{\\yr}};")
    lines.append(f"    }}")

    # surge annotation (2025 is where emergent spikes)
    lines.append(f"    \\draw[->,axgray!70,thin] (4.7,{cumE_pts[2024]/sc + 0.3:.3f}) -- (6.2,{cumE_pts[2025]/sc - 0.15:.3f});")
    lines.append(f"    \\node[font=\\sffamily\\scriptsize\\itshape,axgray,align=center] at (4.1,{cumE_pts[2024]/sc + 0.25:.3f})")
    lines.append(f"      {{emergent risks\\\\\\emph{{surge}} (2025)}};")

    # legend
    lines.append(f"    \\draw[riskAcol,very thick] (0.2,2.35) -- (0.8,2.35);")
    lines.append(f"    \\fill[riskAcol] (0.5,2.35) circle (3pt);")
    lines.append(f"    \\node[right,font=\\sffamily\\scriptsize] at (0.85,2.35) {{Amplified risks}};")
    lines.append(f"    \\draw[riskEcol,very thick] (0.2,2.10) -- (0.8,2.10);")
    lines.append(f"    \\fill[riskEcol] (0.5,2.10) circle (3pt);")
    lines.append(f"    \\node[right,font=\\sffamily\\scriptsize] at (0.85,2.10) {{Emergent risks}};")
    lines.append(f"    \\node[font=\\sffamily\\footnotesize\\bfseries,axgray] at (4.25,-0.9)")
    lines.append(f"      {{(c) Cumulative: amplified vs.\\ emergent risks}};")
    lines.append(f"  \\end{{scope}}")
    return "\n".join(lines)

# ── Patch the tex file ────────────────────────────────────────────────────────

tex = TEX_FILE.read_text()

# Locate the three active scope blocks and replace them.
# Panel (a): begins with \begin{scope}[xshift=0cm, yshift=0cm]
# Panel (b): begins with \begin{scope}[xshift=9.5cm, yshift=0cm]
# Panel (c): begins with \begin{scope}[xshift=19cm, yshift=0cm]

def replace_scope(tex, xshift_str, new_content):
    start_tag = f"\\begin{{scope}}[xshift={xshift_str}"
    end_tag   = "\\end{scope}"
    i = tex.find(start_tag)
    if i == -1:
        raise ValueError(f"Could not find scope xshift={xshift_str}")
    j = tex.find(end_tag, i)
    if j == -1:
        raise ValueError(f"Could not find \\end{{scope}} after xshift={xshift_str}")
    j += len(end_tag)
    return tex[:i] + new_content + tex[j:]

tex = replace_scope(tex, "0cm, yshift=0cm]",   panel_a_tikz())
tex = replace_scope(tex, "9.5cm, yshift=0cm]", panel_b_tikz())
tex = replace_scope(tex, "19cm, yshift=0cm]",  panel_c_tikz())

TEX_FILE.write_text(tex)
print(f"\nPatched: {TEX_FILE}")
print("Done. Verify with: pdflatex tutorial_proposal_cikm.tex")
