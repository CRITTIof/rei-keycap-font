# Keycap Tight / Windows + System Icons

透明、内容贴合的键帽图标集，按照片这把键盘整理为 **Windows 主标注**。  
共 **101 个物理键位**，去重后 **83 个独立键帽字形**；另外加入 **12 个系统线条图标**（4 软件 + 8 硬件），合计 **95 个字形**。数字小键盘、左右修饰键等重复键共享同一个字形。

字母与数字键帽使用 **JetBrains Mono SemiBold** 等宽字体，所有 A-Z、0-9 键帽宽度一致。普通文字里的 **A-Z / a-z / 0-9** 也已映射到对应键帽。

当前版本：**1.4.0**（等宽字母/数字；放大 APP 并开口避让；调整 USB、音量、ROM、GPU、RAM；目录与文件名全部改为英文）。

![总览](keycap-tight-specimen.png)

![系统图标](keycap-tight-icons.png)

![实时 Demo](demo-preview.png)

## 目录

```text
KeycapTight/
├─ work/          源码、字体素材、依赖、构建脚本
└─ dist/          字体、SVG、映射、Demo、预览和 ZIP
   ├─ glyphs/
   │  ├─ U+E000_Esc/
   │  │  ├─ keycap.svg
   │  │  ├─ preview.png
   │  │  └─ glyph.json
   │  ├─ U+E053_CPU/
   │  │  ├─ icon.svg
   │  │  ├─ preview.png
   │  │  └─ glyph.json
   │  ├─ U+E059_CLI/
   │  │  ├─ icon.svg
   │  │  ├─ preview.png
   │  │  └─ glyph.json
   │  └─ ...（共 95 个字形文件夹）
   └─ ...
```

**每个字符/图标一个独立文件夹**，文件夹名使用 `U+码位_标签`，避开了 `\ / * ? " < > |` 等 Windows 非法文件名字符；原始标签、全名、宽度和全部 keycode 都写在同目录的 `glyph.json` 里。`glyphs/index.csv` 是 95 个字形的总索引。

## 成品文件

| 文件 | 用途 |
|---|---|
| `glyphs/U+E000_Esc/keycap.svg` | 单字符键帽 SVG，共 83 个 |
| `glyphs/U+E053_CPU/icon.svg` | 单字符系统图标 SVG，共 12 个 |
| `glyphs/index.csv` | 95 个字形的 PUA、类型、标签、宽度、文件夹索引 |
| `KeycapTight-Regular.woff2` | Web 字体，主推荐 |
| `KeycapTight-Regular.ttf` | 桌面 / 其他环境字体 |
| `keycap-tight.css` | `@font-face` + 基础 `.keycap-tight` 样式 |
| `keycap-tight-sprite.svg` | 95 个 `<symbol>`，透明，可用 `currentColor` 换色 |
| `keycap-tight-mapping.json` | 101 个 keycode、12 个图标、62 个文字别名的完整映射 |
| `keycap-tight-keymap.csv` | 101 个 keycode 映射的表格版 |
| `keycap-tight-glyphs.csv` | 83 个键帽字形的 PUA、文字别名、宽度、关联 keycode |
| `keycap-tight-icons.csv` | 12 个系统图标的分类、PUA、宽度、文件夹 |
| `keycap-tight-software-icons.csv` | 4 个软件图标 |
| `keycap-tight-hardware-icons.csv` | 8 个硬件图标 |
| `keycap-tight-text-map.csv` | 62 个 ASCII 字母/数字 → 键帽字形映射 |
| `demo.html` | 实时按键高亮 Demo，支持深浅色 |
| `keycap-tight-specimen.svg / .png` | 95 个字形总览 |
| `keycap-tight-icons.svg / .png` | 12 个系统图标总览，按软件/硬件分组 |
| `font-proof-light.png / font-proof-dark.png` | 字体明暗背景渲染检查 |
| `OFL.txt` | Noto Sans SemiBold 的 SIL OFL 1.1 |
| `OFL-JetBrainsMono.txt` | JetBrains Mono SemiBold 的 SIL OFL 1.1 |
| `KeycapTight-Windows.zip` | 上述成品的完整打包 |

## 设计规格

