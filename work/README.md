# work / Keycap Tight

这里放构建所需的源码、字体素材、依赖和脚本；所有生成结果写入上一级的 `dist/`。

## 目录

```text
work/
├─ src/
│  ├─ data.py            101 个物理键 / 83 个键帽 + 12 个系统图标
│  ├─ geometry.py        文字度量、等宽字体、圆角框、路径与 PUA
│  ├─ build_svg.py       sprite、总览、每字符文件夹
│  ├─ build_font.py      TTF / WOFF2 + 字体渲染检查
│  ├─ build_mapping.py   JSON / CSV 映射
│  └─ build_demo.py      实时按键 Demo
├─ assets/               Noto Sans SemiBold、JetBrains Mono SemiBold、OFL、照片裁切
├─ pydeps/               fontTools / brotli 本地依赖（已 gitignore）
├─ tools/                @resvg/resvg-js（node_modules 已 gitignore）
├─ requirements.txt      Python 依赖版本
├─ templates/            README / CSS 模板
├─ render.js             单个 SVG → PNG
├─ render_chars.js       95 个字形 SVG → PNG
├─ build_package.py      复制静态文件、打包 ZIP、校验
└─ build_all.py          一键重建
```

## 重建

使用 DSH 自带的 Python（`pydeps` 与它匹配）：

```bash
python build_all.py
```

或显式指定：

```bash
C:\Users\CRITT\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe build_all.py
```

首次在新环境构建时安装依赖：

```bash
python -m pip install --target pydeps -r requirements.txt
cd tools && pnpm install
```

流程：

1. `build_svg.py` 生成 `dist/keycap-tight-sprite.svg`、总览 SVG，以及 `dist/glyphs/U+xxxx_Label/`（83 个键帽 + 12 个图标）。
2. `build_font.py` 生成 TTF / WOFF2、ASCII 字母/数字映射和明暗字体检查图。
3. `build_mapping.py` 生成 101 行 keycode 映射、12 个图标（软件/硬件分组）和 62 条文字别名。
4. `build_demo.py` 生成 `dist/demo.html`。
5. `render_chars.js` 为每个字形生成 `preview.png`。
6. `render.js` 生成总览 PNG。
7. Edge headless 生成 `demo-preview.png`。
8. `build_package.py` 复制 README/CSS/OFL，打包 `KeycapTight-Windows.zip` 并校验数量。

## 修改字符

- 改标签、增删键：编辑 `src/data.py` 的 `UNIQUE` / `PHYS`，保持两者字形 id 一致。
- 增删系统图标：编辑 `src/data.py` 的 `ICONS`（`group` 用 `software` / `hardware`），并在 `geometry.py` 的 `draw_icon_svg()` 中加对应线条路径。
- 字母/数字别名：由 `geometry.py` 的 `TEXT_CHARS` / `TEXT_CMAP` 自动生成，`A-Z`、`a-z`、`0-9` 会写入字体 cmap。
- 字母/数字字体：`geometry.py` 的 `face_for_label()` 与 `FACES`；等宽字体为 `assets/jetbrains-mono-semibold.ttf`。
- 改框高、圆角、描边、字距：编辑 `src/geometry.py` 顶部常量。
- 改字符文件夹命名：编辑 `geometry.py` 的 `FOLDER_LABEL` / `folder_name()`。

`dist/` 可以整个删除后重建；`work/` 不依赖旧 `keyboard_keys/`。

## 许可证

字体轮廓来自 Noto Sans SemiBold 与 JetBrains Mono SemiBold，均为 SIL OFL 1.1。发布时保留 `assets/OFL.txt`、`assets/OFL-JetBrainsMono.txt` 与成品中的对应文件。
