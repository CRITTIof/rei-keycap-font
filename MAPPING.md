# Keycap Tight — Mapping Reference

Version **1.4.0** · **95** glyphs · **101** `event.code` values · **62** ASCII aliases · **157** font cmap entries.

This document explains how characters, PUA codepoints and browser keyboard events map to the glyphs in **Keycap Tight**.

## 1. Three ways to address a glyph

1. **PUA codepoint** — every glyph has a stable codepoint in `U+E000–U+E05E`. Use this when you need an exact keycap or icon.
2. **ASCII alias** — `A–Z`, `a–z` and `0–9` are also mapped to the matching keycap. `A` and `a` intentionally produce the same uppercase A keycap.
3. **`event.code`** — map a physical key to its glyph through `keycap-tight-mapping.json` (or the table below), then render `String.fromCodePoint(codepoint)`.

```css
@font-face {
  font-family: "Keycap Tight";
  src: url("fonts/KeycapTight-Regular.woff2") format("woff2");
}

.key { font: 400 38px/1 "Keycap Tight"; color: currentColor; }
```

```html
<span class="key">&#xE000;</span>   <!-- Esc by PUA -->
<span class="key">A</span>          <!-- A key by ASCII alias -->
<span class="key">7</span>          <!-- 7 key by ASCII alias -->
```

> **Do not use this font for ordinary prose.** ASCII letters and digits are intentionally remapped to keycaps. Use a normal text font for body copy and Keycap Tight only for keycaps and icons.

## 2. PUA glyph map

Keycaps occupy `U+E000–U+E052`; the 12 system icons occupy `U+E053–U+E05E`.