- 键帽外框高 **62**，圆角 **16**，描边 **4**，内部 **不填色**。
- 宽度 = 字符 advance 宽度 + 左右各 **20**；所有框统一高度，字符按实际墨迹垂直居中。
- **所有字形使用同一个高度槽**：键帽外框精确为 **62**，12 个图标全部位于 **62 × 62** 框内；字体中对应 **1000 / em**，因此同一 `font-size` 下所有字符的显示高度一致。
- 单字母与数字统一使用 **JetBrains Mono SemiBold**，字号 **42**，每个键帽内容宽 **25.2**，外框宽统一为 **65.2**。
- 其他标签（Esc、Tab、Ctrl、F1 等）继续使用 **Noto Sans SemiBold**，按实际内容贴合。
- 系统图标使用 **62 × 62** 设计框，以 **3.5** 为重线宽（比键帽描边略细），不加键帽边框、不填背景，用图形表达含义而不是写 `CPU`/`RAM` 等文字。
- 12 个图标分为 **4 个软件图标**（CLI、Web、App、Game）和 **8 个硬件图标**（CPU、GPU、RAM、ROM/硬盘、NetUp、NetDown、USB、Vol）。
- 字体单位：**1000 / em**，字形高度正好 **1em**。所以 `font-size: 38px` 渲染出来的键帽/图标高度就是 38px。
- 字体为单色轮廓字体，`color` / `currentColor` 决定整体颜色；内部透明。
- 文字轮廓来自 **Noto Sans SemiBold** 与 **JetBrains Mono SemiBold**（均为 OFL），没有打包 Segoe UI。

## 字体用法

```css
@font-face {
  font-family: "Keycap Tight";
  src: url("KeycapTight-Regular.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: block;
}

.key {
  font: 400 38px/1 "Keycap Tight";
  color: #20242a;
}
```

```html
<span class="key">&#xE000;</span>
```

`font-size` 就是键帽高度；`line-height: 1`。不要去加 `font-weight: 600`，字体本身已经是半粗轮廓。

字体映射 PUA 码位 **U+E000–U+E05E**，并额外映射普通 ASCII 字母和数字：

- `A`–`Z` → 对应键帽（每个字母的 PUA 见 `text_map`）；
- `a`–`z` → 同一个对应键帽，所以 `a` 和 `A` 都显示 A 键；
- `0`–`9` → 对应数字键帽。

```html
<span class="key">A</span>
<span class="key">a</span>
<span class="key">7</span>
<span class="key">&#xE000;</span>
```

因为 ASCII 被字体占用，**不要用这个字体排普通正文**；正文请用正常字体，只在需要键帽/图标的地方使用 Keycap Tight。完整 62 条映射见 `keycap-tight-text-map.csv` 或 mapping 里的 `text_map`。

### 软件图标

| 图标 | 含义 | PUA | 文件夹 |
|---|---|---|---|
| CLI | 命令行 | `U+E059` | `glyphs/U+E059_CLI/` |
| Web | 网页 | `U+E05A` | `glyphs/U+E05A_Web/` |
| App | 应用程序 | `U+E05B` | `glyphs/U+E05B_App/` |
| Game | 游戏 | `U+E05C` | `glyphs/U+E05C_Game/` |

本版图形：

- **CLI**：终端窗口，顶部只有分隔线，不再有三个窗口圆点；内部为 `>_` 提示符。
- **Web**：浏览器窗口，顶部只有分隔线，不再有三个圆点；内容区为两条横线。
- **App**：一个圆角矩形，右下角为更大的 `APP` 三个字符；字符略微超出右边框，右边框在字符处开口避让，避免与文字重叠。

### 硬件图标

| 图标 | 含义 | PUA | 文件夹 |
|---|---|---|---|
| CPU | 处理器 | `U+E053` | `glyphs/U+E053_CPU/` |
| GPU | 显卡 / 图形处理器 | `U+E054` | `glyphs/U+E054_GPU/` |
| RAM | 内存 | `U+E055` | `glyphs/U+E055_RAM/` |
| ROM | 硬盘（本键盘用 ROM 标注） | `U+E056` | `glyphs/U+E056_ROM/` |
| NetUp | 网络上行 | `U+E057` | `glyphs/U+E057_NetUp/` |
| NetDown | 网络下行 | `U+E058` | `glyphs/U+E058_NetDown/` |
| USB | U 盘 | `U+E05D` | `glyphs/U+E05D_USB/` |
| Vol | 音量 | `U+E05E` | `glyphs/U+E05E_Vol/` |

本版图形：

- **GPU**：整体横向更窄；风扇仍为单一圆环，横向比纵向略窄；底部保留三根竖线，线宽和间距不变。
- **RAM**：内部简化为三个小矩形，底部只有五根小竖线。
- **ROM**：保留硬盘盘片和磁头臂，删除底部三根小竖线。
- **USB**：按照片改为 USB-A 插头正视图，金属壳上有两个方形开孔；下部盘体比插头略宽、比上一版更矮，底部不封口。
- **Vol**：右侧改为两个同心圆弧，不再使用折线箭头。

