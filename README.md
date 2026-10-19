# ReiKeycap

[中文](#中文) · [English](#english)

## 中文

**透明、贴合内容的键帽与系统图标字体。** 依据实拍 Windows 键盘重绘，适合快捷键提示、键位图和键帽展示。

- **版本：** 1.4.0
- **字体族：** ReiKeycap Regular
- **格式：** TTF + WOFF2
- **字形：** 83 个键帽 + 12 个图标 = 95 个
- **映射：** 101 个 `event.code`，62 个 ASCII 别名
- **许可：** SIL Open Font License 1.1
- **作者：** Rei Xinglan（[@CRITTIof](https://github.com/CRITTIof)）

## 仓库结构

```text
rei-keycap-font/
├─ demo.html                     实时键盘演示
├─ fonts/
│  ├─ ReiKeycap-Regular.ttf      桌面字体
│  └─ ReiKeycap-Regular.woff2    Web 字体
├─ MAPPING.md                    完整映射文档（中文）
├─ README.md
├─ src/
│  ├─ build_font.py              构建入口
│  ├─ data.py                    键位与图标分类
│  └─ geometry.py                字形轮廓与几何
├─ assets/                       两个 OFL 源字体
├─ requirements.txt
└─ OFL.txt                       完整许可与源字体版权
```

生成图片、逐字形 SVG、预览 PNG 和 ZIP 不进入仓库。

## 下载与安装

从 **[Releases](https://github.com/CRITTIof/rei-keycap-font/releases/latest)** 下载最新字体。

- **Windows：** 双击 `ReiKeycap-Regular.ttf`，选择“安装”。
- **macOS：** 用“字体册”打开 TTF，选择“安装字体”。
- **Web：**

```css
@font-face {
  font-family: "ReiKeycap";
  src: url("fonts/ReiKeycap-Regular.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: block;
}

.key {
  font: 400 38px/1 "ReiKeycap";
  color: currentColor;
}
```

`font-size` 就是键帽的视觉高度。使用 `line-height: 1`，颜色由 `color` / `currentColor` 控制，内部透明。

## 使用

用 PUA 码位精确取字形：

```html
<span class="key">&#xE000;</span>  <!-- Esc -->
<span class="key">&#xE053;</span>  <!-- CPU -->
<span class="key">&#xE059;</span>  <!-- CLI -->
```

字母和数字也可直接输入：

```html
<span class="key">A</span>
<span class="key">a</span>
<span class="key">7</span>
```

`A` 和 `a` 都显示大写 A 键帽。

> **注意：** ASCII 字母和数字被有意映射为键帽，不要把本字体用于正文。正文请使用普通文本字体。

## 映射

完整码位、ASCII 别名和 101 个 `event.code` 见 **[MAPPING.md](MAPPING.md)**。

| 范围 | 内容 |
|---|---|
| `U+E000–U+E052` | 83 个键帽 |
| `U+E053–U+E05E` | 12 个系统图标 |
| `A–Z`、`a–z`、`0–9` | 键帽的 ASCII 别名 |

字体本身不处理键盘事件。把 `event.code` 映射到码位，再渲染：

```js
document.addEventListener("keydown", (event) => {
  const key = KEYS.find((item) => item.code === event.code);
  if (key) output.textContent = String.fromCodePoint(key.codepoint);
});
```

`demo.html` 中的 `KEYS` 数组已经包含全部 101 条映射，可直接复制使用。

## 从源码构建

需要 Python 3.10+，并安装 `requirements.txt` 中的 `fonttools` 和 `brotli`。

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
python src/build_font.py
```

输出：

```text
fonts/ReiKeycap-Regular.ttf
fonts/ReiKeycap-Regular.woff2
```

构建不依赖 Node.js、浏览器、图像库或网络。

## 设计

- 1000 units/em；所有字形都占满 **1em** 高度。
- 键帽边框高 62 设计单位，外圆角 16，描边 4，内部透明。
- 字母和数字使用 JetBrains Mono SemiBold，统一为 65.2 单位宽的键帽。
- 多字符图例（`Esc`、`Tab`、`Ctrl`、`F1` 等）使用 Noto Sans SemiBold，宽度贴合内容。
- 图标位于 62 × 62 设计框内，描边 3.5，无键帽边框。
- 单色轮廓字体，颜色来自 `currentColor`。

## 许可

字形轮廓来自：

- **Noto Sans SemiBold** — Copyright 2018 The Noto Project Authors
- **JetBrains Mono SemiBold** — Copyright 2020 The JetBrains Mono Project Authors

两者均以 **SIL Open Font License 1.1** 使用和再分发。完整许可与版权声明见 [OFL.txt](OFL.txt)。生成的字体命名为 **ReiKeycap**，未使用任何源字体的保留名称。

---

## English

[中文](#中文) · [English](#english)

**A transparent, content-fitted keycap and system-icon font**, redrawn from a photographed Windows keyboard.

- **Version:** 1.4.0 · **Family:** ReiKeycap Regular · **Formats:** TTF + WOFF2
- **95 glyphs:** 83 keycaps + 12 icons
- **101** `event.code` mappings · **62** ASCII aliases
- **License:** SIL Open Font License 1.1 · **Author:** Rei Xinglan ([@CRITTIof](https://github.com/CRITTIof))

### Install

Download the latest fonts from **[Releases](https://github.com/CRITTIof/rei-keycap-font/releases/latest)**.

- **Windows:** open `ReiKeycap-Regular.ttf` and choose **Install**.
- **macOS:** open the TTF in **Font Book** and choose **Install Font**.
- **Web:**

```css
@font-face {
  font-family: "ReiKeycap";
  src: url("fonts/ReiKeycap-Regular.woff2") format("woff2");
}
.key { font: 400 38px/1 "ReiKeycap"; color: currentColor; }
```

### Use

```html
<span class="key">&#xE000;</span>  <!-- Esc -->
<span class="key">&#xE053;</span>  <!-- CPU -->
<span class="key">A</span>         <!-- A keycap -->
```

Use PUA codepoints for exact glyphs. ASCII `A–Z`, `a–z`, `0–9` are aliases for the matching keycaps. **Do not use this font for body text.**

See **[MAPPING.md](MAPPING.md)** for all PUA codepoints, ASCII aliases, and 101 `event.code` mappings. The `KEYS` array in [demo.html](demo.html) is a ready-to-copy JavaScript map.

### Build

```bash
pip install -r requirements.txt
python src/build_font.py
```

Outputs `fonts/ReiKeycap-Regular.ttf` and `.woff2`. Python 3.10+ only; no Node.js or image tooling required.

### Design and license

Every glyph occupies a **1em** slot at **1000 units/em**. Keycap frames are 62 design units high with a 4-unit stroke and a transparent interior; icons use a 62 × 62 box with a 3.5-unit stroke. Letters and digits use JetBrains Mono SemiBold; other legends use Noto Sans SemiBold.

Outlines are derived from **Noto Sans SemiBold** (Copyright 2018 The Noto Project Authors) and **JetBrains Mono SemiBold** (Copyright 2020 The JetBrains Mono Project Authors), both under the **SIL Open Font License 1.1**. See [OFL.txt](OFL.txt) for the full license and copyright notices. The generated font is named **ReiKeycap** and uses no reserved name from either source font.
