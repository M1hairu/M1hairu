<img alt="m1x — a Schwarzschild black hole, photon geodesics integrated per pixel" src="https://raw.githubusercontent.com/M1hairu/M1hairu/main/.assets/header.gif" width="100%">

<img alt="$ boot --profile M1HAIRU — operator M1HAIRU / M1X, field SYSTEMS · SIGNAL · VISUAL_INTERFACES, base INFORMATION_SECURITY / BSC, state TRANSMITTING" src="https://raw.githubusercontent.com/M1hairu/M1hairu/main/.assets/boot.svg" width="100%">

I build systems that have to hold up twice — once as engineering, once as something
you actually look at. Encrypted storage that survives losing nodes, receivers that pull
aircraft out of the air, and interfaces that behave like archives, not pages.

---

<img alt="signal index — SIG-000 M1X_WEB (live), SIG-001 UPSTORAGE, SIG-002 LOCATOR, SIG-003 WATCH_FACES, SIG-004 SKYJOURNAL, SIG-005 MOEX_AI_AGENT, SIG-006 TENDER_HACK" src="https://raw.githubusercontent.com/M1hairu/M1hairu/main/.assets/signals.svg" width="100%">

<details>
<summary><code>~/ cat ./signals/*.dossier</code></summary>

<br>

**`SIG-000` — M1X_WEB** · [m1hai.ru](https://m1hai.ru)
A scroll-driven portfolio built as a cinematic signal archive. Its centerpiece is a
WebGL fragment shader that integrates photon null geodesics through the Schwarzschild
metric (`a = -3/2 · h² · r / |r|⁵`) — real gravitational lensing, so the accretion disk
wraps over and under the event horizon into an Einstein ring, with Doppler beaming,
rendered monochrome + Bayer dither at low internal resolution for the halftone look.
Falls back to a Canvas 2D particle field and respects `prefers-reduced-motion`.
`NEXT.JS 15` `REACT 19` `TYPESCRIPT` `WEBGL` `FRAMER_MOTION` `NGINX`

**`SIG-001` — UPSTORAGE**
Decentralised encrypted file storage. The client cuts a file into segments, encrypts them
under its own key and spreads Reed-Solomon shards across keeper nodes. A keeper only ever
holds opaque blocks addressed by their own hash — it can read neither the data nor the
file names. RS(10,4) costs 140% overhead instead of replication's 500% at the same
tolerance; content addressing buys dedup, integrity checks and repair without keys;
rendezvous hashing means a departing node moves only 1/N of the shards. One Rust core
serves desktop and mobile over FFI instead of duplicating the logic.
`RUST` `FLUTTER` `REED-SOLOMON` `BLAKE3` `FFI`

**`SIG-002` — LOCATOR**
Portable ADS-B receiver for general-aviation pilots: 1090 MHz off an RTL-SDR Blog V4,
decoding the traffic around your own aircraft. Prototype runs on a laptop with a web UI;
the product moves to Raspberry Pi with e-ink and GPS as a standalone panel. The V4 ships
an R828D tuner, so it needs the rtlsdrblog fork of librtlsdr — the stock distro driver
tunes silently and wrong.
`RTL-SDR` `ADS-B` `PYTHON` `RASPBERRY_PI` `E-INK`

**`SIG-003` — WATCH_FACES**
Nine Connect IQ watch faces for Garmin epix Pro (Gen 2) in the same dither / pixel-dark
language that holds up m1hai.ru. The AMOLED panel takes 65k colours, so 1-bit dithering
here is a style decision, not a constraint — what actually constrains is memory: a
full-screen frame costs 25 KB at two levels and 201 KB at full scale, against a 128 KB
budget for the entire face.
`MONKEY_C` `CONNECT_IQ` `BAYER_DITHER` `AMOLED`

**`SIG-004` — SKYJOURNAL**
Offline flight log for an amphibian-aircraft pilot. A panel floats above the navigation
map, so marking a take-off or a landing is one tap without leaving navigation, stamped in
both UTC and local time — the evening logbook stops being an exercise in memory. No
network path at all: installed from a signed APK, never checks for updates.
`KOTLIN` `JETPACK_COMPOSE` `ANDROID` `OFFLINE_FIRST`

**`SIG-005` — MOEX_AI_AGENT**
Autonomous MOEX trading prototype: a long-only momentum core with risk gates,
persistent state, audit logs and LLM-assisted market-regime checks — the model acts as
an extra signal, not as blind automation.
`PYTHON` `ASYNCIO` `TRADING` `RISK` `LLM`

**`SIG-006` — TENDER_HACK**
Search layer for fragmented marketplaces: queries WB, Ozon, Yandex Market and open-web
sources through SearXNG, then groups, filters and ranks noisy results into a single
usable product-search surface.
`FASTAPI` `REACT` `SCRAPING` `SEARCH` `ML`

</details>

---

<img alt="contribution waterfall — a scan beam sweeping 53 weeks of signal" src="https://raw.githubusercontent.com/M1hairu/M1hairu/main/.assets/heatmap.svg" width="100%">

---

### `~/ tree ./stack`

```
.
├── LOW ········ C · RUST · MONKEY_C · LINUX_KERNEL · V4L2 · DKMS · ACPI
├── CORE ······· PYTHON · TYPESCRIPT · KOTLIN · SQL
├── SURFACE ···· NEXT.JS · REACT · TAILWIND · WEBGL · COMPOSE · FLUTTER
├── FIELD ······ RTL-SDR · ADS-B · RASPBERRY_PI · E-INK · ARDUINO · 3D_PRINTING
└── HOST ······· ARCH · HYPRLAND · NGINX · SYSTEMD · DOCKER
```

### `~/ cat ./record`

```
FINALIST ··· National Technology Olympiad — Wireless Communication Technologies
PRIZE ······ Bolshie Vyzovy (Sirius)
PRIZE ······ HSE University Case Championship
1ST ········ MPIT — regional stage
```

> **Whoever creates always destroys.**
> `— F. NIETZSCHE`

---

### `~/ ping ./out`

[`m1hai.ru`](https://m1hai.ru) · [`telegram`](https://t.me/thesupremecommander) · `mihail.antsev@gmail.com`

```
[ SIGNAL REMAINS UNSTABLE ]
```
