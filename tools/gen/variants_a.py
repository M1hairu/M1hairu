"""Variants A: waterfall, lensing, halftone, oscilloscope, crt."""

import math
from common import (INK, SIGNAL, ASH, DUST, LINE, RAMP, MONO, load, month_ticks,
                    label, metrics_line, wrap, save)

W = 920
PAD = 38
CELL, GAP = 13, 3
STEP = CELL + GAP
GRID_W = 53 * STEP - GAP          # 845
GX = (W - GRID_W) // 2
GY = 60
GRID_H = 7 * STEP - GAP           # 109


def _header(m, left, right):
    return (
        label(GX, 30, left, size=10, fill=SIGNAL, spacing=0.18) +
        label(GX + GRID_W, 30, right, size=8.5, fill=DUST, spacing=0.2, anchor="end") +
        f'<line x1="{GX}" y1="40" x2="{GX + GRID_W}" y2="40" stroke="{LINE}" stroke-width="1"/>'
    )


def _months(weeks, y):
    out = []
    for i, name in month_ticks(weeks):
        x = GX + i * STEP
        if x > GX + GRID_W - 20:
            continue
        out.append(label(x, y, name, size=7, fill=DUST, spacing=0.25))
    return "".join(out)


def _footer(m, y, extra=""):
    dot = (f'<rect x="{GX}" y="{y - 7}" width="6" height="8" fill="{SIGNAL}" class="blink"/>')
    return (
        dot +
        label(GX + 13, y, metrics_line(m), size=8.5, fill=ASH, spacing=0.22) +
        (label(GX + GRID_W, y, extra, size=8.5, fill=DUST, spacing=0.22, anchor="end") if extra else "")
    )


BLINK_CSS = """
    .blink { animation: blink 1.1s steps(1) infinite; }
    @keyframes blink { 0%,49% { opacity: 1 } 50%,100% { opacity: 0 } }"""


# ---------------------------------------------------------------- 01 waterfall
def waterfall(m):
    """SDR waterfall: a scan beam sweeps the window, cells flare under it."""
    H, dur = 224, 8.0
    body = [_header(m, "~/ scan ./contributions --waterfall", f"{m['first']} → {m['last']}")]

    # substrate: every cell at its resting opacity
    base = []
    for ci, week in enumerate(m["weeks"]):
        for d in week:
            x, y = GX + ci * STEP, GY + d["wd"] * STEP
            base.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" fill="{SIGNAL}" '
                f'opacity="{RAMP[d["lv"]]:.3f}"/>'
            )
    body.append(f'<g>{"".join(base)}</g>')

    # flare layer: one animated group per column, delayed across the sweep
    for ci, week in enumerate(m["weeks"]):
        cells = [
            f'<rect x="{GX + ci * STEP}" y="{GY + d["wd"] * STEP}" width="{CELL}" height="{CELL}" '
            f'fill="{SIGNAL}" fill-opacity="{min(1.0, RAMP[d["lv"]] + 0.25):.3f}"/>'
            for d in week if d["lv"] > 0
        ]
        if not cells:
            continue
        delay = (ci / 53) * dur
        body.append(f'<g class="col" style="animation-delay:{delay:.2f}s">{"".join(cells)}</g>')

    # the beam itself
    body.append(f"""
  <g class="beam">
    <rect x="{GX - 1}" y="{GY - 8}" width="2" height="{GRID_H + 16}" fill="{SIGNAL}" opacity="0.85"/>
    <rect x="{GX - 26}" y="{GY - 8}" width="26" height="{GRID_H + 16}" fill="url(#trail)"/>
  </g>""")

    body.append(_months(m["weeks"], GY + GRID_H + 16))
    body.append(_footer(m, 200, "SIG ACTIVE"))

    grad = f"""
  <linearGradient id="trail" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{SIGNAL}" stop-opacity="0"/>
    <stop offset="1" stop-color="{SIGNAL}" stop-opacity="0.16"/>
  </linearGradient>"""
    body.insert(0, f"<defs>{grad}</defs>")

    css = BLINK_CSS + f"""
    .col {{ opacity: 0; animation: flare {dur}s linear infinite; }}
    @keyframes flare {{
      0%   {{ opacity: 0 }}
      1.5% {{ opacity: 1 }}
      9%   {{ opacity: 0 }}
      100% {{ opacity: 0 }}
    }}
    .beam {{ animation: sweep {dur}s linear infinite; }}
    @keyframes sweep {{
      from {{ transform: translateX(0) }}
      to   {{ transform: translateX({GRID_W}px) }}
    }}"""
    return wrap(W, H, "\n".join(body), css,
                "contribution waterfall — a scan beam sweeping 53 weeks of signal")


