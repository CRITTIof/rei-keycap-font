# Keycap Tight

**A transparent, content-fitted keycap and system-icon font, redrawn from a photographed Windows keyboard.**

Keycap Tight turns physical keys into clean, transparent outline glyphs. It includes **83 keycap glyphs**, **12 system line icons**, **101 `event.code` mappings**, and **62 ASCII aliases** — **95 glyphs** in total. Every keycap frame and icon sits in the same **1em / 62-unit** display slot, so they line up at any font size.

- **Version:** 1.4.0
- **Font family:** Keycap Tight Regular
- **Formats:** TTF + WOFF2
- **License:** SIL Open Font License 1.1
- **Author:** Rei Xinglan ([@CRITTIof](https://github.com/CRITTIof))

## Repository layout

This repository intentionally contains only what is needed to use, understand and rebuild the font.

```text
KeycapTight/
├─ demo.html                     Interactive keyboard demo
├─ fonts/
│  ├─ KeycapTight-Regular.ttf    Desktop font
│  └─ KeycapTight-Regular.woff2  Web font
├─ MAPPING.md                    Complete PUA / ASCII / event.code reference
├─ README.md
├─ src/
│  ├─ build_font.py              Font build entry point
│  ├─ data.py                    Key list and icon categories
│  └─ geometry.py                Glyph outlines and shared geometry
├─ assets/
│  ├─ noto-sans-semibold.ttf     Source outlines for multi-character legends
│  └─ jetbrains-mono-semibold.ttf Source outlines for A-Z / 0-9
├─ requirements.txt
├─ OFL.txt
└─ OFL-JetBrainsMono.txt
```

Generated specimens, per-glyph SVG folders, preview PNGs and ZIP archives are not committed. The release contains the final fonts and mapping documentation.

## Download and install

Download the latest fonts from **[Releases](https://github.com/CRITTIof/rei-keycap-frot/releases/latest)**.

- **Windows:** open `KeycapTight-Regular.ttf` and choose **Install**.
- **macOS:** open the TTF with **Font Book** and choose **Install Font**.
- **Web:** use `KeycapTight-Regular.woff2`:

```css
@font-face {
  font-family: "Keycap Tight";
  src: url("fonts/KeycapTight-Regular.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: block;
}

.key {
  font: 400 38px/1 "Keycap Tight";
  color: currentColor;
}
```

`font-size` is the visual key height. Use `line-height: 1` and color the glyph with `color` / `currentColor`; the interior is transparent.

## Demo

Open **`demo.html`** in a browser. It is a self-contained live keyboard demo and loads the fonts from `fonts/` with relative URLs.

The demo supports:

- Physical key presses through `event.code`
- Clickable keycaps
- Light / dark themes
- Size control
- A live glyph and keycode readout

No build step or local server is required.

## Quick start

Use a PUA codepoint for an exact glyph:

```html
<span class="key">&#xE000;</span>  <!-- Esc -->
<span class="key">&#xE053;</span>  <!-- CPU icon -->
<span class="key">&#xE059;</span>  <!-- CLI icon -->
```

Letters and digits are also mapped directly:

```html
<span class="key">A</span>
<span class="key">a</span>
<span class="key">7</span>
```

`A` and `a` both render the uppercase **A** keycap.

> **Important:** ASCII letters and digits are intentionally remapped to keycap glyphs. Do **not** use Keycap Tight for ordinary prose. Use a normal text font for body copy and Keycap Tight only for keycaps and pictograms.

## Mapping

The complete reference is **[MAPPING.md](MAPPING.md)**. It includes:

- All 95 PUA codepoints and glyph IDs
- All 62 ASCII aliases
- All 101 `event.code` mappings
- Category, legend and full name for every glyph
- JavaScript integration example

### Ranges

| Range | Contents |
|---|---|
| `U+E000–U+E052` | 83 keycap glyphs |
| `U+E053–U+E05E` | 12 system icons |
| `A–Z`, `a–z`, `0–9` | ASCII aliases to keycaps |

### System icons

| Software | PUA | Hardware | PUA |
|---|---|---|---|
| CLI | `U+E059` | CPU | `U+E053` |
| Web | `U+E05A` | GPU | `U+E054` |
| App | `U+E05B` | RAM | `U+E055` |
| Game | `U+E05C` | ROM / hard drive | `U+E056` |
| | | NetUp | `U+E057` |
| | | NetDown | `U+E058` |
| | | USB | `U+E05D` |
| | | Vol | `U+E05E` |

The `ROM` glyph follows the label on this keyboard, but the drawing is a hard drive (platter, spindle and actuator arm), not a ROM chip.

## Use with keyboard events

The font does not know about keyboard events. The release includes `keycap-tight-mapping.json`; map `event.code` to a codepoint, then render it:

```js
const mapping = await fetch("keycap-tight-mapping.json").then((r) => r.json());
const byCode = new Map(mapping.keys.map((key) => [key.code, key]));

document.addEventListener("keydown", (event) => {
  const key = byCode.get(event.code);
  if (!key) return;
  output.textContent = String.fromCodePoint(key.codepoint);
});
```

Duplicate physical keys share one glyph: `ShiftLeft` / `ShiftRight` both use `shift`, and `Digit7` / `Numpad7` both use `digit7`. All 101 `event.code` values are still listed individually.

## Build from source

Requirements: Python 3.10+ and the packages in `requirements.txt` (`fonttools` and `brotli`).

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
python src/build_font.py
```

The build writes:

```text
fonts/KeycapTight-Regular.ttf
fonts/KeycapTight-Regular.woff2
```

No Node.js, browser, image library or network access is needed.

### Editing the set

- Keycaps and icon categories: `src/data.py`
- Shared geometry, monospaced letter/digit rules and icon paths: `src/geometry.py`
- Font metadata and output paths: `src/build_font.py`

## Design notes

- Keycap frame: **62** design units high, **16** outer radius, **4** stroke, transparent interior.
- Width: text advance + **20** units on each side. All single letters and digits use **JetBrains Mono SemiBold** and share one **65.2-unit** frame width.
- Multi-character legends (`Esc`, `Tab`, `Ctrl`, `F1`, …) use **Noto Sans SemiBold** and fit their content.
- Icons use a **62 × 62** box and a **3.5** stroke; they have no keycap frame and no background.
- Font metrics: **1000 units/em**; every glyph occupies exactly **1em** of display height. Keycap frames are exactly **1000** units tall and all icons stay inside the same **0–1000** slot.
- The font is a single-color outline font. The interior is transparent; color comes from `color` / `currentColor`.

## Credits and license

Font outlines are derived from:

- **Noto Sans SemiBold** — Copyright 2018 The Noto Project Authors
- **JetBrains Mono SemiBold** — Copyright 2020 The JetBrains Mono Project Authors

Both are used and redistributed under the **SIL Open Font License 1.1**. See [OFL.txt](OFL.txt) and [OFL-JetBrainsMono.txt](OFL-JetBrainsMono.txt). The generated font is named **Keycap Tight** and does not use a reserved name from either source font.
