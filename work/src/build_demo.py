import html
import json
from pathlib import Path

import geometry as G
from data import UNIQUE, PHYS

DIST = G.OUT
KEYS = json.loads((DIST / "keycap-tight-mapping.json").read_text(encoding="utf-8"))

SECTIONS = [
    ("01", "Function & navigation", "function", ["escape", *[f"f{i}" for i in range(1, 13)], "insert", "delete", "home", "end", "pageup", "pagedown"]),
    ("02", "Number row", "numbers", ["backquote", *[f"digit{i}" for i in range(1, 10)], "digit0", "minus", "equal", "backspace"]),
    ("03", "Tabs, letters & punctuation", "letters", ["tab", *[f"key{c}" for c in "qwertyuiop"], "bracketleft", "bracketright", "backslash", "capslock", *[f"key{c}" for c in "asdfghjkl"], "semicolon", "quote", "enter", "shift", *[f"key{c}" for c in "zxcvbnm"], "comma", "period", "slash"]),
    ("04", "Modifiers & arrows", "mods", ["ctrl", "fn", "win", "alt", "space", "arrowleft", "arrowup", "arrowdown", "arrowright"]),
    ("05", "Numpad-only glyphs", "numpad", ["num", "asterisk", "plus"]),
]

shared = {}
for code, label, gid, full, section in PHYS:
    shared.setdefault(gid, []).append(code)

seen = set()
sections_html = []
for num, title, group, ids in SECTIONS:
    buttons = []
    for gid in ids:
        if gid in seen:
            raise RuntimeError(f"duplicate in demo sections: {gid}")
        seen.add(gid)
        meta = G.META[gid]
        codes = " ".join(shared[gid])
        buttons.append(
            f'<button class="cap" type="button" data-glyph="{gid}" data-codes="{html.escape(codes)}" '
            f'aria-label="{html.escape(meta["label"])} — {html.escape(meta["full"])}" '
            f'title="{html.escape(meta["label"])} — {html.escape(meta["full"])} · &#x{meta["pua"]:04X}">'
            f'<span class="cap-glyph" aria-hidden="true">&#x{meta["pua"]:04X};</span></button>'
        )
    sections_html.append(f'''<section class="group">
  <div class="group-head"><span>{num} / {html.escape(title.upper())}</span><span>{len(ids)}</span></div>
  <div class="caps">{''.join(buttons)}</div>
</section>''')
assert seen == {g[0] for g in UNIQUE}, (len(seen), len(UNIQUE))

buttons_js = json.dumps([
    {"code": k["code"], "label": k["label"], "full": k["full"], "glyph": k["glyph"],
     "pua": k["pua"], "codepoint": k["codepoint"]}
    for k in KEYS["keys"]
], ensure_ascii=False)