# ------------------------------------------------------------------ 02 lensing
def lensing(m):
    """Polar heatmap: 53 weeks wrap the horizon, 7 weekdays stack as orbits.
    A radar sweep runs the year and lights each sector as it passes."""
    H, dur = 300, 12.0
    cx, cy = 168.0, 154.0
    r0, dr = 42.0, 10.5                    # inner radius, ring pitch
    body = [_header(m, "~/ orbit ./contributions --polar", f"{m['total']} QUANTA")]

    seg = (2 * math.pi) / 53
    cells, flare = [], {}
    for ci, week in enumerate(m["weeks"]):
        col = []
        for d in week:
            a0 = -math.pi / 2 + ci * seg
            a1 = a0 + seg * 0.82
            ri, ro = r0 + d["wd"] * dr, r0 + d["wd"] * dr + dr * 0.82
            p = _arc(cx, cy, ri, ro, a0, a1)
            cells.append(f'<path d="{p}" fill="{SIGNAL}" opacity="{RAMP[d["lv"]]:.3f}"/>')
            if d["lv"] > 0:
                col.append(f'<path d="{p}" fill="{SIGNAL}" '
                           f'fill-opacity="{min(1.0, RAMP[d["lv"]] + 0.25):.3f}"/>')
        if col:
            flare[ci] = "".join(col)

    body.append(f'<g>{"".join(cells)}</g>')
    for ci, cells_s in flare.items():
        body.append(f'<g class="col" style="animation-delay:{(ci / 53) * dur:.2f}s">{cells_s}</g>')

    # horizon, photon ring, sweep arm
    outer = r0 + 7 * dr + 6
    body.append(f"""
  <circle cx="{cx}" cy="{cy}" r="{r0 - 6}" fill="{INK}"/>
  <circle cx="{cx}" cy="{cy}" r="{r0 - 4}" fill="none" stroke="{SIGNAL}" stroke-width="1"
          opacity="0.5" class="ring"/>
  <circle cx="{cx}" cy="{cy}" r="{outer}" fill="none" stroke="{LINE}" stroke-width="1"/>
  <g class="sweep" style="transform-origin:{cx}px {cy}px">
    <line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - outer}" stroke="{SIGNAL}" stroke-width="1"
          opacity="0.7"/>
  </g>""")

    # right-hand instrument panel
    px = 400
    rows = [
        ("TOTAL", f"{m['total']}"),
        ("PEAK", f"{m['peak']}/DAY"),
        ("STREAK", f"{m['streak']}D  (NOW {m['streak_now']}D)"),
        ("ACTIVE", f"{m['active']}/{m['span']} DAYS"),
        ("WINDOW", f"{m['first']} → {m['last']}"),
    ]
    body.append(f'<line x1="{px - 26}" y1="62" x2="{px - 26}" y2="252" stroke="{LINE}"/>')
    for i, (k, v) in enumerate(rows):
        y = 84 + i * 26
        body.append(label(px, y, k, size=8.5, fill=DUST, spacing=0.3))
        body.append(label(px + 96, y, v, size=11, fill=SIGNAL, spacing=0.14))
        body.append(f'<line x1="{px}" y1="{y + 8}" x2="{W - PAD}" y2="{y + 8}" '
                    f'stroke="{LINE}" stroke-width="1"/>')

    # weekday ring legend
    body.append(label(px, 232, "RING 0 = MON   ·   RING 6 = SUN   ·   SECTOR = WEEK",
                      size=7.5, fill=DUST, spacing=0.22))

    body.append(_footer(m, 274, "EVENT HORIZON STABLE"))

    css = BLINK_CSS + f"""
    .col {{ opacity: 0; animation: flare {dur}s linear infinite; }}
    @keyframes flare {{
      0% {{ opacity: 0 }} 1.2% {{ opacity: 1 }} 8% {{ opacity: 0 }} 100% {{ opacity: 0 }}
    }}
    .sweep {{ animation: rot {dur}s linear infinite; }}
    @keyframes rot {{ from {{ transform: rotate(0deg) }} to {{ transform: rotate(360deg) }} }}
    .ring {{ animation: pulse 4s ease-in-out infinite; }}
    @keyframes pulse {{ 0%,100% {{ opacity: .3 }} 50% {{ opacity: .9 }} }}"""
    return wrap(W, H, "\n".join(body), css,
                "polar contribution heatmap orbiting an event horizon")


