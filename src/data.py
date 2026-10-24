"""Keycap set data: 106 physical keys, 87 keycaps, 32 system icons."""

# glyph_id, label, full name, group
UNIQUE = [
    ("escape", "Esc", "Escape", "function"),
    *[(f"f{i}", f"F{i}", f"F{i}", "function") for i in range(1, 13)],
    ("insert", "Ins", "Insert", "function"),
    ("delete", "Del", "Delete", "function"),
    ("home", "Home", "Home", "function"),
    ("end", "End", "End", "function"),
    ("pageup", "PgUp", "Page Up", "function"),
    ("pagedown", "PgDn", "Page Down", "function"),
    ("backquote", "`", "Backquote", "numbers"),
    *[(f"digit{i}", str(i), str(i), "numbers") for i in range(1, 10)],
    ("digit0", "0", "0", "numbers"),
    ("minus", "-", "Minus", "numbers"),
    ("equal", "=", "Equal", "numbers"),
    ("backspace", "Back", "Backspace", "numbers"),
    ("tab", "Tab", "Tab", "letters"),
    *[(f"key{c}", c.upper(), c.upper(), "letters") for c in "qwertyuiop"],
    ("bracketleft", "[", "Left Bracket", "letters"),
    ("bracketright", "]", "Right Bracket", "letters"),
    ("backslash", "\\", "Backslash", "letters"),
    ("capslock", "Cap", "Caps Lock", "caps"),
    *[(f"key{c}", c.upper(), c.upper(), "caps") for c in "asdfghjkl"],
    ("semicolon", ";", "Semicolon", "caps"),
    ("quote", "'", "Apostrophe", "caps"),
    ("enter", "Enter", "Enter", "caps"),
    ("shift", "Shift", "Shift", "shift"),
    *[(f"key{c}", c.upper(), c.upper(), "shift") for c in "zxcvbnm"],
    ("comma", ",", "Comma", "shift"),
    ("period", ".", "Period", "shift"),
    ("slash", "/", "Slash", "shift"),
    ("ctrl", "Ctrl", "Control", "mods"),
    ("fn", "Fn", "Function", "mods"),
    ("win", "Win", "Windows", "mods"),
    ("alt", "Alt", "Alt", "mods"),
    ("space", "Space", "Space", "mods"),
    ("arrowleft", "←", "Arrow Left", "mods"),
    ("arrowup", "↑", "Arrow Up", "mods"),
    ("arrowdown", "↓", "Arrow Down", "mods"),
    ("arrowright", "→", "Arrow Right", "mods"),
    ("num", "Num", "Num Lock", "numpad"),
    ("asterisk", "*", "Multiply", "numpad"),
    ("plus", "+", "Plus", "numpad"),
]

# Keys that a standard 104-key Windows keyboard has in addition to the
# photographed keyboard.  They are ordinary keycaps and sit in the same
# contiguous U+E000 block as every other keycap.
EXTRA_KEYS = [
    ("printscreen", "PrtSc", "Print Screen", "function"),
    ("scrolllock", "ScrLk", "Scroll Lock", "function"),
    ("pause", "Pause", "Pause", "function"),
    ("menu", "Menu", "Context Menu", "mods"),
]

