# Keycap Tight / Windows

透明、内容贴合的键帽图标集，按照片这把键盘整理为 **Windows 主标注**。  
共 **101 个物理键位**，去重后 **83 个独立键帽字形**；数字小键盘、左右修饰键等重复键共享同一个字形。

![总览](keycap-tight-specimen.png)

![实时 Demo](demo-preview.png)

## 目录

```text
KeycapTight/
├─ 工作文件/      源码、字体素材、依赖、构建脚本
└─ 成品/          字体、SVG、映射、Demo、预览和 ZIP
   ├─ 字符/
   │  ├─ U+E000_Esc/
   │  │  ├─ keycap.svg
   │  │  ├─ preview.png
   │  │  └─ glyph.json
   │  ├─ U+E001_F1/
   │  └─ ...（共 83 个字符文件夹）
   └─ ...
```

**每个字符一个独立文件夹**，文件夹名使用 `U+码位_标签`，避开了 `\ / * ? " < > |` 等 Windows 非法文件名字符；原始标签、全名、宽度和全部 keycode 都写在同目录的 `glyph.json` 里。`字符/index.csv` 是 83 个字符的总索引。

## 成品文件

| 文件 | 用途 |
|---|---|
| `字符/U+E000_Esc/keycap.svg` | 单字符 SVG，共 83 个文件夹 |
| `字符/index.csv` | 83 个字符的 PUA、标签、宽度、文件夹索引 |
| `KeycapTight-Regular.woff2` | Web 字体，主推荐 |
| `KeycapTight-Regular.ttf` | 桌面 / 其他环境字体 |
| `keycap-tight.css` | `@font-face` + 基础 `.keycap-tight` 样式 |
| `keycap-tight-sprite.svg` | 83 个 `<symbol>`，透明，可用 `currentColor` 换色 |
| `keycap-tight-mapping.json` | 完整映射：101 个 `event.code` → 字形 / PUA / 字符文件夹 |
| `keycap-tight-keymap.csv` | 同一映射的表格版 |
| `keycap-tight-glyphs.csv` | 83 个字形的 PUA、宽度、关联 keycode |
| `demo.html` | 实时按键高亮 Demo，支持深浅色 |
| `keycap-tight-specimen.svg / .png` | 83 个字形总览 |
| `font-proof-light.png / font-proof-dark.png` | 字体明暗背景渲染检查 |
| `OFL.txt` | 字体许可证（SIL Open Font License 1.1） |
| `KeycapTight-Windows.zip` | 上述成品的完整打包 |

## 设计规格

- 键帽外框高 **62**，圆角 **16**，描边 **4**，内部 **不填色**。
- 宽度 = 字符 advance 宽度 + 左右各 **20**；所有框统一高度，字符按实际墨迹垂直居中。
- 字体单位：**1000 / em**，字形高度正好 **1em**。所以 `font-size: 38px` 渲染出来的键帽高度就是 38px。
- 字体为单色轮廓字体，`color` / `currentColor` 决定整体颜色；内部透明。
- 文字轮廓来自 **Noto Sans SemiBold**（OFL），没有打包 Segoe UI。

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

字体只映射 PUA 码位 **U+E000–U+E052**，不覆盖普通 ASCII；渲染时请用 mapping 里的 `codepoint`。

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
<img src="字符/U+E000_Esc/keycap.svg" width="105" height="62" alt="Esc">
```

`<img>` 方式固定为黑色；要跟随主题色，直接内联该 SVG，或使用 sprite。

### Sprite + currentColor

```html
<svg class="key" viewBox="0 0 105.058 62" aria-label="Esc">
  <use href="keycap-tight-sprite.svg#key-escape"></use>
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

## 许可证

字体轮廓来自 **Noto Sans SemiBold**，按 **SIL Open Font License 1.1** 使用与再分发。  
本字体命名为 **Keycap Tight**，不沿用 Noto 的保留字体名。完整许可证见 `OFL.txt`。