def _arc(cx, cy, ri, ro, a0, a1):
    """Annular sector path."""
    x0i, y0i = cx + ri * math.cos(a0), cy + ri * math.sin(a0)
    x1i, y1i = cx + ri * math.cos(a1), cy + ri * math.sin(a1)
    x0o, y0o = cx + ro * math.cos(a0), cy + ro * math.sin(a0)
    x1o, y1o = cx + ro * math.cos(a1), cy + ro * math.sin(a1)
    return (f"M{x0i:.2f},{y0i:.2f} A{ri:.2f},{ri:.2f} 0 0 1 {x1i:.2f},{y1i:.2f} "
            f"L{x1o:.2f},{y1o:.2f} A{ro:.2f},{ro:.2f} 0 0 0 {x0o:.2f},{y0o:.2f} Z")


# ----------------------------------------------------------------- 03 halftone
def halftone(m):
    """Dot field: radius carries the value, a wave breathes through it."""
    H, dur = 224, 7.0
    body = [_header(m, "~/ dither ./contributions --bayer", f"HALFTONE · {m['active']} ACTIVE DAYS")]

    base, pulse = [], {}
    for ci, week in enumerate(m["weeks"]):
        col = []
        for d in week:
            cx = GX + ci * STEP + CELL / 2
            cy = GY + d["wd"] * STEP + CELL / 2
            r = 0.9 + d["lv"] * 1.35
            base.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.2f}" fill="{SIGNAL}" '
                        f'opacity="{max(0.12, RAMP[d["lv"]]):.3f}"/>')
            if d["lv"] > 0:
                col.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 1.9:.2f}" fill="{SIGNAL}" '
                           f'fill-opacity="{RAMP[d["lv"]] * 0.5:.3f}"/>')
        if col:
            pulse[ci] = "".join(col)

    body.append(f'<g>{"".join(base)}</g>')
    for ci, cells in pulse.items():
        body.append(f'<g class="col" style="animation-delay:{(ci / 53) * dur:.2f}s">{cells}</g>')

    body.append(_months(m["weeks"], GY + GRID_H + 16))
    body.append(_footer(m, 200, "DITHER 4×4"))

    css = BLINK_CSS + f"""
    .col {{ opacity: 0; animation: bloom {dur}s ease-out infinite; }}
    @keyframes bloom {{
      0%  {{ opacity: 0 }}
      3%  {{ opacity: 1 }}
      14% {{ opacity: 0 }}
      100% {{ opacity: 0 }}
    }}"""
    return wrap(W, H, "\n".join(body), css,
                "halftone dot field breathing through the contribution window")


