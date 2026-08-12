"""Shared plumbing for the m1x profile SVG variants.

Palette, typography and motion vocabulary are lifted from m1hai.ru
(tailwind.config.ts + app/globals.css) so the README reads as the same
system as the site: monochrome, terminal, halftone-dithered.
"""

import json
import os
from datetime import date

# --- palette (m1x_web/tailwind.config.ts) -----------------------------------
INK = "#000000"
SIGNAL = "#f5f5f5"
ASH = "#9a9a9a"
DUST = "#555555"
LINE = "#1a1a1a"

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

# opacity ramp per contribution level — level 0 stays a faint substrate
RAMP = [0.055, 0.26, 0.48, 0.72, 1.0]

HERE = os.path.dirname(os.path.abspath(__file__))


def _find_up(name, start, depth=4):
    d = start
    for _ in range(depth):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
        d = os.path.dirname(d)
    return None


# Paths are overridable so the same generator runs from the scratchpad and from
# the profile repo, where the workflow points them at the checkout root.
CONTRIB = os.environ.get("CONTRIB_JSON") or _find_up("contrib.json", HERE)
OUT = os.environ.get("SVG_OUT") or os.path.join(os.path.dirname(HERE), "out")


def load():
    """Read the GraphQL calendar dump into a flat day list + metrics."""
    if not CONTRIB or not os.path.exists(CONTRIB):
        raise SystemExit("contrib.json not found — set CONTRIB_JSON or run "
                         "tools/fetch_contributions.py first")
    with open(CONTRIB) as f:
        raw = json.load(f)
    cal = raw["data"]["viewer"]["contributionsCollection"]["contributionCalendar"]

    weeks = []
    for w in cal["weeks"]:
        weeks.append([
            {"date": d["date"], "n": d["contributionCount"], "wd": d["weekday"]}
            for d in w["contributionDays"]
        ])

    days = [d for w in weeks for d in w]
    counts = [d["n"] for d in days]
    active = [c for c in counts if c > 0]
    active.sort()

    # quartile thresholds over active days -> levels 1..4
    def q(p):
        if not active:
            return 1
        return active[min(len(active) - 1, int(len(active) * p))]

    t1, t2, t3 = q(0.25), q(0.5), q(0.75)

    def level(n):
        if n <= 0:
            return 0
        if n <= t1:
            return 1
        if n <= t2:
            return 2
        if n <= t3:
            return 3
        return 4

    for d in days:
        d["lv"] = level(d["n"])

    best = cur = 0
    for c in counts:
        cur = cur + 1 if c > 0 else 0
        best = max(best, cur)
    streak_now = 0
    for c in reversed(counts):
        if c > 0:
            streak_now += 1
        else:
            break

    return {
        "weeks": weeks,
        "days": days,
        "total": cal["totalContributions"],
        "peak": max(counts) if counts else 0,
        "active": len(active),
        "span": len(days),
        "streak": best,
        "streak_now": streak_now,
        "first": days[0]["date"],
        "last": days[-1]["date"],
    }


def month_ticks(weeks):
    """First week index of each month, for the axis under the grid."""
    ticks, seen = [], set()
    for i, w in enumerate(weeks):
        d = date.fromisoformat(w[0]["date"])
        key = (d.year, d.month)
        if key not in seen:
            seen.add(key)
            ticks.append((i, d.strftime("%b").upper()))
    return ticks


def defs_texture(scan=True, halftone=True, grain=False):
    """Halftone dot field + CRT scanlines — the site's texture utilities."""
    out = []
    if halftone:
        out.append(f"""
  <pattern id="halftone" width="4" height="4" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="0.6" fill="{SIGNAL}" opacity="0.18"/>
  </pattern>""")
    if scan:
        out.append(f"""
  <pattern id="scanlines" width="3" height="3" patternUnits="userSpaceOnUse">
    <rect width="3" height="1.5" y="1.5" fill="{INK}" opacity="0.5"/>
  </pattern>""")
    if grain:
        out.append("""
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7"/>
    <feColorMatrix type="saturate" values="0"/>
    <feComponentTransfer><feFuncA type="linear" slope="0.06"/></feComponentTransfer>
    <feBlend in2="SourceGraphic" mode="screen"/>
  </filter>""")
    return "".join(out)


def label(x, y, text, size=9, fill=ASH, spacing=0.22, anchor="start", weight="400", opacity=1.0):
    return (
        f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" fill="{fill}" '
        f'letter-spacing="{spacing}em" text-anchor="{anchor}" font-weight="{weight}" '
        f'opacity="{opacity}">{text}</text>'
    )


def metrics_line(m):
    return (
        f"TOTAL {m['total']}   PEAK {m['peak']}/D   STREAK {m['streak']}D   "
        f"ACTIVE {m['active']}/{m['span']}   WINDOW 53W"
    )


REDUCED = """
    @media (prefers-reduced-motion: reduce) {
      * { animation: none !important; }
    }"""


def wrap(width, height, body, css, title, desc=""):
    """Assemble a self-contained SVG. No script — GitHub strips it; all
    motion lives in CSS/SMIL inside the file itself."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"
     viewBox="0 0 {width} {height}" role="img" aria-label="{title}">
  <title>{title}</title>
  <desc>{desc}</desc>
  <defs>{defs_texture()}
  <style>
    text {{ font-family: {MONO}; }}
{css}
{REDUCED}
  </style>
  </defs>
  <rect width="{width}" height="{height}" fill="{INK}"/>
{body}
  <rect width="{width}" height="{height}" fill="url(#scanlines)" opacity="0.35" pointer-events="none"/>
</svg>
"""


def save(name, svg):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    with open(p, "w") as f:
        f.write(svg)
    return p, len(svg)
