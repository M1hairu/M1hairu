"""Variants B: tape, spectrum, glitch, accretion, boot."""

import math
from common import (INK, SIGNAL, ASH, DUST, LINE, RAMP, MONO, load, month_ticks,
                    label, metrics_line, wrap, save)
from variants_a import W, PAD, CELL, GAP, STEP, GRID_W, GX, GY, GRID_H, _header, _months, _footer, BLINK_CSS


# --------------------------------------------------------------------- 06 tape
def tape(m):
    """Punched tape: each day punches a column, the reel runs continuously."""
    H, dur = 220, 26.0
    days = m["days"]
    pitch = 6.0
    tw = len(days) * pitch                   # one full reel width
    ty = 62                                  # tape top
    th = 104                                 # tape height
    lanes = 5                                # data lanes above the sprocket
    tp = 15.0
    sprocket_y = th - 20

    holes = []
    prev_month = None
    for i, d in enumerate(days):
        x = i * pitch + pitch / 2
        # sprocket lane — the constant rhythm that sells the motion
        holes.append(f'<circle cx="{x:.1f}" cy="{sprocket_y:.0f}" r="1.0" fill="{ASH}" '
                     f'opacity="0.7"/>')
        # week rule every Monday
        if d["wd"] == 0:
            holes.append(f'<line x1="{x:.1f}" y1="6" x2="{x:.1f}" y2="{th - 6:.0f}" '
                         f'stroke="{SIGNAL}" stroke-width="0.5" opacity="0.07"/>')
        # month stamp travels with the reel so empty stretches still read as archive
        month = d["date"][:7]
        if month != prev_month:
            prev_month = month
            holes.append(f'<line x1="{x:.1f}" y1="4" x2="{x:.1f}" y2="{th - 4:.0f}" '
                         f'stroke="{SIGNAL}" stroke-width="0.7" opacity="0.22"/>')
            holes.append(
                f'<text x="{x + 4:.1f}" y="13" font-size="7" fill="{DUST}" '
                f'letter-spacing="0.2em">{d["date"][:7].replace("-", ".")}</text>'
            )
        if d["lv"] == 0:
            # unpunched frame — a shallow dimple keeps the data lane continuous
            holes.append(f'<circle cx="{x:.1f}" cy="{sprocket_y - 14:.0f}" r="0.45" '
                         f'fill="{SIGNAL}" opacity="0.22"/>')
        for lv in range(d["lv"]):
            cy = sprocket_y - 14 - lv * tp
            holes.append(f'<circle cx="{x:.1f}" cy="{cy:.0f}" r="2.1" fill="{SIGNAL}" '
                         f'opacity="{0.55 + 0.11 * lv:.2f}"/>')

    reel = (f'<g id="reel"><rect x="0" y="0" width="{tw:.0f}" height="{th}" fill="{SIGNAL}" '
            f'opacity="0.03"/>{"".join(holes)}</g>')

    body = [_header(m, "~/ dd if=./contributions of=/dev/tape0",
                    f"{len(days)} FRAMES · 5-LANE")]
    body.append(f'<defs>{reel}<clipPath id="win"><rect x="{PAD}" y="{ty}" '
                f'width="{W - PAD * 2}" height="{th}"/></clipPath></defs>')
    body.append(f"""
  <g clip-path="url(#win)">
    <g class="run" transform="translate({PAD},{ty})">
      <use href="#reel" x="0"/>
      <use href="#reel" x="{tw:.0f}"/>
    </g>
  </g>
  <line x1="{PAD}" y1="{ty - 4}" x2="{W - PAD}" y2="{ty - 4}" stroke="{LINE}"/>
  <line x1="{PAD}" y1="{ty + th + 4}" x2="{W - PAD}" y2="{ty + th + 4}" stroke="{LINE}"/>
  <rect x="{W / 2 - 1}" y="{ty - 10}" width="2" height="{th + 20}" fill="{SIGNAL}"
        opacity="0.5" class="blink"/>""")

    body.append(label(PAD, ty + th + 22, "COLUMN = ONE DAY   ·   PUNCH DEPTH = CONTRIBUTION "
                      "LEVEL   ·   LOWER LANE = SPROCKET", size=7.5, fill=DUST, spacing=0.2))
    body.append(_footer(m, 200, "READ HEAD LOCKED"))

    css = BLINK_CSS + f"""
    .run {{ animation: roll {dur}s linear infinite; }}
    @keyframes roll {{
      from {{ transform: translate({PAD}px,{ty}px) }}
      to   {{ transform: translate({PAD - tw:.0f}px,{ty}px) }}
    }}"""
    return wrap(W, H, "\n".join(body), css,
                "contribution history punched onto a running paper tape")