html_doc = f'''<!doctype html>
<html lang="zh-CN" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Keycap Tight — Live Input Demo</title>
<style>
@font-face {{
  font-family: 'Keycap Tight';
  src: url('KeycapTight-Regular.woff2') format('woff2'),
       url('KeycapTight-Regular.ttf') format('truetype');
  font-weight: 400;
  font-style: normal;
  font-display: block;
}}
:root {{
  --bg: #14171c;
  --bg-2: #191d24;
  --panel: #1c2027;
  --panel-2: #222731;
  --ink: #f4f1ea;
  --muted: #8c939e;
  --line: #303641;
  --accent: #ffb454;
  --accent-2: #e4572e;
  --ui: "Segoe UI", "Noto Sans", "Microsoft YaHei UI", "Microsoft YaHei", sans-serif;
  --cap-size: 38px;
  --shadow: 0 28px 80px rgba(0,0,0,.42);
}}
html[data-theme="light"] {{
  --bg: #ebe7de;
  --bg-2: #f3f0e9;
  --panel: #f7f5f0;
  --panel-2: #fffdf8;
  --ink: #20242a;
  --muted: #77736b;
  --line: #d8d2c7;
  --accent: #c35a12;
  --accent-2: #a33d0b;
  --shadow: 0 28px 80px rgba(50,42,30,.16);
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; min-height: 100%; }}
body {{
  font-family: var(--ui);
  background:
    radial-gradient(1200px 600px at 18% -10%, color-mix(in srgb, var(--accent) 9%, transparent), transparent 62%),
    radial-gradient(1000px 600px at 100% 22%, color-mix(in srgb, var(--accent-2) 7%, transparent), transparent 60%),
    var(--bg);
  color: var(--ink);
  -webkit-font-smoothing: antialiased;
}}
.wrap {{ width: min(1240px, calc(100% - 48px)); margin: 0 auto; padding: 42px 0 64px; }}
header {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 24px; margin-bottom: 28px; }}
h1 {{ margin: 0; font-size: 24px; letter-spacing: .16em; font-weight: 650; }}
.sub {{ margin: 9px 0 0; color: var(--muted); font-size: 12px; letter-spacing: .08em; line-height: 1.7; }}
.sub b {{ color: var(--ink); font-weight: 600; }}
.theme {{
  border: 1px solid var(--line); background: var(--panel); color: var(--ink);
  padding: 9px 14px; border-radius: 999px; cursor: pointer; font: 600 12px/1 var(--ui);
  letter-spacing: .08em; white-space: nowrap;
}}
.theme:hover {{ border-color: var(--accent); color: var(--accent); }}
.hud {{
  display: grid; grid-template-columns: minmax(220px, 330px) 1fr; gap: 30px; align-items: center;
  background: linear-gradient(145deg, var(--panel-2), var(--panel));
  border: 1px solid var(--line); border-radius: 24px; padding: 26px 30px;
  box-shadow: var(--shadow); min-height: 212px;
}}
.hud-visual {{ min-width: 0; display: flex; align-items: center; justify-content: center; }}
.hud-glyph {{
  font-family: 'Keycap Tight'; font-size: clamp(76px, 7.6vw, 104px); line-height: 1; color: var(--accent);
  display: block; max-width: 100%; transition: color .12s;
}}
.hud-placeholder {{
  width: 148px; height: 148px; border: 1px dashed var(--line); border-radius: 26px;
  display: grid; place-items: center; color: var(--muted); font-size: 11px; letter-spacing: .14em;
  text-align: center; line-height: 1.6;
}}
.hud.has-key .hud-placeholder {{ display: none; }}
.hud-meta {{ min-width: 0; }}
.kicker {{ font-size: 10px; letter-spacing: .3em; color: var(--muted); text-transform: uppercase; margin-bottom: 10px; }}
.last-label {{ font-size: clamp(24px, 4vw, 38px); font-weight: 650; letter-spacing: -.02em; }}
.last-full {{ margin-top: 6px; color: var(--muted); font-size: 13px; line-height: 1.6; word-break: break-word; }}
.last-code {{ margin-top: 16px; display: inline-flex; gap: 8px; align-items: center; font: 600 11px/1 ui-monospace, Consolas, monospace; color: var(--accent); background: color-mix(in srgb, var(--accent) 10%, transparent); border: 1px solid color-mix(in srgb, var(--accent) 32%, transparent); border-radius: 999px; padding: 7px 10px; }}
.history {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 18px; min-height: 28px; }}
.hist {{
  display: inline-flex; align-items: center; gap: 6px; border: 1px solid var(--line);
  background: color-mix(in srgb, var(--panel-2) 72%, transparent); border-radius: 8px; padding: 3px 7px;
  color: var(--muted); font: 500 10px/1 ui-monospace, Consolas, monospace;
}}
.hist-glyph {{ font-family: 'Keycap Tight'; font-size: 18px; line-height: 1; color: var(--ink); }}
.panel {{
  margin-top: 26px; background: var(--panel); border: 1px solid var(--line);
  border-radius: 24px; padding: 22px 26px 28px; box-shadow: var(--shadow);
}}
.panel-head {{ display: flex; align-items: center; justify-content: space-between; gap: 18px; margin-bottom: 16px; }}
.panel-title {{ font-size: 11px; letter-spacing: .24em; color: var(--muted); text-transform: uppercase; }}
.controls {{ display: flex; align-items: center; gap: 12px; color: var(--muted); font-size: 11px; }}
input[type=range] {{ accent-color: var(--accent); width: 128px; }}
.group {{ margin-top: 22px; }}
.group:first-of-type {{ margin-top: 2px; }}
.group-head {{ display: flex; justify-content: space-between; gap: 16px; border-bottom: 1px solid var(--line); padding-bottom: 8px; color: var(--muted); font-size: 10px; font-weight: 600; letter-spacing: .18em; }}
.caps {{ display: flex; flex-wrap: wrap; align-items: center; gap: 14px 15px; padding-top: 16px; }}
.cap {{
  appearance: none; border: 0; background: transparent; padding: 0; margin: 0; color: var(--ink);
  font-family: 'Keycap Tight'; font-size: var(--cap-size); line-height: 1; cursor: pointer;
  display: inline-flex; align-items: center; justify-content: center; height: var(--cap-size);
  transition: color .12s ease, transform .08s ease;
  -webkit-tap-highlight-color: transparent;
}}
.cap-glyph {{ display: block; line-height: 1; }}
.cap:hover {{ color: var(--accent); }}
.cap.is-down {{ color: var(--accent); transform: translateY(2px) scale(.97); }}
.notes {{ display: grid; grid-template-columns: 1.1fr .9fr; gap: 22px; margin-top: 26px; }}
.note {{ background: var(--bg-2); border: 1px solid var(--line); border-radius: 18px; padding: 18px 20px; color: var(--muted); font-size: 12px; line-height: 1.8; }}
.note strong {{ color: var(--ink); }}
.note ul {{ margin: 10px 0 0; padding-left: 18px; }}
.note li {{ margin: 5px 0; }}
code {{ font-family: ui-monospace, Consolas, monospace; font-size: .92em; color: var(--accent); }}
pre {{ margin: 10px 0 0; padding: 14px; overflow: auto; background: var(--panel); border: 1px solid var(--line); border-radius: 12px; color: var(--ink); font: 11px/1.65 ui-monospace, Consolas, monospace; }}
@media (max-width: 760px) {{
  .wrap {{ width: calc(100% - 28px); padding-top: 24px; }}
  header {{ align-items: flex-start; }}
  .hud {{ grid-template-columns: 1fr; gap: 18px; padding: 22px; }}
  .hud-visual {{ justify-content: flex-start; }}
  .hud-glyph {{ font-size: 92px; }}
  .notes {{ grid-template-columns: 1fr; }}
  .cap {{ --cap-size: 32px !important; }}
}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div>
      <h1>KEYCAP TIGHT</h1>
      <p class="sub"><b>83</b> keycaps + <b>12</b> system icons · <b>101</b> physical Windows keycodes · transparent outline<br>按任意键测试；数字小键盘、左右 Shift/Ctrl/Alt 会映射到同一个字形。</p>
    </div>
    <button class="theme" id="theme" type="button">LIGHT</button>
  </header>

  <section class="hud" id="hud">
    <div class="hud-visual">
      <div class="hud-placeholder" id="placeholder">PRESS<br>ANY KEY</div>
      <span class="hud-glyph" id="lastGlyph" aria-hidden="true"></span>
    </div>
    <div class="hud-meta">
      <div class="kicker">LAST INPUT</div>
      <div class="last-label" id="lastLabel">等待输入</div>
      <div class="last-full" id="lastFull">按下键盘上的任意键，或点击下方键帽。</div>
      <div class="last-code" id="lastCode">event.code —</div>
      <div class="history" id="history"></div>
    </div>
  </section>

  <section class="panel">
    <div class="panel-head">
      <div class="panel-title">83 KEYCAPS / 101 KEYCODES · +12 SYSTEM ICONS</div>
      <div class="controls"><label for="size">SIZE</label><input id="size" type="range" min="26" max="64" value="38" step="1"><span id="sizeLabel">38</span></div>
    </div>
{''.join(sections_html)}
  </section>

  <section class="notes">
    <div class="note">
      <strong>Usage</strong>
      <ul>
        <li><code>font-size</code> equals the visual key height; use <code>line-height: 1</code>.</li>
        <li>Interior is transparent. Color the whole glyph with <code>color</code> / <code>currentColor</code>.</li>
        <li>Use <code>keycap-tight-mapping.json</code> to map <code>event.code</code> to a PUA codepoint.</li>
        <li>Normal text <code>A-Z</code> / <code>a-z</code> / <code>0-9</code> render the matching keycap glyph directly.</li>
        <li>Letter and digit keycaps use a monospaced face, so every one has the same width.</li>
        <li>12 transparent icons: 4 software, 8 hardware (U+E053–U+E05E).</li>
        <li>Fn usually emits no browser key event; treat it as a custom/visual key.</li>
      </ul>
    </div>
    <div class="note">
      <strong>Font</strong>
      <pre>@font-face {{
  font-family: 'Keycap Tight';
  src: url('KeycapTight-Regular.woff2') format('woff2');
}}
.key {{
  font: 400 38px/1 'Keycap Tight';
  color: #20242A;
}}
&lt;span class="key"&gt;&amp;#xE000;&lt;/span&gt;</pre>
    </div>
  </section>
</div>
<script>
const KEYS = {buttons_js};
const BY_CODE = new Map(KEYS.map(k => [k.code, k]));
const capNodes = [...document.querySelectorAll('.cap')];
const lastGlyph = document.getElementById('lastGlyph');
const lastLabel = document.getElementById('lastLabel');
const lastFull = document.getElementById('lastFull');
const lastCode = document.getElementById('lastCode');
const hud = document.getElementById('hud');
const history = document.getElementById('history');
let historyItems = [];

function setGlyphDown(glyph, down) {{
  capNodes.filter(el => el.dataset.glyph === glyph).forEach(el => el.classList.toggle('is-down', down));
}}
function clearDown() {{
  capNodes.forEach(el => el.classList.remove('is-down'));
}}
function showKey(k) {{
  hud.classList.add('has-key');
  lastGlyph.textContent = String.fromCodePoint(k.codepoint);
  lastLabel.textContent = k.label;
  lastFull.textContent = k.full + ' · ' + k.pua;
  lastCode.textContent = 'event.code ' + k.code;
  historyItems.unshift(k);
  historyItems = historyItems.slice(0, 12);
  history.innerHTML = historyItems.map(item =>
    '<span class="hist"><span class="hist-glyph">' + String.fromCodePoint(item.codepoint) + '</span>' + item.code + '</span>'
  ).join('');
}}
function pressFromElement(el) {{
  const codes = el.dataset.codes.split(' ');
  const k = BY_CODE.get(codes[0]);
  if (!k) return;
  setGlyphDown(k.glyph, true);
  showKey(k);
  setTimeout(() => setGlyphDown(k.glyph, false), 120);
}}
capNodes.forEach(el => {{
  el.addEventListener('pointerdown', e => {{ e.preventDefault(); pressFromElement(el); }});
  el.addEventListener('click', e => {{ e.preventDefault(); }});
}});
document.addEventListener('keydown', e => {{
  const k = BY_CODE.get(e.code);
  if (!k) return;
  e.preventDefault();
  setGlyphDown(k.glyph, true);
  if (!e.repeat) showKey(k);
}});
document.addEventListener('keyup', e => {{
  const k = BY_CODE.get(e.code);
  if (k) setGlyphDown(k.glyph, false);
}});
window.addEventListener('blur', clearDown);
const theme = document.getElementById('theme');
theme.addEventListener('click', () => {{
  const root = document.documentElement;
  const light = root.dataset.theme === 'light';
  root.dataset.theme = light ? 'dark' : 'light';
  theme.textContent = light ? 'LIGHT' : 'DARK';
}});
const size = document.getElementById('size');
const sizeLabel = document.getElementById('sizeLabel');
size.addEventListener('input', () => {{
  document.documentElement.style.setProperty('--cap-size', size.value + 'px');
  sizeLabel.textContent = size.value;
}});
const params = new URLSearchParams(location.search);
if (params.get('theme') === 'light') {{
  document.documentElement.dataset.theme = 'light';
  theme.textContent = 'DARK';
}}
const demoKey = params.get('key');
if (demoKey && BY_CODE.has(demoKey)) showKey(BY_CODE.get(demoKey));
</script>
</body>
</html>
'''
(DIST / "demo.html").write_text(html_doc, encoding="utf-8")
print(DIST / "demo.html", len(html_doc))