# code, label, glyph, full, section
PHYS = [
    ("Escape", "Esc", "escape", "Escape", "function"),
    *[(f"F{i}", f"F{i}", f"f{i}", f"F{i}", "function") for i in range(1, 13)],
    ("Insert", "Ins", "insert", "Insert", "function"),
    ("Delete", "Del", "delete", "Delete", "function"),
    ("Home", "Home", "home", "Home", "function"),
    ("End", "End", "end", "End", "function"),
    ("PageUp", "PgUp", "pageup", "Page Up", "function"),
    ("PageDown", "PgDn", "pagedown", "Page Down", "function"),
    ("Backquote", "`", "backquote", "Backquote", "numbers"),
    *[(f"Digit{i}", str(i), f"digit{i}", str(i), "numbers") for i in range(1, 10)],
    ("Digit0", "0", "digit0", "0", "numbers"),
    ("Minus", "-", "minus", "Minus", "numbers"),
    ("Equal", "=", "equal", "Equal", "numbers"),
    ("Backspace", "Back", "backspace", "Backspace", "numbers"),
    ("Tab", "Tab", "tab", "Tab", "letters"),
    *[(f"Key{c.upper()}", c.upper(), f"key{c}", c.upper(), "letters") for c in "qwertyuiop"],
    ("BracketLeft", "[", "bracketleft", "Left Bracket", "letters"),
    ("BracketRight", "]", "bracketright", "Right Bracket", "letters"),
    ("Backslash", "\\", "backslash", "Backslash", "letters"),
    ("CapsLock", "Cap", "capslock", "Caps Lock", "caps"),
    *[(f"Key{c.upper()}", c.upper(), f"key{c}", c.upper(), "caps") for c in "asdfghjkl"],
    ("Semicolon", ";", "semicolon", "Semicolon", "caps"),
    ("Quote", "'", "quote", "Apostrophe", "caps"),
    ("Enter", "Enter", "enter", "Enter", "caps"),
    ("ShiftLeft", "Shift", "shift", "Shift", "shift"),
    *[(f"Key{c.upper()}", c.upper(), f"key{c}", c.upper(), "shift") for c in "zxcvbnm"],
    ("Comma", ",", "comma", "Comma", "shift"),
    ("Period", ".", "period", "Period", "shift"),
    ("Slash", "/", "slash", "Slash", "shift"),
    ("ShiftRight", "Shift", "shift", "Shift", "shift"),
    ("ControlLeft", "Ctrl", "ctrl", "Control", "mods"),
    ("FnLeft", "Fn", "fn", "Function", "mods"),
    ("MetaLeft", "Win", "win", "Windows", "mods"),
    ("AltLeft", "Alt", "alt", "Alt", "mods"),
    ("Space", "Space", "space", "Space", "mods"),
    ("AltRight", "Alt", "alt", "Alt", "mods"),
    ("FnRight", "Fn", "fn", "Function", "mods"),
    ("ControlRight", "Ctrl", "ctrl", "Control", "mods"),
    ("ArrowLeft", "←", "arrowleft", "Arrow Left", "mods"),
    ("ArrowUp", "↑", "arrowup", "Arrow Up", "mods"),
    ("ArrowDown", "↓", "arrowdown", "Arrow Down", "mods"),
    ("ArrowRight", "→", "arrowright", "Arrow Right", "mods"),
    ("NumLock", "Num", "num", "Num Lock", "numpad"),
    ("NumpadDivide", "/", "slash", "Slash", "numpad"),
    ("NumpadMultiply", "*", "asterisk", "Multiply", "numpad"),
    ("NumpadSubtract", "-", "minus", "Minus", "numpad"),
    ("Numpad7", "7", "digit7", "7", "numpad"),
    ("Numpad8", "8", "digit8", "8", "numpad"),
    ("Numpad9", "9", "digit9", "9", "numpad"),
    ("NumpadAdd", "+", "plus", "Plus", "numpad"),
    ("Numpad4", "4", "digit4", "4", "numpad"),
    ("Numpad5", "5", "digit5", "5", "numpad"),
    ("Numpad6", "6", "digit6", "6", "numpad"),
    ("Numpad1", "1", "digit1", "1", "numpad"),
    ("Numpad2", "2", "digit2", "2", "numpad"),
    ("Numpad3", "3", "digit3", "3", "numpad"),
    ("NumpadEnter", "Enter", "enter", "Enter", "numpad"),
    ("Numpad0", "0", "digit0", "0", "numpad"),
    ("NumpadDecimal", ".", "period", "Period", "numpad"),
    ("PrintScreen", "PrtSc", "printscreen", "Print Screen", "function"),
    ("ScrollLock", "ScrLk", "scrolllock", "Scroll Lock", "function"),
    ("Pause", "Pause", "pause", "Pause", "function"),
    ("MetaRight", "Win", "win", "Windows", "mods"),
    ("ContextMenu", "Menu", "menu", "Context Menu", "mods"),
]

