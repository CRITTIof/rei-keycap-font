# 工作文件 / Keycap Tight

这里放构建所需的源码、字体素材、依赖和脚本；所有生成结果写入上一级的 `成品/`。

## 目录

```text
工作文件/
├─ src/
│  ├─ data.py            101 个物理键 / 83 个唯一字形
│  ├─ geometry.py        文字度量、圆角框、路径与 PUA
│  ├─ build_svg.py       sprite、总览、每字符文件夹
│  ├─ build_font.py      TTF / WOFF2 + 字体渲染检查
│  ├─ build_mapping.py   JSON / CSV 映射
│  └─ build_demo.py      实时按键 Demo
├─ assets/               Noto Sans SemiBold、OFL、备用字体、照片裁切
├─ pydeps/               fontTools / brotli 本地依赖（已 gitignore）
├─ tools/                @resvg/resvg-js（node_modules 已 gitignore）
├─ requirements.txt      Python 依赖版本
├─ templates/            README / CSS 模板
├─ render.js             单个 SVG → PNG
├─ render_chars.js       83 个字符 SVG → PNG
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

1. `build_svg.py` 生成 `成品/keycap-tight-sprite.svg`、总览 SVG，以及 `成品/字符/U+xxxx_Label/`。
2. `build_font.py` 生成 TTF / WOFF2 和明暗字体检查图。
3. `build_mapping.py` 生成 101 行 keycode 映射。
4. `build_demo.py` 生成 `成品/demo.html`。
5. `render_chars.js` 为每个字符生成 `preview.png`。
6. `render.js` 生成总览 PNG。
7. Edge headless 生成 `demo-preview.png`。
8. `build_package.py` 复制 README/CSS/OFL，打包 `KeycapTight-Windows.zip` 并校验数量。

## 修改字符

- 改标签、增删键：编辑 `src/data.py` 的 `UNIQUE` / `PHYS`，保持两者字形 id 一致。
- 改框高、圆角、描边、字距：编辑 `src/geometry.py` 顶部常量。
- 改字符文件夹命名：编辑 `geometry.py` 的 `FOLDER_LABEL` / `folder_name()`。

`成品/` 可以整个删除后重建；`工作文件/` 不依赖旧 `keyboard_keys/`。

## 许可证

字体轮廓来自 Noto Sans SemiBold，SIL OFL 1.1。发布时保留 `assets/OFL.txt` 与成品中的 `OFL.txt`。
