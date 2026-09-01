#!/usr/bin/env python3
"""
Generate SVG tag/pill assets for the reading-list tables.

Why local SVG rather than shields.io: no external requests, no rate limits or
camo-cache staleness, renders offline, and the palette stays locked to the
survey figure. Colours are solid with white text so the pills read correctly
in both GitHub light and dark themes.

Run after changing the tag vocabulary:
    python3 assets/make_badges.py
"""
import json, re
from pathlib import Path

ASSETS = Path(__file__).parent / "badges"
REPO   = Path(__file__).parent.parent

# palette shared with Figure 1 of the tutorial/survey
PALETTE = {
    "amplified":    "#7B5EA7",   # riskAcol
    "emergent":     "#2D9E6B",   # riskEcol
    "component":    "#A8C8E8",   # loa1col  (light -> dark text)
    "interaction":  "#2D6A9F",   # loa2col
    "composition":  "#E07B39",   # loa3col
    "drift":        "#5F7484",
    "misalignment": "#A9772A",
    "compromise":   "#C0392B",
    "_topic":       "#EDF0F2",   # neutral chip, dark text
    "_domain":      "#DCE6EF",
}


def _luminance(hexcolour: str) -> float:
    c = [int(hexcolour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def _contrast(a: str, b: str) -> float:
    l1, l2 = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


INK, PAPER = "#24292F", "#FFFFFF"


def ensure_contrast(fill: str, target: float = 4.5) -> str:
    """Darken a fill just enough that one ink colour clears `target`.

    Most fills come straight from the Figure 1 palette, but a few mid-tone
    hues (the green and the amber) cannot reach 4.5:1 against either black or
    white at 11px. We step the fill toward black in 2% increments, which keeps
    the hue recognisable while making the label readable.
    """
    r, g, b = (int(fill[i:i + 2], 16) for i in (1, 3, 5))
    for _ in range(50):
        cur = f"#{r:02X}{g:02X}{b:02X}"
        if max(_contrast(cur, INK), _contrast(cur, PAPER)) >= target:
            return cur
        r, g, b = (int(v * 0.98) for v in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


def pick_text(fill: str) -> str:
    """Whichever of dark/white ink contrasts better against the fill.

    Several fills are taken verbatim from the Figure 1 palette, so the hue is
    fixed; the text colour is what we vary to keep every pill legible.
    """
    return INK if _contrast(fill, INK) >= _contrast(fill, PAPER) else PAPER


# average advance widths at font-size 11 for a system sans stack
_NARROW = set("iljtfrI.,;:'!|()[]{}-")
_WIDE   = set("mwMW@")
def text_width(s: str) -> float:
    w = 0.0
    for ch in s:
        w += 3.4 if ch in _NARROW else 8.6 if ch in _WIDE else 6.35
    return w

def badge(label: str, fill: str) -> str:
    pad = 8
    w = round(text_width(label) + 2 * pad, 1)
    h, r = 18, 9
    fg = pick_text(fill)
    # presentation attributes only: GitHub strips <style> from sanitised SVG
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
        f'<title>{label}</title>'
        f'<rect x="0" y="0" width="{w}" height="{h}" rx="{r}" ry="{r}" fill="{fill}"/>'
        f'<text x="{w/2:.1f}" y="12.8" fill="{fg}" text-anchor="middle" '
        f'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" '
        f'font-size="11" font-weight="500">{label}</text>'
        f'</svg>\n'
    )

def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def main():
    papers = json.loads((REPO / "papers.json").read_text())

    # The closed vocabulary is always emitted, even when no paper currently uses
    # a value: otherwise the first paper tagged `scope: interaction` wouldpoint to
    # a badge that was never generated and render as a broken image.
    wanted = {"amplified", "emergent",
              "component", "interaction", "composition",
              "drift", "misalignment", "compromise"}
    for p in papers:
        for t in p.get("tags") or []:
            if ":" in t:
                prefix, val = t.split(":", 1)
                if prefix in ("topic", "topo", "domain"):
                    wanted.add(val)

    ASSETS.mkdir(parents=True, exist_ok=True)
    existing = {f.name for f in ASSETS.glob("*.svg")}
    written = set()
    for label in sorted(wanted):
        fill = ensure_contrast(PALETTE.get(label, PALETTE["_topic"]))
        name = f"{slug(label)}.svg"
        (ASSETS / name).write_text(badge(label, fill))
        written.add(name)

    for stale in sorted(existing - written):
        (ASSETS / stale).unlink()
        print(f"  removed stale badge {stale}")
    print(f"{len(written)} badges written to {ASSETS.relative_to(REPO)}/")

if __name__ == "__main__":
    main()
