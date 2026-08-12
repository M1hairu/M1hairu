"""Variant D: the contact panel — ./out answering a ping.

Channels report state, not fabricated latency: everything printed here is
either true or plainly a stylistic frame. The clickable links stay in the
README underneath, since a link inside an <img> is not a link.
"""

from common import INK, SIGNAL, ASH, DUST, LINE, label, wrap

W = 920
PAD = 38
CHW = 6.62

HOSTS = [
    ("m1hai.ru",                  "LIVE"),
    ("t.me/thesupremecommander",  "OPEN"),
    ("mihail.antsev@gmail.com",   "OPEN"),
]


def ping(m=None):
    row_h = 26
    top = 92
    H = top + len(HOSTS) * row_h + 96
    beat = 0.85                                  # seconds between packets
    cycle = beat * (len(HOSTS) + 3)

    body = [
        label(PAD, 32, "~/ ping ./out", size=11, fill=SIGNAL, spacing=0.16),
        label(W - PAD, 32, f"{len(HOSTS)} CHANNELS · 0% LOSS", size=8.5, fill=DUST,
              spacing=0.2, anchor="end"),
        f'<line x1="{PAD}" y1="44" x2="{W - PAD}" y2="44" stroke="{LINE}"/>',
        label(PAD, 68, f"PING ./out — {len(HOSTS)} channels, 56 data bytes", size=9.5,
              fill=ASH, spacing=0.14),
    ]

    for i, (host, state) in enumerate(HOSTS):
        y = top + i * row_h + 14
        delay = 0.3 + i * beat
        row = [
            label(PAD, y, "reply from", size=10, fill=DUST, spacing=0.12),
            label(PAD + 92, y, host, size=11.5, fill=SIGNAL, spacing=0.14),
            label(560, y, f"seq={i + 1}", size=9.5, fill=DUST, spacing=0.14),
            label(648, y, f"state={state}", size=9.5, fill=ASH, spacing=0.14),
        ]
        # transmission arcs, lit as the packet lands
        for k in range(3):
            r = 7 + k * 5
            row.append(
                f'<path d="M{W - PAD - 46} {y - 4 - r} A {r} {r} 0 0 1 {W - PAD - 46} {y - 4 + r}" '
                f'fill="none" stroke="{SIGNAL}" stroke-width="1.1" '
                f'opacity="{0.55 - k * 0.13:.2f}" class="arc" '
                f'style="animation-delay:{delay + k * 0.12:.2f}s"/>'
            )
        row.append(f'<circle cx="{W - PAD - 48}" cy="{y - 4}" r="2.4" fill="{SIGNAL}"/>')
        body.append(f'<g class="row" style="animation-delay:{delay:.2f}s">{"".join(row)}</g>')

    sy = top + len(HOSTS) * row_h + 30
    body.append(f'<line x1="{PAD}" y1="{sy - 20}" x2="{W - PAD}" y2="{sy - 20}" '
                f'stroke="{LINE}"/>')
    body.append(f'<g class="row" style="animation-delay:{0.3 + len(HOSTS) * beat:.2f}s">'
                + label(PAD, sy, "--- ./out ping statistics ---", size=9.5, fill=DUST,
                        spacing=0.14)
                + label(PAD, sy + 22, "3 packets transmitted, 3 received, 0% packet loss",
                        size=10, fill=ASH, spacing=0.14)
                + "</g>")

    # the profile's sign-off, blinking like a carrier that never quite settles
    by = sy + 52
    body.append(f'<rect x="{PAD}" y="{by - 10}" width="6" height="11" fill="{SIGNAL}" '
                f'class="blink"/>')
    body.append(label(PAD + 14, by, "[ SIGNAL REMAINS UNSTABLE ]", size=10.5, fill=SIGNAL,
                      spacing=0.24))

    css = f"""
    .row {{ opacity: 1; animation: land {cycle:.2f}s ease-out infinite; }}
    @keyframes land {{
      0%   {{ opacity: 0 }}
      4%   {{ opacity: 1 }}
      96%  {{ opacity: 1 }}
      100% {{ opacity: 0 }}
    }}
    .arc {{ opacity: 0; animation: ripple {cycle:.2f}s ease-out infinite; }}
    @keyframes ripple {{
      0%   {{ opacity: 0 }}
      3%   {{ opacity: .8 }}
      14%  {{ opacity: 0 }}
      100% {{ opacity: 0 }}
    }}
    .blink {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes blink {{ 0%,49% {{ opacity: 1 }} 50%,100% {{ opacity: 0 }} }}"""

    return wrap(W, H, "\n".join(body), css,
                "contact panel — three channels answering a ping")