# ----------------------------------------------------------------- 07 spectrum
def spectrum(m):
    """Spectrum analyser: weekly power, peak-hold caps, live noise floor."""
    H = 236
    base, top = 186, 58
    bw = 13.0
    gap = STEP - bw

    weeks = [sum(d["n"] for d in w) for w in m["weeks"]]
    wmax = max(1, max(weeks))

    body = [_header(m, "~/ fft ./contributions --bins 53w",
                    f"PEAK {wmax}/W   FLOOR -{60 - int(wmax / 4)}dB")]

    # dB graticule
    for i in range(5):
        y = top + (base - top) * i / 4
        body.append(f'<line x1="{GX}" y1="{y:.0f}" x2="{GX + GRID_W}" y2="{y:.0f}" '
                    f'stroke="{LINE}"/>')
        body.append(label(GX - 8, y + 3, f"-{i * 15}", size=6.5, fill=DUST, spacing=0.1,
                          anchor="end"))

    for i, v in enumerate(weeks):
        x = GX + i * STEP
        amp = (v / wmax) ** 0.6
        h = amp * (base - top)
        phase = (i * 0.37) % 1.0
        # noise floor — receiver hiss, keeps empty weeks alive
        nh = 2 + (i * 7 % 5) * 0.9
        body.append(f'<rect x="{x}" y="{base - nh:.1f}" width="{bw}" height="{nh:.1f}" '
                    f'fill="{SIGNAL}" opacity="0.14" class="noise" '
                    f'style="animation-delay:{phase * 1.8:.2f}s"/>')
        if v > 0:
            body.append(
                f'<g class="bar" style="animation-delay:{phase * 2.4:.2f}s;'
                f'transform-origin:{x + bw / 2:.1f}px {base}px">'
                f'<rect x="{x}" y="{base - h:.1f}" width="{bw}" height="{h:.1f}" '
                f'fill="{SIGNAL}" opacity="{0.35 + 0.5 * amp:.2f}"/></g>'
            )
            body.append(f'<rect x="{x}" y="{base - h - 3:.1f}" width="{bw}" height="1.6" '
                        f'fill="{SIGNAL}" opacity="0.95"/>')

    body.append(f'<line x1="{GX}" y1="{base}" x2="{GX + GRID_W}" y2="{base}" '
                f'stroke="{DUST}"/>')
    body.append(_months(m["weeks"], base + 18))
    body.append(_footer(m, 212, "RBW 1W · AVG OFF"))

    css = BLINK_CSS + """
    .bar { animation: breathe 2.4s ease-in-out infinite; }
    @keyframes breathe {
      0%,100% { transform: scaleY(0.94) }
      50%     { transform: scaleY(1) }
    }
    .noise { animation: hiss 1.8s steps(3) infinite; }
    @keyframes hiss {
      0%   { opacity: .08 }
      33%  { opacity: .2 }
      66%  { opacity: .12 }
      100% { opacity: .08 }
    }"""
    return wrap(W, H, "\n".join(body), css,
                "weekly contribution power on a spectrum analyser")


