```
███╗   ███╗  ██╗ ██╗  ██╗
████╗ ████║ ███║ ╚██╗██╔╝
██╔████╔██║ ╚██║  ╚███╔╝
██║╚██╔╝██║  ██║  ██╔██╗
██║ ╚═╝ ██║  ██║ ██╔╝ ██╗
╚═╝     ╚═╝  ╚═╝ ╚═╝  ╚═╝
```

> CODE MEETS MOVEMENT · PROFILE AS TRANSMISSION

```
OPERATOR   M1HAIRU / M1X
FIELD      SYSTEMS · SIGNAL · VISUAL_INTERFACES
BASE       INFORMATION_SECURITY / BSC
STATE      TRANSMITTING
```

I build things that sit close to the metal and still have to look like something —
kernel quirks for hardware that ships broken on Linux, telemetry for machines that
run for years unattended, and interfaces that behave like archives rather than pages.

---

### `~/ ls -1 ./signals`

| INDEX | SIGNAL | TYPE | STATUS |
|---|---|---|---|
| `SIG-000` | [**M1X_WEB**](https://m1hai.ru) | WEB / VISUAL_SYSTEM | `LIVE / SELF_BUILT` |
| `SIG-007` | **IPU_BRIDGE_QUIRK** | KERNEL / MEDIA / DMI | `UPSTREAM` |
| `SIG-008` | **LOCATOR** | SDR / ADS-B / EMBEDDED | `IN_PROGRESS` |
| `SIG-009` | **BOILER_SERVICE** | TELEMETRY / PYTHON | `PRODUCTION` |
| `SIG-010` | **CAT_CLICKER** | GAMEDEV / YANDEX_GAMES | `SHIPPED` |
| `SIG-001` | **MOEX_AI_AGENT** | TRADING_AI / ASYNCIO | `ARCHIVED / HACKATHON` |
| `SIG-002` | **TENDER_HACK** | SEARCH / AGGREGATION | `ARCHIVED / HACKATHON` |

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

**`SIG-007` — IPU_BRIDGE_QUIRK** · mainline Linux
The Galaxy Book5 Pro 360 mounts its OV02E10 sensor rotated 180°, but Samsung's ACPI
firmware reports 0° in both the SSDB and the `_PLD` — so libcamera renders every frame
upside-down. A DMI quirk in `drivers/media/pci/intel/ipu-bridge.c` sets the sensor
fwnode's `rotation` to 180, userspace compensates, and the out-of-tree DKMS workaround
becomes unnecessary. `checkpatch --strict`: clean. Separate finding filed alongside it:
wrong Bayer CFA order under H/V flips (`GRBG` unflipped vs `RGGB` flipped), measured by
raw Bayer phase analysis of ISYS captures.
`C` `LINUX_KERNEL` `V4L2` `LIBCAMERA` `ACPI`

**`SIG-008` — LOCATOR**
Portable ADS-B receiver (1090 MHz, RTL-SDR Blog V4) that renders the air picture around
your own aircraft — built for general-aviation pilots. Phased: SDR diagnostics → laptop
receiver + web UI → Raspberry Pi with e-ink → GPS positioning → product.
`PYTHON` `RTL-SDR` `ADS-B` `RASPBERRY_PI` `E-INK`

**`SIG-009` — BOILER_SERVICE**
Gas-consumption monitoring for a 96 kW Baxi boiler cascade (3×33.1) through ZONT
H2000+ PRO. Accounting is derived from burner modulation and calibrated against real
meter readings. Designed to survive months unattended: self-refreshing tokens,
incremental SQLite metering, API failures that degrade instead of writing zeros.
`PYTHON` `SQLITE` `CLOUDFLARE_WORKERS` `TELEGRAM`

**`SIG-010` — CAT_CLICKER**
Yandex Games title under the *Пельмень Геймс* label. SVG character rig, skin system,
generated art pipeline, i18n, original soundtrack.
`JAVASCRIPT` `SVG` `CANVAS` `YANDEX_GAMES_SDK`

</details>

---

### `~/ cat ./stack`

```
LOW      C · LINUX_KERNEL · V4L2 · DKMS · ACPI · EMBEDDED
CORE     PYTHON · TYPESCRIPT · JAVASCRIPT · SQL
SURFACE  NEXT.JS · REACT · TAILWIND · WEBGL · CANVAS · FRAMER_MOTION
FIELD    RTL-SDR · ARDUINO · RASPBERRY_PI · 3D_PRINTING · BLENDER
HOST     ARCH · HYPRLAND · NGINX · SYSTEMD · DOCKER
```

### `~/ cat ./record`

```
FINALIST   National Technology Olympiad — Wireless Communication Technologies
PRIZE      Bolshie Vyzovy (Sirius)
PRIZE      HSE University Case Championship
1ST        MPIT — regional stage
```

---

### `~/ ping ./out`

[`m1hai.ru`](https://m1hai.ru) · [`telegram`](https://t.me/thesupremecommander) · `mihail.antsev@gmail.com`

```
[ SIGNAL REMAINS UNSTABLE ]
```
