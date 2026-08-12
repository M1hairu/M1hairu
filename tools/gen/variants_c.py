"""Variant C: the signal index — the ./signals listing as an instrument panel.

Unlike the other variants this one carries no contribution data: it renders the
project table itself, so the section header reads like a directory listing from
the same machine as the rest of the profile. Edit SIGNALS to change the roster.
"""

from common import INK, SIGNAL, ASH, DUST, LINE, label, wrap

W = 920
PAD = 38
CHW = 6.62                                    # 11px mono advance

# index, name, type, status, state class
SIGNALS = [
    ("SIG-000", "M1X_WEB",       "WEB / VISUAL_SYSTEM",   "LIVE",     "live"),
    ("SIG-001", "UPSTORAGE",     "STORAGE / CRYPTO",      "ACTIVE",   "work"),
    ("SIG-002", "LOCATOR",       "SDR / AVIONICS",        "FIELD",    "work"),
    ("SIG-003", "WATCH_FACES",   "EMBEDDED / VISUAL",     "SHIPPED",  "done"),
    ("SIG-004", "SKYJOURNAL",    "ANDROID / OFFLINE",     "SHIPPED",  "done"),
    ("SIG-005", "MOEX_AI_AGENT", "TRADING_AI / ASYNCIO",  "ARCHIVED", "cold"),
    ("SIG-006", "TENDER_HACK",   "SEARCH / AGGREGATION",  "ARCHIVED", "cold"),
]

COLS = (56, 168, 372, 700)                    # index, signal, type, status


def signals(m=None):
    row_h = 24
    top = 78
    H = top + len(SIGNALS) * row_h + 56

    live = sum(1 for s in SIGNALS if s[4] == "live")
    body = [
        label(PAD, 32, "~/ ls -1 ./signals", size=11, fill=SIGNAL, spacing=0.16),
        label(W - PAD, 32, f"{len(SIGNALS)} ENTRIES · {live} LIVE · 4 PRIVATE",
              size=8.5, fill=DUST, spacing=0.2, anchor="end"),
        f'<line x1="{PAD}" y1="44" x2="{W - PAD}" y2="44" stroke="{LINE}"/>',
    ]

    # column headings
    heads = ("INDEX", "SIGNAL", "TYPE", "STATUS")
    for x, h in zip(COLS, heads):
        body.append(label(x, 64, h, size=8, fill=DUST, spacing=0.28))
    body.append(f'<line x1="{PAD}" y1="72" x2="{W - PAD}" y2="72" stroke="{LINE}"/>')

    for i, (idx, name, kind, status, state) in enumerate(SIGNALS):
        y = top + i * row_h + 15
        delay = 0.12 + i * 0.16
        row = [
            label(COLS[0], y, idx, size=9.5, fill=DUST, spacing=0.16),
            label(COLS[1], y, name, size=11.5, fill=SIGNAL, spacing=0.2),
            label(COLS[2], y, kind, size=9.5, fill=ASH, spacing=0.16),
        ]
        # status lamp: only the live signal pulses
        lamp_cls = "lamp" if state == "live" else ""
        lamp_fill = SIGNAL if state in ("live", "work") else DUST
        lamp_op = "1" if state == "live" else ("0.75" if state == "work" else "0.4")
        row.append(f'<circle cx="{COLS[3] + 4}" cy="{y - 4}" r="3" fill="{lamp_fill}" '
                   f'opacity="{lamp_op}" class="{lamp_cls}"/>')
        row.append(label(COLS[3] + 16, y, status, size=9.5,
                         fill=SIGNAL if state in ("live", "work") else DUST, spacing=0.2))
        # hairline under every row but the last
        if i < len(SIGNALS) - 1:
            row.append(f'<line x1="{PAD}" y1="{y + 9}" x2="{W - PAD}" y2="{y + 9}" '
                       f'stroke="{LINE}"/>')
        body.append(f'<g class="row" style="animation-delay:{delay:.2f}s">{"".join(row)}</g>')

    # footer: cursor + hint that the dossiers sit in the collapsed block below
    fy = H - 26
    body.append(f'<line x1="{PAD}" y1="{fy - 20}" x2="{W - PAD}" y2="{fy - 20}" '
                f'stroke="{LINE}"/>')
    body.append(f'<rect x="{PAD}" y="{fy - 9}" width="6" height="10" fill="{SIGNAL}" '
                f'class="blink"/>')
    body.append(label(PAD + 14, fy, "cat ./signals/*.dossier", size=9.5, fill=ASH,
                      spacing=0.16))
    body.append(label(W - PAD, fy, "EXPAND BELOW ↓", size=8.5, fill=DUST, spacing=0.24,
                      anchor="end"))

    # Resting state is visible and the animation only replays the reveal, so a
    # renderer that ignores CSS animation still shows the full listing.
    css = """
    .row { opacity: 1; animation: in .3s ease-out both; }
    @keyframes in { from { opacity: 0 } to { opacity: 1 } }
    .blink { animation: blink 1.1s steps(1) infinite; }
    @keyframes blink { 0%,49% { opacity: 1 } 50%,100% { opacity: 0 } }
    .lamp { animation: pulse 2.4s ease-in-out infinite; }
    @keyframes pulse { 0%,100% { opacity: .35 } 50% { opacity: 1 } }"""

    return wrap(W, H, "\n".join(body), css,
                "signal index — seven projects listed as a directory")