# -------------------------------------------------------------------- 08 glitch
def glitch(m):
    """The grid, torn into horizontal slices that slip out of register."""
    H = 224
    cells = []
    for ci, week in enumerate(m["weeks"]):
        for d in week:
            cells.append(
                f'<rect x="{GX + ci * STEP}" y="{GY + d["wd"] * STEP}" width="{CELL}" '
                f'height="{CELL}" fill="{SIGNAL}" opacity="{RAMP[d["lv"]]:.3f}"/>'
            )
    grid = f'<g id="grid">{"".join(cells)}</g>'

    slices = []
    cuts = [(0, 26, "a"), (26, 34, "b"), (60, 22, "c"), (82, 27, "d")]
    for i, (off, hh, cls) in enumerate(cuts):
        slices.append(f"""
    <clipPath id="cut{i}"><rect x="{GX - 4}" y="{GY + off}" width="{GRID_W + 8}" height="{hh}"/></clipPath>""")

    body = [_header(m, "~/ xxd ./contributions | corrupt --slices 4", "CHECKSUM MISMATCH")]
    body.append(f'<defs>{grid}{"".join(slices)}</defs>')
    body.append(f'<use href="#grid" opacity="0.75"/>')
    for i, (off, hh, cls) in enumerate(cuts):
        body.append(f'<g clip-path="url(#cut{i})" class="s{cls}"><use href="#grid"/></g>')
    # ghost registers — the site's monochrome text-glitch shadow, applied to the grid
    body.append(f'<g class="ghost" opacity="0.35"><use href="#grid"/></g>')

    body.append(_months(m["weeks"], GY + GRID_H + 16))
    body.append(_footer(m, 200, "RESYNC 0.4s"))

    css = BLINK_CSS + """
    .sa { animation: ga 2.2s steps(2) infinite; }
    .sb { animation: gb 1.8s steps(2) infinite reverse; }
    .sc { animation: gc 3.1s steps(2) infinite; }
    .sd { animation: gd 2.6s steps(2) infinite reverse; }
    @keyframes ga { 0%,88% { transform: translateX(0) } 90% { transform: translateX(-9px) } 100% { transform: translateX(0) } }
    @keyframes gb { 0%,82% { transform: translateX(0) } 86% { transform: translateX(13px) } 100% { transform: translateX(0) } }
    @keyframes gc { 0%,91% { transform: translateX(0) } 94% { transform: translateX(-6px) } 100% { transform: translateX(0) } }
    @keyframes gd { 0%,86% { transform: translateX(0) } 89% { transform: translateX(8px) } 100% { transform: translateX(0) } }
    .ghost { animation: gh 3.5s steps(2) infinite; }
    @keyframes gh {
      0%,92% { transform: translateX(0); opacity: 0 }
      94%    { transform: translateX(3px); opacity: .5 }
      96%    { transform: translateX(-3px); opacity: .35 }
      100%   { transform: translateX(0); opacity: 0 }
    }"""
    return wrap(W, H, "\n".join(body), css,
                "contribution grid tearing into glitch slices")


# ---------------------------------------------------------------- 09 accretion
def accretion(m):
    """Tilted accretion disk: each active day is matter on a Keplerian orbit."""
    H = 300
    cx, cy = W / 2, 158.0
    r0, dr = 52.0, 13.0
    tilt = 0.34

    body = [_header(m, "~/ orbit ./contributions --keplerian --tilt 20deg",
                    f"{m['active']} BODIES IN ORBIT")]

    rings = []
    for wd in range(7):
        r = r0 + wd * dr
        parts = []
        for ci, week in enumerate(m["weeks"]):
            d = next((x for x in week if x["wd"] == wd), None)
            if d is None:
                continue
            a = (ci / 53) * 2 * math.pi
            x, y = r * math.cos(a), r * math.sin(a)
            if d["lv"] == 0:
                # cold dust — keeps the orbit legible where nothing was committed
                parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="0.6" fill="{SIGNAL}" '
                             f'opacity="0.16"/>')
                continue
            rr = 1.2 + d["lv"] * 0.85
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="{SIGNAL}" '
                         f'opacity="{RAMP[d["lv"]]:.3f}"/>')
        period = 14 + wd * 5.5              # inner orbits run faster
        rings.append(f"""
    <ellipse cx="0" cy="0" rx="{r}" ry="{r}" fill="none" stroke="{LINE}" stroke-width="0.7"/>
    <g class="orb" style="animation-duration:{period:.1f}s">{"".join(parts)}</g>""")

    body.append(f"""
  <g transform="translate({cx},{cy}) scale(1,{tilt})">
    {"".join(rings)}
  </g>
  <ellipse cx="{cx}" cy="{cy}" rx="{r0 - 14}" ry="{(r0 - 14) * tilt}" fill="{INK}"/>
  <circle cx="{cx}" cy="{cy}" r="{r0 - 22}" fill="{INK}" stroke="{SIGNAL}" stroke-width="1"
          opacity="0.9" class="ring"/>
  <ellipse cx="{cx}" cy="{cy}" rx="{r0 + 6 * dr + 14}" ry="{(r0 + 6 * dr + 14) * tilt}"
           fill="none" stroke="{LINE}" stroke-dasharray="2 6"/>""")

    body.append(label(GX, 258, "RING = WEEKDAY   ·   ANGLE = WEEK OF YEAR   ·   "
                      "MASS = CONTRIBUTIONS", size=7.5, fill=DUST, spacing=0.22))
    body.append(_footer(m, 276, "DOPPLER BEAMING ON"))

    css = BLINK_CSS + """
    .orb { animation-name: spin; animation-timing-function: linear; animation-iteration-count: infinite; }
    @keyframes spin { from { transform: rotate(0deg) } to { transform: rotate(360deg) } }
    .ring { animation: pulse 4s ease-in-out infinite; }
    @keyframes pulse { 0%,100% { opacity: .55 } 50% { opacity: 1 } }"""
    return wrap(W, H, "\n".join(body), css,
                "contributions orbiting as an accretion disk")