| PUA | Glyph ID | Type | Group | Legend | Full name | ASCII aliases |
|---|---|---|---|---|---|---|
| <code>U+E000</code> | <code>escape</code> | keycap | function | <code>Esc</code> | Escape | — |
| <code>U+E001</code> | <code>f1</code> | keycap | function | <code>F1</code> | F1 | — |
| <code>U+E002</code> | <code>f2</code> | keycap | function | <code>F2</code> | F2 | — |
| <code>U+E003</code> | <code>f3</code> | keycap | function | <code>F3</code> | F3 | — |
| <code>U+E004</code> | <code>f4</code> | keycap | function | <code>F4</code> | F4 | — |
| <code>U+E005</code> | <code>f5</code> | keycap | function | <code>F5</code> | F5 | — |
| <code>U+E006</code> | <code>f6</code> | keycap | function | <code>F6</code> | F6 | — |
| <code>U+E007</code> | <code>f7</code> | keycap | function | <code>F7</code> | F7 | — |
| <code>U+E008</code> | <code>f8</code> | keycap | function | <code>F8</code> | F8 | — |
| <code>U+E009</code> | <code>f9</code> | keycap | function | <code>F9</code> | F9 | — |
| <code>U+E00A</code> | <code>f10</code> | keycap | function | <code>F10</code> | F10 | — |
| <code>U+E00B</code> | <code>f11</code> | keycap | function | <code>F11</code> | F11 | — |
| <code>U+E00C</code> | <code>f12</code> | keycap | function | <code>F12</code> | F12 | — |
| <code>U+E00D</code> | <code>insert</code> | keycap | function | <code>Ins</code> | Insert | — |
| <code>U+E00E</code> | <code>delete</code> | keycap | function | <code>Del</code> | Delete | — |
| <code>U+E00F</code> | <code>home</code> | keycap | function | <code>Home</code> | Home | — |
| <code>U+E010</code> | <code>end</code> | keycap | function | <code>End</code> | End | — |
| <code>U+E011</code> | <code>pageup</code> | keycap | function | <code>PgUp</code> | Page Up | — |
| <code>U+E012</code> | <code>pagedown</code> | keycap | function | <code>PgDn</code> | Page Down | — |
| <code>U+E013</code> | <code>backquote</code> | keycap | numbers | <code>`</code> | Backquote | — |
| <code>U+E014</code> | <code>digit1</code> | keycap | numbers | <code>1</code> | 1 | <code>1</code> |
| <code>U+E015</code> | <code>digit2</code> | keycap | numbers | <code>2</code> | 2 | <code>2</code> |
| <code>U+E016</code> | <code>digit3</code> | keycap | numbers | <code>3</code> | 3 | <code>3</code> |
| <code>U+E017</code> | <code>digit4</code> | keycap | numbers | <code>4</code> | 4 | <code>4</code> |
| <code>U+E018</code> | <code>digit5</code> | keycap | numbers | <code>5</code> | 5 | <code>5</code> |
| <code>U+E019</code> | <code>digit6</code> | keycap | numbers | <code>6</code> | 6 | <code>6</code> |
| <code>U+E01A</code> | <code>digit7</code> | keycap | numbers | <code>7</code> | 7 | <code>7</code> |
| <code>U+E01B</code> | <code>digit8</code> | keycap | numbers | <code>8</code> | 8 | <code>8</code> |
| <code>U+E01C</code> | <code>digit9</code> | keycap | numbers | <code>9</code> | 9 | <code>9</code> |
| <code>U+E01D</code> | <code>digit0</code> | keycap | numbers | <code>0</code> | 0 | <code>0</code> |
| <code>U+E01E</code> | <code>minus</code> | keycap | numbers | <code>-</code> | Minus | — |
| <code>U+E01F</code> | <code>equal</code> | keycap | numbers | <code>=</code> | Equal | — |
| <code>U+E020</code> | <code>backspace</code> | keycap | numbers | <code>Back</code> | Backspace | — |
| <code>U+E021</code> | <code>tab</code> | keycap | letters | <code>Tab</code> | Tab | — |
| <code>U+E022</code> | <code>keyq</code> | keycap | letters | <code>Q</code> | Q | <code>Q</code>, <code>q</code> |
| <code>U+E023</code> | <code>keyw</code> | keycap | letters | <code>W</code> | W | <code>W</code>, <code>w</code> |
| <code>U+E024</code> | <code>keye</code> | keycap | letters | <code>E</code> | E | <code>E</code>, <code>e</code> |
| <code>U+E025</code> | <code>keyr</code> | keycap | letters | <code>R</code> | R | <code>R</code>, <code>r</code> |
| <code>U+E026</code> | <code>keyt</code> | keycap | letters | <code>T</code> | T | <code>T</code>, <code>t</code> |
| <code>U+E027</code> | <code>keyy</code> | keycap | letters | <code>Y</code> | Y | <code>Y</code>, <code>y</code> |
| <code>U+E028</code> | <code>keyu</code> | keycap | letters | <code>U</code> | U | <code>U</code>, <code>u</code> |
| <code>U+E029</code> | <code>keyi</code> | keycap | letters | <code>I</code> | I | <code>I</code>, <code>i</code> |
| <code>U+E02A</code> | <code>keyo</code> | keycap | letters | <code>O</code> | O | <code>O</code>, <code>o</code> |
| <code>U+E02B</code> | <code>keyp</code> | keycap | letters | <code>P</code> | P | <code>P</code>, <code>p</code> |
| <code>U+E02C</code> | <code>bracketleft</code> | keycap | letters | <code>[</code> | Left Bracket | — |
| <code>U+E02D</code> | <code>bracketright</code> | keycap | letters | <code>]</code> | Right Bracket | — |
| <code>U+E02E</code> | <code>backslash</code> | keycap | letters | <code>\</code> | Backslash | — |
| <code>U+E02F</code> | <code>capslock</code> | keycap | caps | <code>Cap</code> | Caps Lock | — |
| <code>U+E030</code> | <code>keya</code> | keycap | caps | <code>A</code> | A | <code>A</code>, <code>a</code> |
| <code>U+E031</code> | <code>keys</code> | keycap | caps | <code>S</code> | S | <code>S</code>, <code>s</code> |
| <code>U+E032</code> | <code>keyd</code> | keycap | caps | <code>D</code> | D | <code>D</code>, <code>d</code> |
| <code>U+E033</code> | <code>keyf</code> | keycap | caps | <code>F</code> | F | <code>F</code>, <code>f</code> |
| <code>U+E034</code> | <code>keyg</code> | keycap | caps | <code>G</code> | G | <code>G</code>, <code>g</code> |
| <code>U+E035</code> | <code>keyh</code> | keycap | caps | <code>H</code> | H | <code>H</code>, <code>h</code> |
| <code>U+E036</code> | <code>keyj</code> | keycap | caps | <code>J</code> | J | <code>J</code>, <code>j</code> |
| <code>U+E037</code> | <code>keyk</code> | keycap | caps | <code>K</code> | K | <code>K</code>, <code>k</code> |
| <code>U+E038</code> | <code>keyl</code> | keycap | caps | <code>L</code> | L | <code>L</code>, <code>l</code> |
| <code>U+E039</code> | <code>semicolon</code> | keycap | caps | <code>;</code> | Semicolon | — |
| <code>U+E03A</code> | <code>quote</code> | keycap | caps | <code>&#x27;</code> | Apostrophe | — |
| <code>U+E03B</code> | <code>enter</code> | keycap | caps | <code>Enter</code> | Enter | — |
| <code>U+E03C</code> | <code>shift</code> | keycap | shift | <code>Shift</code> | Shift | — |
| <code>U+E03D</code> | <code>keyz</code> | keycap | shift | <code>Z</code> | Z | <code>Z</code>, <code>z</code> |
| <code>U+E03E</code> | <code>keyx</code> | keycap | shift | <code>X</code> | X | <code>X</code>, <code>x</code> |
| <code>U+E03F</code> | <code>keyc</code> | keycap | shift | <code>C</code> | C | <code>C</code>, <code>c</code> |
| <code>U+E040</code> | <code>keyv</code> | keycap | shift | <code>V</code> | V | <code>V</code>, <code>v</code> |
| <code>U+E041</code> | <code>keyb</code> | keycap | shift | <code>B</code> | B | <code>B</code>, <code>b</code> |
| <code>U+E042</code> | <code>keyn</code> | keycap | shift | <code>N</code> | N | <code>N</code>, <code>n</code> |
| <code>U+E043</code> | <code>keym</code> | keycap | shift | <code>M</code> | M | <code>M</code>, <code>m</code> |
| <code>U+E044</code> | <code>comma</code> | keycap | shift | <code>,</code> | Comma | — |
| <code>U+E045</code> | <code>period</code> | keycap | shift | <code>.</code> | Period | — |
| <code>U+E046</code> | <code>slash</code> | keycap | shift | <code>/</code> | Slash | — |
| <code>U+E047</code> | <code>ctrl</code> | keycap | mods | <code>Ctrl</code> | Control | — |
| <code>U+E048</code> | <code>fn</code> | keycap | mods | <code>Fn</code> | Function | — |
| <code>U+E049</code> | <code>win</code> | keycap | mods | <code>Win</code> | Windows | — |
| <code>U+E04A</code> | <code>alt</code> | keycap | mods | <code>Alt</code> | Alt | — |
| <code>U+E04B</code> | <code>space</code> | keycap | mods | <code>Space</code> | Space | — |
| <code>U+E04C</code> | <code>arrowleft</code> | keycap | mods | <code>←</code> | Arrow Left | — |
| <code>U+E04D</code> | <code>arrowup</code> | keycap | mods | <code>↑</code> | Arrow Up | — |
| <code>U+E04E</code> | <code>arrowdown</code> | keycap | mods | <code>↓</code> | Arrow Down | — |
| <code>U+E04F</code> | <code>arrowright</code> | keycap | mods | <code>→</code> | Arrow Right | — |
| <code>U+E050</code> | <code>num</code> | keycap | numpad | <code>Num</code> | Num Lock | — |
| <code>U+E051</code> | <code>asterisk</code> | keycap | numpad | <code>*</code> | Multiply | — |
| <code>U+E052</code> | <code>plus</code> | keycap | numpad | <code>+</code> | Plus | — |
| <code>U+E053</code> | <code>cpu</code> | icon | hardware | <code>CPU</code> | Processor | — |
| <code>U+E054</code> | <code>gpu</code> | icon | hardware | <code>GPU</code> | Graphics processor | — |
| <code>U+E055</code> | <code>ram</code> | icon | hardware | <code>RAM</code> | Memory | — |
| <code>U+E056</code> | <code>rom</code> | icon | hardware | <code>ROM</code> | Hard drive (ROM) | — |
| <code>U+E057</code> | <code>netup</code> | icon | hardware | <code>NetUp</code> | Network uplink | — |
| <code>U+E058</code> | <code>netdown</code> | icon | hardware | <code>NetDown</code> | Network downlink | — |
| <code>U+E059</code> | <code>terminal</code> | icon | software | <code>CLI</code> | Command line | — |
| <code>U+E05A</code> | <code>web</code> | icon | software | <code>Web</code> | Web page | — |
| <code>U+E05B</code> | <code>app</code> | icon | software | <code>App</code> | Application | — |
| <code>U+E05C</code> | <code>game</code> | icon | software | <code>Game</code> | Game | — |
| <code>U+E05D</code> | <code>usb</code> | icon | hardware | <code>USB</code> | USB drive | — |
| <code>U+E05E</code> | <code>volume</code> | icon | hardware | <code>Vol</code> | Volume | — |

### Notes on the glyph names

- `ROM` follows the legend printed on this keyboard, but the drawing is a **hard drive**: platter, spindle and actuator arm. It is not a ROM chip.
- The 12 icons are split into **4 software** (`CLI`, `Web`, `App`, `Game`) and **8 hardware** (`CPU`, `GPU`, `RAM`, `ROM`, `NetUp`, `NetDown`, `USB`, `Vol`).
- Icons are pictograms, have no `event.code`, and are not text.

## 3. ASCII aliases

`A–Z` and `a–z` both render the uppercase keycap of the same letter. `0–9` render the matching digit keycap. The complete table:

| Character | Unicode | Glyph | PUA |
|---|---|---|---|
| <code>0</code> | <code>U+0030</code> | <code>digit0</code> | <code>U+E01D</code> |
| <code>1</code> | <code>U+0031</code> | <code>digit1</code> | <code>U+E014</code> |
| <code>2</code> | <code>U+0032</code> | <code>digit2</code> | <code>U+E015</code> |
| <code>3</code> | <code>U+0033</code> | <code>digit3</code> | <code>U+E016</code> |
| <code>4</code> | <code>U+0034</code> | <code>digit4</code> | <code>U+E017</code> |
| <code>5</code> | <code>U+0035</code> | <code>digit5</code> | <code>U+E018</code> |
| <code>6</code> | <code>U+0036</code> | <code>digit6</code> | <code>U+E019</code> |
| <code>7</code> | <code>U+0037</code> | <code>digit7</code> | <code>U+E01A</code> |
| <code>8</code> | <code>U+0038</code> | <code>digit8</code> | <code>U+E01B</code> |
| <code>9</code> | <code>U+0039</code> | <code>digit9</code> | <code>U+E01C</code> |
| <code>A</code> | <code>U+0041</code> | <code>keya</code> | <code>U+E030</code> |
| <code>B</code> | <code>U+0042</code> | <code>keyb</code> | <code>U+E041</code> |
| <code>C</code> | <code>U+0043</code> | <code>keyc</code> | <code>U+E03F</code> |
| <code>D</code> | <code>U+0044</code> | <code>keyd</code> | <code>U+E032</code> |
| <code>E</code> | <code>U+0045</code> | <code>keye</code> | <code>U+E024</code> |
| <code>F</code> | <code>U+0046</code> | <code>keyf</code> | <code>U+E033</code> |
| <code>G</code> | <code>U+0047</code> | <code>keyg</code> | <code>U+E034</code> |
| <code>H</code> | <code>U+0048</code> | <code>keyh</code> | <code>U+E035</code> |
| <code>I</code> | <code>U+0049</code> | <code>keyi</code> | <code>U+E029</code> |
| <code>J</code> | <code>U+004A</code> | <code>keyj</code> | <code>U+E036</code> |
| <code>K</code> | <code>U+004B</code> | <code>keyk</code> | <code>U+E037</code> |
| <code>L</code> | <code>U+004C</code> | <code>keyl</code> | <code>U+E038</code> |
| <code>M</code> | <code>U+004D</code> | <code>keym</code> | <code>U+E043</code> |
| <code>N</code> | <code>U+004E</code> | <code>keyn</code> | <code>U+E042</code> |
| <code>O</code> | <code>U+004F</code> | <code>keyo</code> | <code>U+E02A</code> |
| <code>P</code> | <code>U+0050</code> | <code>keyp</code> | <code>U+E02B</code> |
| <code>Q</code> | <code>U+0051</code> | <code>keyq</code> | <code>U+E022</code> |
| <code>R</code> | <code>U+0052</code> | <code>keyr</code> | <code>U+E025</code> |
| <code>S</code> | <code>U+0053</code> | <code>keys</code> | <code>U+E031</code> |
| <code>T</code> | <code>U+0054</code> | <code>keyt</code> | <code>U+E026</code> |
| <code>U</code> | <code>U+0055</code> | <code>keyu</code> | <code>U+E028</code> |
| <code>V</code> | <code>U+0056</code> | <code>keyv</code> | <code>U+E040</code> |
| <code>W</code> | <code>U+0057</code> | <code>keyw</code> | <code>U+E023</code> |
| <code>X</code> | <code>U+0058</code> | <code>keyx</code> | <code>U+E03E</code> |
| <code>Y</code> | <code>U+0059</code> | <code>keyy</code> | <code>U+E027</code> |
| <code>Z</code> | <code>U+005A</code> | <code>keyz</code> | <code>U+E03D</code> |
| <code>a</code> | <code>U+0061</code> | <code>keya</code> | <code>U+E030</code> |
| <code>b</code> | <code>U+0062</code> | <code>keyb</code> | <code>U+E041</code> |
| <code>c</code> | <code>U+0063</code> | <code>keyc</code> | <code>U+E03F</code> |
| <code>d</code> | <code>U+0064</code> | <code>keyd</code> | <code>U+E032</code> |
| <code>e</code> | <code>U+0065</code> | <code>keye</code> | <code>U+E024</code> |
| <code>f</code> | <code>U+0066</code> | <code>keyf</code> | <code>U+E033</code> |
| <code>g</code> | <code>U+0067</code> | <code>keyg</code> | <code>U+E034</code> |
| <code>h</code> | <code>U+0068</code> | <code>keyh</code> | <code>U+E035</code> |
| <code>i</code> | <code>U+0069</code> | <code>keyi</code> | <code>U+E029</code> |
| <code>j</code> | <code>U+006A</code> | <code>keyj</code> | <code>U+E036</code> |
| <code>k</code> | <code>U+006B</code> | <code>keyk</code> | <code>U+E037</code> |
| <code>l</code> | <code>U+006C</code> | <code>keyl</code> | <code>U+E038</code> |
| <code>m</code> | <code>U+006D</code> | <code>keym</code> | <code>U+E043</code> |
| <code>n</code> | <code>U+006E</code> | <code>keyn</code> | <code>U+E042</code> |
| <code>o</code> | <code>U+006F</code> | <code>keyo</code> | <code>U+E02A</code> |
| <code>p</code> | <code>U+0070</code> | <code>keyp</code> | <code>U+E02B</code> |
| <code>q</code> | <code>U+0071</code> | <code>keyq</code> | <code>U+E022</code> |
| <code>r</code> | <code>U+0072</code> | <code>keyr</code> | <code>U+E025</code> |
| <code>s</code> | <code>U+0073</code> | <code>keys</code> | <code>U+E031</code> |
| <code>t</code> | <code>U+0074</code> | <code>keyt</code> | <code>U+E026</code> |
| <code>u</code> | <code>U+0075</code> | <code>keyu</code> | <code>U+E028</code> |
| <code>v</code> | <code>U+0076</code> | <code>keyv</code> | <code>U+E040</code> |
| <code>w</code> | <code>U+0077</code> | <code>keyw</code> | <code>U+E023</code> |
| <code>x</code> | <code>U+0078</code> | <code>keyx</code> | <code>U+E03E</code> |
| <code>y</code> | <code>U+0079</code> | <code>keyy</code> | <code>U+E027</code> |
| <code>z</code> | <code>U+007A</code> | <code>keyz</code> | <code>U+E03D</code> |

## 4. `event.code` map

The font itself does not know about keyboard events. Use the mapping below in JavaScript:

```js
const map = await fetch("keycap-tight-mapping.json").then(r => r.json());
const byCode = new Map(map.keys.map(k => [k.code, k]));

