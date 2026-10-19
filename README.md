# KeycapTight 整理结果

按照片键盘制作的 Windows 主标注键帽图标集：**101 个物理键 → 83 个键帽字形 + 6 个系统线条图标 = 89 个字形**。键帽为内容贴合圆角框、内部透明、只显示主键内容；系统图标为透明线条图形，不是文字。

当前版本：**1.1.1**。

## 目录

| 目录 | 内容 |
|---|---|
| `工作文件/` | 源码、Noto 字体素材、`pydeps`、`tools`、构建脚本 |
| `成品/` | 字体、sprite、映射、Demo、总览、89 个字形文件夹、ZIP |
| `成品/字符/` | **每个字符/图标一个文件夹**：`keycap.svg` 或 `icon.svg` + `preview.png` + `glyph.json` |

## 快速打开

- [完整包](成品/KeycapTight-Windows.zip)
- [总览图](成品/keycap-tight-specimen.png)
- [6 个系统图标](成品/keycap-tight-icons.png)
- [实时 Demo](成品/demo.html)
- [成品说明](成品/README.md)
- [字符总索引](成品/字符/index.csv)

## 重建

```bash
cd 工作文件
python build_all.py
```

`成品/` 可整个删除后重建；构建不依赖旧 `keyboard_keys/`。

根目录上一轮的实验文件已移到 `../旧实验_2026-10-17/`，未删除。

## 许可

字体轮廓来自 Noto Sans SemiBold，SIL OFL 1.1；见 `成品/OFL.txt`。