# -------------------------------------------------------------------- 10 boot
def boot(m):
    """The console block from the README, actually booting."""
    H = 282
    CHW = 6.62                                   # 11px mono advance, no tracking
    x0, y0, lh = PAD + 8, 62, 22
    lines = [
        ("$ boot --profile M1HAIRU", SIGNAL, ""),
        ("", "", ""),
        ("  [ok]  operator ....... M1HAIRU / M1X", ASH, "ok"),
        ("  [ok]  field .......... SYSTEMS · SIGNAL · VISUAL_INTERFACES", ASH, "ok"),
        ("  [ok]  base ........... INFORMATION_SECURITY / BSC", ASH, "ok"),
        ("  [ok]  signal_log ..... " + f"{m['total']} CONTRIBUTIONS / 53W", ASH, "ok"),
        ("  [··]  state .......... TRANSMITTING", SIGNAL, "run"),
    ]

    body = [f'<rect x="{PAD}" y="40" width="{W - PAD * 2}" height="172" fill="none" '
            f'stroke="{LINE}"/>']

    # Typed character by character: a clipPath animated with SMIL renders
    # unreliably in Chrome (the frozen clip is not always repainted), so each
    # glyph is its own element fading in on the terminal grid.
    t = 0.0
    last_line = ""
    for i, (txt, col, kind) in enumerate(lines):
        if not txt:
            t += 0.18
            continue
        y = y0 + i * lh
        glyphs = []
        for j, ch in enumerate(txt):
            if ch == " ":
                continue
            g = {"<": "&lt;", ">": "&gt;", "&": "&amp;", "·": "&#183;"}.get(ch, ch)
            glyphs.append(
                f'<text x="{x0 + j * CHW:.1f}" y="{y}" font-size="11" class="ch" '
                f'style="animation-delay:{t + j * 0.022:.2f}s">{g}</text>'
            )
        body_line = f'<g fill="{col}">{"".join(glyphs)}</g>'
        body.append(body_line)
        t += len(txt) * 0.022 + 0.14
        last_line = txt

    # cursor parked at the end of the last line
    cy = y0 + (len(lines) - 1) * lh
    body.append(f'<rect x="{x0 + len(last_line) * CHW + 3:.0f}" y="{cy - 11}" width="7" '
                f'height="13" fill="{SIGNAL}" opacity="0" class="cur" '
                f'style="animation-delay:{t:.2f}s"/>')

    # ascii progress bar
    by = 238
    cells, cw, cs = 40, 6, 9
    body.append(label(x0, by, "[", size=11, fill=DUST, spacing=0.06))
    for i in range(cells):
        body.append(f'<rect x="{x0 + 12 + i * cs:.0f}" y="{by - 9}" width="{cw}" height="10" '
                    f'fill="{SIGNAL}" opacity="0" class="pb" '
                    f'style="animation-delay:{t + i * 0.03:.2f}s"/>')
    body.append(label(x0 + 12 + cells * cs + 6, by, "]", size=11, fill=DUST, spacing=0.06))
    body.append(f'<g class="pct" style="animation-delay:{t + cells * 0.03:.2f}s" opacity="0">'
                + label(W - PAD - 8, by, "100%", size=10, fill=SIGNAL, spacing=0.1, anchor="end")
                + "</g>")

    body.append(label(x0, 268, metrics_line(m), size=8.5, fill=DUST, spacing=0.22))

    css = """
    .ch { opacity: 0; animation: on 0.01s linear forwards; letter-spacing: 0; }
    @keyframes on { to { opacity: 1 } }
    .cur { animation: blink 1.1s steps(1) infinite; }
    @keyframes blink { 0%,49% { opacity: 1 } 50%,100% { opacity: 0 } }
    .pb { animation: fill 0.1s linear forwards; }
    @keyframes fill { to { opacity: 0.9 } }
    .pct { animation: fill 0.2s linear forwards; }"""
    return wrap(W, H, "\n".join(body), css,
                "the profile boot sequence typing itself out")


BUILD = {
    "06-tape": tape,
    "07-spectrum": spectrum,
    "08-glitch": glitch,
    "09-accretion": accretion,
    "10-boot": boot,
}

if __name__ == "__main__":
    m = load()
    for name, fn in BUILD.items():
        p, size = save(f"{name}.svg", fn(m))
        print(f"{name:16} {size / 1024:6.1f} KB")