# ------------------------------------------------------------- 04 oscilloscope
def oscilloscope(m):
    """Daily signal as a trace, drawn by a running beam with phosphor decay."""
    H, dur = 240, 9.0
    top, bot = 58, 178
    days = m["days"]
    n = len(days)
    peak = max(1, m["peak"])
    sx = GRID_W / (n - 1)

    pts = []
    for i, d in enumerate(days):
        amp = (d["n"] / peak) ** 0.62
        x = GX + i * sx
        y = bot - amp * (bot - top)
        pts.append(f"{x:.1f},{y:.1f}")
    path = "M" + " L".join(pts)

    body = [_header(m, "~/ probe ./contributions --trace daily",
                    f"V/DIV {peak / 4:.0f}   T/DIV 1W")]

    # graticule
    grid = []
    for i in range(1, 6):
        y = top + (bot - top) * i / 6
        grid.append(f'<line x1="{GX}" y1="{y:.0f}" x2="{GX + GRID_W}" y2="{y:.0f}" '
                    f'stroke="{LINE}" stroke-width="1"/>')
    for i in range(1, 12):
        x = GX + GRID_W * i / 12
        grid.append(f'<line x1="{x:.0f}" y1="{top}" x2="{x:.0f}" y2="{bot}" '
                    f'stroke="{LINE}" stroke-width="1"/>')
    grid.append(f'<line x1="{GX}" y1="{bot}" x2="{GX + GRID_W}" y2="{bot}" '
                f'stroke="{DUST}" stroke-width="1"/>')
    body.append("".join(grid))

    body.append(f"""
  <path d="{path}" fill="none" stroke="{SIGNAL}" stroke-width="2.2" opacity="0.12"
        filter="url(#glow)"/>
  <path d="{path}" fill="none" stroke="{SIGNAL}" stroke-width="1.4" class="trace"
        pathLength="1000"/>
  <circle r="2.6" fill="{SIGNAL}" class="dot">
    <animateMotion dur="{dur}s" repeatCount="indefinite" path="{path}"/>
  </circle>""")

    body.append(_months(m["weeks"], bot + 20))
    body.append(_footer(m, 214, "TRIGGER AUTO"))

    defs = f"""<defs>
  <filter id="glow"><feGaussianBlur stdDeviation="1.8"/></filter>
</defs>"""
    body.insert(0, defs)

    css = BLINK_CSS + f"""
    .trace {{
      stroke-dasharray: 1000; stroke-dashoffset: 1000;
      animation: draw {dur}s linear infinite;
    }}
    @keyframes draw {{
      0%   {{ stroke-dashoffset: 1000 }}
      45%  {{ stroke-dashoffset: 0 }}
      100% {{ stroke-dashoffset: 0 }}
    }}
    .dot {{ animation: dotfade {dur}s linear infinite; }}
    @keyframes dotfade {{ 0%,45% {{ opacity: 1 }} 47%,100% {{ opacity: 0 }} }}"""
    return wrap(W, H, "\n".join(body), css,
                "daily contribution trace on an oscilloscope")


# ---------------------------------------------------------------------- 05 crt
def crt(m):
    """A CRT powering on: rows sweep in one at a time, then settle and flicker."""
    H, dur = 224, 6.5
    body = [_header(m, "~/ cat ./contributions > /dev/crt0", "PHOSPHOR P4")]

    rows = ["MON", "", "WED", "", "FRI", "", "SUN"]
    for wd in range(7):
        cells = []
        for ci, week in enumerate(m["weeks"]):
            d = next((x for x in week if x["wd"] == wd), None)
            if d is None:          # trailing week is partial
                continue
            cells.append(
                f'<rect x="{GX + ci * STEP}" y="{GY + wd * STEP}" width="{CELL}" height="{CELL}" '
                f'fill="{SIGNAL}" opacity="{RAMP[d["lv"]]:.3f}"/>'
            )
        delay = wd * 0.22
        body.append(f'<g class="row" style="animation-delay:{delay:.2f}s">{"".join(cells)}</g>')
        if rows[wd]:
            body.append(label(GX - 30, GY + wd * STEP + 10, rows[wd], size=7, fill=DUST, spacing=0.15))

    # the powering-on flash line
    body.append(f'<rect x="{GX}" y="{GY - 2}" width="{GRID_W}" height="{GRID_H + 4}" '
                f'fill="{SIGNAL}" class="flash"/>')

    body.append(_months(m["weeks"], GY + GRID_H + 16))
    body.append(_footer(m, 200, "VSYNC 60HZ"))

    css = BLINK_CSS + f"""
    .row {{
      transform-origin: {GX}px 0; opacity: 0;
      animation: rowin {dur}s ease-out infinite;
    }}
    @keyframes rowin {{
      0%   {{ opacity: 0; transform: scaleX(0.02) }}
      6%   {{ opacity: 1; transform: scaleX(1) }}
      88%  {{ opacity: 1; transform: scaleX(1) }}
      96%  {{ opacity: 0; transform: scaleX(1) }}
      100% {{ opacity: 0; transform: scaleX(0.02) }}
    }}
    .flash {{ opacity: 0; animation: flash {dur}s linear infinite; }}
    @keyframes flash {{
      0%   {{ opacity: 0 }}
      2%   {{ opacity: 0.55 }}
      8%   {{ opacity: 0 }}
      100% {{ opacity: 0 }}
    }}"""
    return wrap(W, H, "\n".join(body), css,
                "contribution grid painted row by row on a CRT")


BUILD = {
    "01-waterfall": waterfall,
    "02-polar": lensing,
    "03-halftone": halftone,
    "04-oscilloscope": oscilloscope,
    "05-crt": crt,
}

if __name__ == "__main__":
    m = load()
    for name, fn in BUILD.items():
        p, size = save(f"{name}.svg", fn(m))
        print(f"{name:16} {size / 1024:6.1f} KB  {p}")