# Software / file / AI / media icons.  They own the U+E100 block.
# Simple transparent line icons, not text; each occupies one em.
SOFTWARE_ICONS = [
    ("terminal", "CLI", "Command line", "software"),
    ("web", "Web", "Web page", "software"),
    ("app", "App", "Application", "software"),
    ("game", "Game", "Game", "software"),
    ("folder", "Folder", "Folder", "file"),
    ("txt", "TXT", "Text file", "file"),
    ("image", "Image", "Image", "file"),
    ("agent", "AI", "AI Agent", "ai"),
]

# Hardware icons.  They own the U+E200 block.
HARDWARE_ICONS = [
    ("cpu", "CPU", "Processor", "hardware"),
    ("gpu", "GPU", "Graphics processor", "hardware"),
    ("ram", "RAM", "Memory", "hardware"),
    ("rom", "ROM", "Hard drive (ROM)", "hardware"),
    ("netup", "NetUp", "Network uplink", "hardware"),
    ("netdown", "NetDown", "Network downlink", "hardware"),
    ("usb", "USB", "USB drive", "hardware"),
    ("volume", "Vol", "Volume", "hardware"),
    ("microphone", "Mic", "Microphone", "hardware"),
]

# Interface icons.  They own the U+E300 block and are not keycaps, software
# icons or hardware icons.
UI_ICONS = [
    ("content", "Content", "Content", "ui"),
    ("appearance", "Look", "Appearance", "ui"),
    ("datasource", "Source", "Data source", "ui"),
    ("behavior", "Action", "Behavior", "ui"),
    ("hotkey", "Hotkey", "Hotkey", "ui"),
    ("search", "Search", "Search", "ui"),
    ("trash", "Delete", "Delete", "ui"),
    ("move", "Move", "Move", "ui"),
    ("add", "Add", "Add", "ui"),
    ("expand", "Expand", "Expand", "ui"),
    ("video", "Video", "Video", "ui"),
    ("clock", "Clock", "Clock", "ui"),
    ("keypress", "Press", "Key press", "ui"),
    ("play", "Play", "Play", "ui"),
    # "pause" is already the gid of the Pause keycap.
    ("pausemedia", "Pause", "Pause", "ui"),
]

ICONS = SOFTWARE_ICONS + HARDWARE_ICONS + UI_ICONS

# PUA blocks.  Each block is 256 code points so later additions have room:
#   U+E000-U+E0FF  keycaps (87 used)
#   U+E100-U+E1FF  software, file and AI icons (8 used)
#   U+E200-U+E2FF  hardware icons (9 used)
#   U+E300-U+E3FF  interface icons (15 used)
PUA_KEYCAP = 0xE000
PUA_SOFTWARE = 0xE100
PUA_HARDWARE = 0xE200
PUA_UI = 0xE300

ALL_KEYCAPS = UNIQUE + EXTRA_KEYS
ALL_GLYPHS = ALL_KEYCAPS + ICONS

PUA = {gid: PUA_KEYCAP + i for i, (gid, *_rest) in enumerate(ALL_KEYCAPS)}
PUA.update({gid: PUA_SOFTWARE + i for i, (gid, *_rest) in enumerate(SOFTWARE_ICONS)})
PUA.update({gid: PUA_HARDWARE + i for i, (gid, *_rest) in enumerate(HARDWARE_ICONS)})
PUA.update({gid: PUA_UI + i for i, (gid, *_rest) in enumerate(UI_ICONS)})

assert len(PHYS) == 106, len(PHYS)
assert len(UNIQUE) == 83, len(UNIQUE)
assert len(EXTRA_KEYS) == 4, len(EXTRA_KEYS)
assert len(ALL_KEYCAPS) == 87, len(ALL_KEYCAPS)
assert len(SOFTWARE_ICONS) == 8, len(SOFTWARE_ICONS)
assert len(HARDWARE_ICONS) == 9, len(HARDWARE_ICONS)
assert len(UI_ICONS) == 15, len(UI_ICONS)
assert len(ICONS) == 32, len(ICONS)
assert len({g[0] for g in ALL_KEYCAPS}) == len(ALL_KEYCAPS)
assert len({g[0] for g in ALL_GLYPHS}) == len(ALL_GLYPHS)
assert set(g[0] for g in ALL_KEYCAPS) == set(p[2] for p in PHYS)
assert len(PUA) == len(ALL_GLYPHS)