document.addEventListener("keydown", (event) => {
  const key = byCode.get(event.code);
  if (!key) return;
  element.textContent = String.fromCodePoint(key.codepoint);
});
```

| `event.code` | Legend | Glyph | PUA | Section |
|---|---|---|---|---|
| <code>Escape</code> | <code>Esc</code> | <code>escape</code> | <code>U+E000</code> | function |
| <code>F1</code> | <code>F1</code> | <code>f1</code> | <code>U+E001</code> | function |
| <code>F2</code> | <code>F2</code> | <code>f2</code> | <code>U+E002</code> | function |
| <code>F3</code> | <code>F3</code> | <code>f3</code> | <code>U+E003</code> | function |
| <code>F4</code> | <code>F4</code> | <code>f4</code> | <code>U+E004</code> | function |
| <code>F5</code> | <code>F5</code> | <code>f5</code> | <code>U+E005</code> | function |
| <code>F6</code> | <code>F6</code> | <code>f6</code> | <code>U+E006</code> | function |
| <code>F7</code> | <code>F7</code> | <code>f7</code> | <code>U+E007</code> | function |
| <code>F8</code> | <code>F8</code> | <code>f8</code> | <code>U+E008</code> | function |
| <code>F9</code> | <code>F9</code> | <code>f9</code> | <code>U+E009</code> | function |
| <code>F10</code> | <code>F10</code> | <code>f10</code> | <code>U+E00A</code> | function |
| <code>F11</code> | <code>F11</code> | <code>f11</code> | <code>U+E00B</code> | function |
| <code>F12</code> | <code>F12</code> | <code>f12</code> | <code>U+E00C</code> | function |
| <code>Insert</code> | <code>Ins</code> | <code>insert</code> | <code>U+E00D</code> | function |
| <code>Delete</code> | <code>Del</code> | <code>delete</code> | <code>U+E00E</code> | function |
| <code>Home</code> | <code>Home</code> | <code>home</code> | <code>U+E00F</code> | function |
| <code>End</code> | <code>End</code> | <code>end</code> | <code>U+E010</code> | function |
| <code>PageUp</code> | <code>PgUp</code> | <code>pageup</code> | <code>U+E011</code> | function |
| <code>PageDown</code> | <code>PgDn</code> | <code>pagedown</code> | <code>U+E012</code> | function |
| <code>Backquote</code> | <code>`</code> | <code>backquote</code> | <code>U+E013</code> | numbers |
| <code>Digit1</code> | <code>1</code> | <code>digit1</code> | <code>U+E014</code> | numbers |
| <code>Digit2</code> | <code>2</code> | <code>digit2</code> | <code>U+E015</code> | numbers |
| <code>Digit3</code> | <code>3</code> | <code>digit3</code> | <code>U+E016</code> | numbers |
| <code>Digit4</code> | <code>4</code> | <code>digit4</code> | <code>U+E017</code> | numbers |
| <code>Digit5</code> | <code>5</code> | <code>digit5</code> | <code>U+E018</code> | numbers |
| <code>Digit6</code> | <code>6</code> | <code>digit6</code> | <code>U+E019</code> | numbers |
| <code>Digit7</code> | <code>7</code> | <code>digit7</code> | <code>U+E01A</code> | numbers |
| <code>Digit8</code> | <code>8</code> | <code>digit8</code> | <code>U+E01B</code> | numbers |
| <code>Digit9</code> | <code>9</code> | <code>digit9</code> | <code>U+E01C</code> | numbers |
| <code>Digit0</code> | <code>0</code> | <code>digit0</code> | <code>U+E01D</code> | numbers |
| <code>Minus</code> | <code>-</code> | <code>minus</code> | <code>U+E01E</code> | numbers |
| <code>Equal</code> | <code>=</code> | <code>equal</code> | <code>U+E01F</code> | numbers |
| <code>Backspace</code> | <code>Back</code> | <code>backspace</code> | <code>U+E020</code> | numbers |
| <code>Tab</code> | <code>Tab</code> | <code>tab</code> | <code>U+E021</code> | letters |
| <code>KeyQ</code> | <code>Q</code> | <code>keyq</code> | <code>U+E022</code> | letters |
| <code>KeyW</code> | <code>W</code> | <code>keyw</code> | <code>U+E023</code> | letters |
| <code>KeyE</code> | <code>E</code> | <code>keye</code> | <code>U+E024</code> | letters |
| <code>KeyR</code> | <code>R</code> | <code>keyr</code> | <code>U+E025</code> | letters |
| <code>KeyT</code> | <code>T</code> | <code>keyt</code> | <code>U+E026</code> | letters |
| <code>KeyY</code> | <code>Y</code> | <code>keyy</code> | <code>U+E027</code> | letters |
| <code>KeyU</code> | <code>U</code> | <code>keyu</code> | <code>U+E028</code> | letters |
| <code>KeyI</code> | <code>I</code> | <code>keyi</code> | <code>U+E029</code> | letters |
| <code>KeyO</code> | <code>O</code> | <code>keyo</code> | <code>U+E02A</code> | letters |
| <code>KeyP</code> | <code>P</code> | <code>keyp</code> | <code>U+E02B</code> | letters |
| <code>BracketLeft</code> | <code>[</code> | <code>bracketleft</code> | <code>U+E02C</code> | letters |
| <code>BracketRight</code> | <code>]</code> | <code>bracketright</code> | <code>U+E02D</code> | letters |
| <code>Backslash</code> | <code>\</code> | <code>backslash</code> | <code>U+E02E</code> | letters |
| <code>CapsLock</code> | <code>Cap</code> | <code>capslock</code> | <code>U+E02F</code> | caps |
| <code>KeyA</code> | <code>A</code> | <code>keya</code> | <code>U+E030</code> | caps |
| <code>KeyS</code> | <code>S</code> | <code>keys</code> | <code>U+E031</code> | caps |
| <code>KeyD</code> | <code>D</code> | <code>keyd</code> | <code>U+E032</code> | caps |
| <code>KeyF</code> | <code>F</code> | <code>keyf</code> | <code>U+E033</code> | caps |
| <code>KeyG</code> | <code>G</code> | <code>keyg</code> | <code>U+E034</code> | caps |
| <code>KeyH</code> | <code>H</code> | <code>keyh</code> | <code>U+E035</code> | caps |
| <code>KeyJ</code> | <code>J</code> | <code>keyj</code> | <code>U+E036</code> | caps |
| <code>KeyK</code> | <code>K</code> | <code>keyk</code> | <code>U+E037</code> | caps |
| <code>KeyL</code> | <code>L</code> | <code>keyl</code> | <code>U+E038</code> | caps |
| <code>Semicolon</code> | <code>;</code> | <code>semicolon</code> | <code>U+E039</code> | caps |
| <code>Quote</code> | <code>&#x27;</code> | <code>quote</code> | <code>U+E03A</code> | caps |
| <code>Enter</code> | <code>Enter</code> | <code>enter</code> | <code>U+E03B</code> | caps |
| <code>ShiftLeft</code> | <code>Shift</code> | <code>shift</code> | <code>U+E03C</code> | shift |
| <code>KeyZ</code> | <code>Z</code> | <code>keyz</code> | <code>U+E03D</code> | shift |
| <code>KeyX</code> | <code>X</code> | <code>keyx</code> | <code>U+E03E</code> | shift |
| <code>KeyC</code> | <code>C</code> | <code>keyc</code> | <code>U+E03F</code> | shift |
| <code>KeyV</code> | <code>V</code> | <code>keyv</code> | <code>U+E040</code> | shift |
| <code>KeyB</code> | <code>B</code> | <code>keyb</code> | <code>U+E041</code> | shift |
| <code>KeyN</code> | <code>N</code> | <code>keyn</code> | <code>U+E042</code> | shift |
| <code>KeyM</code> | <code>M</code> | <code>keym</code> | <code>U+E043</code> | shift |
| <code>Comma</code> | <code>,</code> | <code>comma</code> | <code>U+E044</code> | shift |
| <code>Period</code> | <code>.</code> | <code>period</code> | <code>U+E045</code> | shift |
| <code>Slash</code> | <code>/</code> | <code>slash</code> | <code>U+E046</code> | shift |
| <code>ShiftRight</code> | <code>Shift</code> | <code>shift</code> | <code>U+E03C</code> | shift |
| <code>ControlLeft</code> | <code>Ctrl</code> | <code>ctrl</code> | <code>U+E047</code> | mods |
| <code>FnLeft</code> | <code>Fn</code> | <code>fn</code> | <code>U+E048</code> | mods |
| <code>MetaLeft</code> | <code>Win</code> | <code>win</code> | <code>U+E049</code> | mods |
| <code>AltLeft</code> | <code>Alt</code> | <code>alt</code> | <code>U+E04A</code> | mods |
| <code>Space</code> | <code>Space</code> | <code>space</code> | <code>U+E04B</code> | mods |
| <code>AltRight</code> | <code>Alt</code> | <code>alt</code> | <code>U+E04A</code> | mods |
| <code>FnRight</code> | <code>Fn</code> | <code>fn</code> | <code>U+E048</code> | mods |
| <code>ControlRight</code> | <code>Ctrl</code> | <code>ctrl</code> | <code>U+E047</code> | mods |
| <code>ArrowLeft</code> | <code>←</code> | <code>arrowleft</code> | <code>U+E04C</code> | mods |
| <code>ArrowUp</code> | <code>↑</code> | <code>arrowup</code> | <code>U+E04D</code> | mods |
| <code>ArrowDown</code> | <code>↓</code> | <code>arrowdown</code> | <code>U+E04E</code> | mods |
| <code>ArrowRight</code> | <code>→</code> | <code>arrowright</code> | <code>U+E04F</code> | mods |
| <code>NumLock</code> | <code>Num</code> | <code>num</code> | <code>U+E050</code> | numpad |
| <code>NumpadDivide</code> | <code>/</code> | <code>slash</code> | <code>U+E046</code> | numpad |
| <code>NumpadMultiply</code> | <code>*</code> | <code>asterisk</code> | <code>U+E051</code> | numpad |
| <code>NumpadSubtract</code> | <code>-</code> | <code>minus</code> | <code>U+E01E</code> | numpad |
| <code>Numpad7</code> | <code>7</code> | <code>digit7</code> | <code>U+E01A</code> | numpad |
| <code>Numpad8</code> | <code>8</code> | <code>digit8</code> | <code>U+E01B</code> | numpad |
| <code>Numpad9</code> | <code>9</code> | <code>digit9</code> | <code>U+E01C</code> | numpad |
| <code>NumpadAdd</code> | <code>+</code> | <code>plus</code> | <code>U+E052</code> | numpad |
| <code>Numpad4</code> | <code>4</code> | <code>digit4</code> | <code>U+E017</code> | numpad |
| <code>Numpad5</code> | <code>5</code> | <code>digit5</code> | <code>U+E018</code> | numpad |
| <code>Numpad6</code> | <code>6</code> | <code>digit6</code> | <code>U+E019</code> | numpad |
| <code>Numpad1</code> | <code>1</code> | <code>digit1</code> | <code>U+E014</code> | numpad |
| <code>Numpad2</code> | <code>2</code> | <code>digit2</code> | <code>U+E015</code> | numpad |
| <code>Numpad3</code> | <code>3</code> | <code>digit3</code> | <code>U+E016</code> | numpad |
| <code>NumpadEnter</code> | <code>Enter</code> | <code>enter</code> | <code>U+E03B</code> | numpad |
| <code>Numpad0</code> | <code>0</code> | <code>digit0</code> | <code>U+E01D</code> | numpad |
| <code>NumpadDecimal</code> | <code>.</code> | <code>period</code> | <code>U+E045</code> | numpad |

Duplicate physical keys share one glyph, but every `event.code` is listed. Examples: `ShiftLeft` and `ShiftRight` both use `shift`; `Digit7` and `Numpad7` both use `digit7`.

## 5. Machine-readable mapping files

These files are attached to the GitHub release:

| File | Contents |
|---|---|
| `keycap-tight-mapping.json` | Complete JSON: metadata, 83 keycaps, 12 icons, 101 keys, 62 text aliases |
| `keycap-tight-keymap.csv` | 101 rows of `event.code` → glyph/PUA |
| `keycap-tight-text-map.csv` | 62 ASCII aliases → glyph/PUA |
| `keycap-tight-icons.csv` | 12 icons with software/hardware category |

## 6. Font facts

- Family: **Keycap Tight**, style **Regular**, version **1.400**.
- Units per em: **1000**; every glyph occupies a **1em / 62-unit** display slot.
- Keycap frames are exactly 1000 font units tall; every standalone SVG is 62 units high.
- Transparent interior; one color via `color` / `currentColor`.
- Outlines are derived from Noto Sans SemiBold and JetBrains Mono SemiBold under SIL OFL 1.1. See `OFL.txt` and `OFL-JetBrainsMono.txt`.

