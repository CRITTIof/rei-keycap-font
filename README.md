# KeycapTight

按照片键盘制作的 Windows 主标注键帽图标集：**101 个物理键 → 83 个键帽字形 + 12 个系统线条图标 = 95 个字形**。键帽为内容贴合圆角框、内部透明、只显示主键内容；系统图标为透明线条图形，不是文字。普通 ASCII 字母/数字已映射到对应键帽。

当前版本：**1.4.0**。字母与数字键帽保持等宽；所有字形统一使用 62 高 / 1em 槽；本轮缩短 USB 下部、放大 APP。

## 目录

| 目录 | 内容 |
|---|---|
| `work/` | 源码、字体素材、`pydeps`、`tools`、构建脚本 |
| `dist/` | 字体、sprite、映射、Demo、总览、95 个字形文件夹、ZIP |
| `dist/glyphs/` | **每个字符/图标一个文件夹**：`keycap.svg` 或 `icon.svg` + `preview.png` + `glyph.json` |

所有目录与文件名均为英文。

## 快速打开

- [完整包](dist/KeycapTight-Windows.zip)
- [总览图](dist/keycap-tight-specimen.png)
- [12 个系统图标](dist/keycap-tight-icons.png)
- [实时 Demo](dist/demo.html)
- [成品说明](dist/README.md)
- [字形总索引](dist/glyphs/index.csv)

## 重建

```bash
cd work
python build_all.py
```

`dist/` 可整个删除后重建；构建不依赖旧 `keyboard_keys/`。

上一轮实验目录已改名为 `../old-experiment-2026-10-17/`，未删除。

## 许可

字体轮廓来自 Noto Sans SemiBold 与 JetBrains Mono SemiBold，均为 SIL OFL 1.1；见 `dist/OFL.txt` 与 `dist/OFL-JetBrainsMono.txt`。
