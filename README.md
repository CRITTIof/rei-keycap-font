# KeycapTight 整理结果

按照片键盘制作的 Windows 主标注键帽图标集：**101 个物理键 → 83 个唯一字形**。键帽为内容贴合圆角框、内部透明、只显示主键内容。

## 目录

| 目录 | 内容 |
|---|---|
| `工作文件/` | 源码、Noto 字体素材、`pydeps`、`tools`、构建脚本 |
| `成品/` | 字体、sprite、映射、Demo、总览、83 个字符文件夹、ZIP |
| `成品/字符/` | **每个字符一个文件夹**：`keycap.svg` + `preview.png` + `glyph.json` |

## 快速打开

- [完整包](成品/KeycapTight-Windows.zip)
- [总览图](成品/keycap-tight-specimen.png)
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
