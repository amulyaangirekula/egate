# theme.py

# ---------- COLOR PALETTE ----------
PRIMARY_COLOR = "#3498db"
PRIMARY_DARK = "#2980b9"
DANGER_COLOR = "#e74c3c"
DANGER_DARK = "#c0392b"
BACKGROUND_LIGHT = "#fdfefe"
BACKGROUND_MAIN = "#f0f4f7"
TEXT_COLOR = "#222"
TITLE_COLOR = "#2c3e50"

# ---------- FONTS ----------
BASE_FONT = ("Segoe UI", 11)
TITLE_FONT = ("Segoe UI", 20, "bold")
SUBTITLE_FONT = ("Segoe UI", 14, "bold")
SECTION_TITLE = {
    "font": ("Segoe UI", 16, "bold"),
    "bg": BACKGROUND_LIGHT,
    "fg": TITLE_COLOR
}

# ---------- LABELS ----------
LABEL_STYLE = {
    "bg": BACKGROUND_LIGHT,
    "fg": TEXT_COLOR,
    "font": BASE_FONT
}

# ---------- ENTRIES ----------
ENTRY_STYLE = {
    "font": BASE_FONT,
    "width": 30,
    "bd": 1,
    "relief": "solid",
    "highlightthickness": 1,
    "highlightbackground": "#ccc",
    "highlightcolor": PRIMARY_COLOR
}

# ---------- BUTTONS ----------
BUTTON_STYLE = {
    "font": ("Segoe UI", 11, "bold"),
    "bg": PRIMARY_COLOR,
    "fg": "#fff",
    "activebackground": PRIMARY_DARK,
    "activeforeground": "#fff",
    "padx": 12,
    "pady": 6,
    "bd": 0,
    "cursor": "hand2"
}

DANGER_BUTTON_STYLE = {
    "font": ("Segoe UI", 11, "bold"),
    "bg": DANGER_COLOR,
    "fg": "#fff",
    "activebackground": DANGER_DARK,
    "activeforeground": "#fff",
    "padx": 12,
    "pady": 6,
    "bd": 0,
    "cursor": "hand2"
}