这些字形是**线条图形**，不是 `CPU`、`CLI` 等文字，也没有键帽外框；背景完全透明。字体中它们与键帽一样占 **1em 高**，所以 `font-size: 38px` 时图标高 38px。图标没有 `event.code`，不参与键盘按键映射，但可以按 `icons` / `software_icons` / `hardware_icons` 分类读取。

### 与事件映射

```js
const map = await fetch("keycap-tight-mapping.json").then(r => r.json());
const byCode = new Map(map.keys.map(k => [k.code, k]));

document.addEventListener("keydown", (e) => {
  const key = byCode.get(e.code);
  if (!key) return;
  el.textContent = String.fromCodePoint(key.codepoint);
});
```

同一字形会被多个物理键共用，例如 `ShiftLeft` / `ShiftRight` 都指向 `shift`，`Numpad7` 与 `Digit7` 都指向 `digit7`。这是按“重复键只计一个”处理的；映射表里仍保留全部 101 个 keycode。

## SVG 用法

### 单字符文件夹

```html
<img src="glyphs/U+E000_Esc/keycap.svg" width="105" height="62" alt="Esc">
<img src="glyphs/U+E053_CPU/icon.svg" width="62" height="62" alt="CPU">
<img src="glyphs/U+E059_CLI/icon.svg" width="62" height="62" alt="Command line">
```

`<img>` 方式固定为黑色；要跟随主题色，直接内联该 SVG，或使用 sprite。

### Sprite + currentColor

```html
<svg class="key" viewBox="0 0 105.058 62" aria-label="Esc">
  <use href="keycap-tight-sprite.svg#key-escape"></use>
</svg>
<svg class="key" viewBox="0 0 62 62" aria-label="CPU">
  <use href="keycap-tight-sprite.svg#key-cpu"></use>
</svg>
<svg class="key" viewBox="0 0 62 62" aria-label="Command line">
  <use href="keycap-tight-sprite.svg#key-terminal"></use>
</svg>
```

```css
.key { color: #f4f1ea; }
```

外部 `<use>` 在 `file://` 下可能被浏览器拦截，本地开发建议起一个静态服务器；或者把 sprite 内联到 HTML 中，再用 `#key-escape` 引用。内联时还可以分别覆盖：

```css
.keycap-frame { fill: #20242a; }
.keycap-label { fill: #c35a12; }
```

## Windows 标注规则

| 照片上的内容 | 输出 |
|---|---|
| `start / opt` | `Win` |
| `alt / cmd` | `Alt` |
| `ctrl / opt` | `Ctrl` |
| `caps lock` | `Cap` |
| `backspace` | `Back` |
| `escape` | `Esc` |
| `page up` / `page down` | `PgUp` / `PgDn` |
| `insert` / `delete` | `Ins` / `Del` |
| `clear` + 锁图标 | `Num` |
| 数字键上的 `! @ # …` | 只保留主字符 `1 2 3 …` |
| 小键盘 `7 home`、`0 ins` 等 | 只保留 `7`、`0` |
| F1–F12 的媒体图标 | 只保留 `F1`–`F12` |
| `\`、`[`、`]`、`;`、`'`、`,`、`.`、`/` | 只保留主字符，不带 shift 副符号 |

## 注意事项

- 浏览器通常不会为 **Fn** 触发 `KeyboardEvent`；`FnLeft` / `FnRight` 是自定义映射名，只用于视觉显示。
- Windows 键在浏览器里通常报告为 **`MetaLeft`**。
- 小键盘使用 `Numpad0`…`Numpad9`、`NumpadAdd`、`NumpadSubtract`、`NumpadMultiply`、`NumpadDivide`、`NumpadDecimal`、`NumpadEnter`、`NumLock`。
- 字体高度等于 1em；如果放进 `line-height` 很紧的容器，请显式设置 `line-height: 1`。
- 字体是单色轮廓：外框和文字同色。需要外框/文字双色时，用内联 SVG sprite。
- 字符文件夹名中的 `U+E02E_Backslash` 等描述词只用于文件名；显示内容始终以 `glyph.json` / mapping 的 `label` 为准。
- 所有目录与文件名使用英文：`work/`、`dist/`、`dist/glyphs/`。

## 许可证

字体轮廓来自 **Noto Sans SemiBold** 与 **JetBrains Mono SemiBold**，按 **SIL Open Font License 1.1** 使用与再分发。  
本字体命名为 **Keycap Tight**，不沿用原字体的保留字体名。完整许可证见 `OFL.txt` 与 `OFL-JetBrainsMono.txt`。
