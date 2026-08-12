#!/usr/bin/env python3
"""Render the chosen variants into .assets/.

    python tools/render.py waterfall            -> .assets/heatmap.svg
    python tools/render.py waterfall boot       -> heatmap.svg + boot.svg

Each variant is a self-contained SVG: all motion is CSS inside the file,
because GitHub strips <script> from anything it renders.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "gen"))

from common import load, save              # noqa: E402
import variants_a                          # noqa: E402
import variants_b                          # noqa: E402
import variants_c                          # noqa: E402
import variants_d                          # noqa: E402

# variant name -> (builder, output filename)
CATALOG = {
    "waterfall":    (variants_a.waterfall,    "heatmap.svg"),
    "polar":        (variants_a.lensing,      "heatmap.svg"),
    "halftone":     (variants_a.halftone,     "heatmap.svg"),
    "oscilloscope": (variants_a.oscilloscope, "heatmap.svg"),
    "crt":          (variants_a.crt,          "heatmap.svg"),
    "tape":         (variants_b.tape,         "heatmap.svg"),
    "spectrum":     (variants_b.spectrum,     "heatmap.svg"),
    "glitch":       (variants_b.glitch,       "heatmap.svg"),
    "accretion":    (variants_b.accretion,    "heatmap.svg"),
    "boot":         (variants_b.boot,         "boot.svg"),
    "signals":      (variants_c.signals,      "signals.svg"),
    "ping":         (variants_d.ping,         "ping.svg"),
}


def main():
    names = sys.argv[1:] or ["waterfall"]
    unknown = [n for n in names if n not in CATALOG]
    if unknown:
        sys.exit(f"unknown variant(s): {', '.join(unknown)}\n"
                 f"available: {', '.join(CATALOG)}")

    # validate the whole set before writing anything
    seen = {}
    for name in names:
        out = CATALOG[name][1]
        if out in seen:
            sys.exit(f"'{seen[out]}' and '{name}' both write {out} — pick one heatmap")
        seen[out] = name

    m = load()
    for name in names:
        fn, out = CATALOG[name]
        path, size = save(out, fn(m))
        print(f"{name:14} -> {path}  ({size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
