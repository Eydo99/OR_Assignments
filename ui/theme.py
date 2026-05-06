

BG = "#0F172A"          # Midnight Slate (Main Background)
SURFACE = "#1E293B"     # Elevated Card Background
SURFACE2 = "#334155"    # Hover states / Active elements
BORDER = "#334155"      # Subtle separators
HIGHLIGHT = "#475569"   # Pressed states / Table selection

# Vibrant Accents
INDIGO = "#6366F1"      # Primary Brand / Active CTA
INDIGO_D = "#4338CA"    # Darker Indigo for gradients/pressed
CYAN = "#06B6D4"        # Secondary Accent (Numbers, highlights)
CYAN_D = "#0891B2"
GREEN = "#10B981"       # Safe / Positive (Hider payoff)
RED = "#F43F5E"         # Danger / Negative (Seeker payoff)
AMBER = "#F59E0B"       # Scores / Warnings

# Typography Colors
TEXT = "#F8FAFC"        # Brilliant White (Headings, primary text)
TEXT_DARK = "#0F172A"   # Dark text for light backgrounds
MUTED = "#94A3B8"       # Slate 400 (Secondary text)
MUTED2 = "#64748B"      # Slate 500 (Tertiary / disabled)

FONT_UI = "Segoe UI Variable, Segoe UI, Inter, Roboto, sans-serif"
FONT_MONO = "Cascadia Code, Consolas, Courier New, monospace"

FONT_SM = 11
FONT_MD = 14
FONT_LG = 16
FONT_XL = 32
FONT_TITLE = 36


# Maps place-type codes to difficulty levels.
# "Easy"    → seeker-friendly location (open terrain, visible)
# "Neutral" → balanced location
# "Hard"    → hider-friendly location (dense cover, concealed)
DIFFICULTY_MAPPING: dict[str, str] = {
    "F": "Hard",      # Forest  — dense cover, hard to seek
    "C": "Hard",      # Cave    — enclosed, hard to seek
    "M": "Hard",      # Mountain— rugged terrain, hard to seek
    "V": "Neutral",   # Valley  — moderate visibility
    "R": "Neutral",   # River   — moderate visibility
    "N": "Neutral",   # Neutral — by definition balanced
    "B": "Easy",      # Beach   — open, easy to seek
    "P": "Easy",      # Park    — open, easy to seek
    "H": "Easy",      # House   — structured, easy to seek
    "S": "Easy",      # Shop    — structured, easy to seek
    "E": "Easy",      # Easy    — explicitly easy
    "D": "Neutral",   # Danger  — high-risk neutral
    "X": "Hard",      # Hard    — explicitly hard
}

# Colours used for difficulty badges/borders
DIFFICULTY_COLORS: dict[str, str] = {
    "Easy":    GREEN,
    "Neutral": AMBER,
    "Hard":    RED,
}

# Short badge labels shown inside buttons
DIFFICULTY_BADGE: dict[str, str] = {
    "Easy":    "◉ Easy",
    "Neutral": "◎ Neutral",
    "Hard":    "◈ Hard",
}


def difficulty_color(place_type: str) -> str:
    """Return the accent colour for the given place type's difficulty."""
    diff = DIFFICULTY_MAPPING.get(place_type, "Neutral")
    return DIFFICULTY_COLORS[diff]


def difficulty_label(place_type: str) -> str:
    """Return the short badge string for the given place type's difficulty."""
    diff = DIFFICULTY_MAPPING.get(place_type, "Neutral")
    return DIFFICULTY_BADGE[diff]


def difficulty_name(place_type: str) -> str:
    """Return just the difficulty name (Easy / Neutral / Hard)."""
    return DIFFICULTY_MAPPING.get(place_type, "Neutral")


def global_stylesheet() -> str:
    return f"""
    /* ── Base App & Window ── */
    QMainWindow, QDialog, QStackedWidget {{
        background-color: {BG};
    }}
    QWidget {{
        color: {TEXT};
        font-family: "{FONT_UI}";
        font-size: {FONT_MD}px;
    }}

    /* ── Side Nav Bar ── */
    #SideNavBar {{
        background-color: {SURFACE};
        border-right: 1px solid {BORDER};
    }}
    #NavButton {{
        background: transparent;
        border: none;
        border-radius: 12px;
        padding: 10px 4px;
        color: {MUTED};
        font-weight: 600;
    }}
    #NavButton:hover {{
        background-color: {SURFACE2};
        color: {TEXT};
    }}

    /* ── Primary CTA Buttons ── */
    QPushButton {{
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {INDIGO}, stop:1 {INDIGO_D});
        color: {TEXT};
        border: none;
        border-radius: 10px;
        padding: 12px 28px;
        font-weight: bold;
        font-size: {FONT_MD}px;
        letter-spacing: 1px;
    }}
    QPushButton:hover {{
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #818CF8, stop:1 {INDIGO});
    }}
    QPushButton:pressed {{
        background-color: {INDIGO_D};
    }}
    QPushButton:disabled {{
        background-color: {SURFACE};
        color: {MUTED2};
        border: 1.5px solid {BORDER};
    }}

    /* ── Stepper Buttons (+/-) ── */
    QPushButton[class="stepper-btn"] {{
        background-color: {SURFACE2};
        color: {TEXT};
        border: none;
        border-radius: 10px;
        font-size: 20px;
        font-weight: 400;
        padding: 0px;
        letter-spacing: 0px;
    }}
    QPushButton[class="stepper-btn"]:hover {{
        background-color: {HIGHLIGHT};
    }}
    QPushButton[class="stepper-btn"]:pressed {{
        background-color: {MUTED2};
    }}

    /* ── Role Card Button ── */
    QPushButton[class="role-card"] {{
        background-color: {SURFACE};
        color: {TEXT};
        border: 1.5px solid {BORDER};
        border-radius: 16px;
        padding: 24px;
        font-size: {FONT_MD}px;
        text-align: center;
    }}
    QPushButton[class="role-card"]:hover {{
        background-color: #263245;
        border: 1.5px solid {HIGHLIGHT};
    }}
    QPushButton[class="role-card"][active="true"] {{
        background-color: rgba(99, 102, 241, 0.12);
        border: 2px solid {INDIGO};
    }}

    /* ── Mode Toggle ── */
    QPushButton[class="toggle-on"] {{
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {INDIGO}, stop:1 {INDIGO_D});
        color: {TEXT};
        border: none;
        border-radius: 10px;
        font-weight: 700;
        font-size: {FONT_MD}px;
        padding: 11px 24px;
        letter-spacing: 0.3px;
    }}
    QPushButton[class="toggle-on"]:hover {{
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #818CF8, stop:1 {INDIGO});
    }}
    QPushButton[class="toggle-off"] {{
        background-color: transparent;
        color: {MUTED};
        border: none;
        border-radius: 10px;
        font-weight: 500;
        font-size: {FONT_MD}px;
        padding: 11px 24px;
        letter-spacing: 0px;
    }}
    QPushButton[class="toggle-off"]:hover {{
        color: {TEXT};
        background-color: {SURFACE2};
    }}

    /* ── Inputs ── */
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
        background-color: {SURFACE};
        color: {TEXT};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 8px 14px;
        font-size: {FONT_MD}px;
        selection-background-color: {INDIGO};
    }}
    QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
        border: 1px solid {INDIGO};
        background-color: {SURFACE2};
    }}
    QSpinBox::up-button, QSpinBox::down-button {{
        background-color: transparent;
        width: 24px;
    }}
    QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
        background-color: {HIGHLIGHT};
        border-radius: 4px;
    }}
    QComboBox::drop-down {{
        border: none;
        background: transparent;
        width: 30px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {SURFACE2};
        color: {TEXT};
        border: 1px solid {BORDER};
        border-radius: 8px;
        selection-background-color: {INDIGO};
    }}

    /* ── Typography / Labels ── */
    QLabel {{
        background: transparent;
    }}
    QLabel[class="page-title"] {{
        font-size: {FONT_TITLE}px;
        font-weight: 800;
        color: {TEXT};
        letter-spacing: -1px;
    }}
    QLabel[class="page-subtitle"] {{
        font-size: {FONT_LG}px;
        color: {MUTED};
        font-weight: 400;
    }}
    QLabel[class="section-label"] {{
        font-size: {FONT_SM}px;
        font-weight: 800;
        color: {MUTED2};
        letter-spacing: 2px;
        text-transform: uppercase;
    }}
    QLabel[class="cyan-number"] {{
        font-family: "{FONT_MONO}";
        font-size: {FONT_XL}px;
        font-weight: 900;
        color: {CYAN};
    }}
    QLabel[class="amber-number"] {{
        font-family: "{FONT_MONO}";
        font-size: {FONT_XL}px;
        font-weight: 900;
        color: {AMBER};
    }}
    QLabel[class="stat-value"] {{
        font-family: "{FONT_MONO}";
        font-size: {FONT_LG}px;
        font-weight: 800;
        color: {TEXT};
    }}

    /* ── World Size Container ── */
    QFrame[class="size-container"] {{
        background-color: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 14px;
    }}

    /* ── Panels & Cards ── */
    QFrame[class="score-panel"], QFrame[class="stat-card"] {{
        background-color: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 16px;
    }}
    QFrame[class="score-panel"]:hover, QFrame[class="stat-card"]:hover {{
        border: 1px solid {HIGHLIGHT};
    }}

    /* ── 1D Strip Place Button ── */
    QPushButton[class="place-btn"] {{
        background-color: {SURFACE2};
        color: {TEXT};
        border: 1px solid {BORDER};
        border-radius: 10px;
        font-family: "{FONT_MONO}";
        font-size: {FONT_SM}px;
        font-weight: bold;
        padding: 12px 8px;
        min-width: 60px;
        letter-spacing: 0px;
    }}
    QPushButton[class="place-btn"]:hover {{
        background-color: {HIGHLIGHT};
        border: 1px solid {INDIGO};
    }}

    /* ── Table (Payoff Matrix) ── */
    QTableWidget {{
        background-color: transparent;
        gridline-color: transparent;
        border: none;
        font-family: "{FONT_MONO}";
        font-size: {FONT_SM}px;
    }}
    QTableWidget::item {{
        padding: 4px;
        margin: 1px;
        border-radius: 4px;
        background-color: {SURFACE};
        border: none;
        text-align: center;
    }}
    QTableWidget::item:selected {{
        background-color: rgba(99, 102, 241, 0.2);
        border: 1px solid {INDIGO};
        color: {TEXT};
    }}
    QHeaderView::section {{
        background-color: transparent;
        color: {MUTED};
        font-family: "{FONT_MONO}";
        font-size: 10px;
        font-weight: bold;
        padding: 4px 2px;
        border: none;
    }}
    QHeaderView {{
        background-color: transparent;
    }}
    QTableCornerButton::section {{
        background-color: transparent;
        border: none;
    }}

    /* ── Progress Bar (Strategy) ── */
    QProgressBar {{
        background-color: {SURFACE2};
        border: none;
        border-radius: 6px;
        height: 10px;
        text-align: center;
        color: transparent;
    }}
    QProgressBar::chunk {{
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {CYAN_D}, stop:1 {CYAN});
        border-radius: 6px;
    }}

    /* ── Scroll Bars ── */
    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 0px;
    }}
    QScrollBar::handle:vertical {{
        background: {BORDER};
        border-radius: 4px;
        min-height: 24px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {HIGHLIGHT};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar:horizontal {{
        background: transparent;
        height: 8px;
        margin: 0px;
    }}
    QScrollBar::handle:horizontal {{
        background: {BORDER};
        border-radius: 4px;
        min-width: 24px;
    }}

    /* ── Splitter ── */
    QSplitter::handle {{
        background-color: transparent;
    }}

    /* ── Tab Widget ── */
    QTabWidget::pane {{
        background-color: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 16px;
        border-top-left-radius: 0px;
        top: -1px;
    }}
    QTabBar {{
        background: transparent;
    }}
    QTabBar::tab {{
        background-color: {BG};
        color: {MUTED};
        border: 1px solid {BORDER};
        border-bottom: none;
        border-radius: 10px;
        border-bottom-left-radius: 0px;
        border-bottom-right-radius: 0px;
        padding: 9px 22px;
        margin-right: 4px;
        font-weight: 700;
        font-size: {FONT_SM}px;
        letter-spacing: 0.5px;
        min-width: 130px;
    }}
    QTabBar::tab:selected {{
        background-color: {SURFACE};
        color: {TEXT};
        border-bottom: 2px solid {INDIGO};
    }}
    QTabBar::tab:hover:!selected {{
        background-color: {SURFACE2};
        color: {TEXT};
    }}
    """


def cell_color(value: int) -> str:
    """
    Returns the BACKGROUND colour for a payoff cell.
    All cells use the same flat dark surface — colour distinction
    is handled via text colour (red/green) in PayoffMatrixWidget,
    matching the screenshot style.
    """
    return SURFACE


def cell_text_color(value: int) -> str:

    if value > 0:
        return GREEN
    elif value < 0:
        return RED
    else:
        return MUTED


PLACE_COLORS: dict[str, str] = {
    "P": GREEN,
    "H": AMBER,
    "S": INDIGO,
    "D": RED,
    "F": GREEN,
    "C": MUTED,
    "B": CYAN,
    "M": "#8B5CF6",
    "V": "#10B981",
    "R": "#0EA5E9",
    # Neutral / Easy / Hard type codes (if Member 1 uses these)
    "N": MUTED,     # Neutral
    "E": CYAN,      # Easy for seeker
    "X": AMBER,     # Hard for seeker
}

PLACE_LABELS: dict[str, str] = {
    "P": "Park",
    "H": "House",
    "S": "Shop",
    "D": "Danger",
    "F": "Forest",
    "C": "Cave",
    "B": "Beach",
    "M": "Mountain",
    "V": "Valley",
    "R": "River",
    "N": "Neutral",
    "E": "Easy",
    "X": "Hard",
}

def difficulty_name(place_type: str) -> str:
    """Map place type code to difficulty name."""
    # Backend PlaceType enum values: "Easy", "Neutral", "Hard"
    # UI codes: B=Beach, V=Valley, F=Forest
    easy_types = {"B", "P", "E"}
    hard_types = {"M", "D", "X", "F"}
    if place_type in easy_types:
        return "Easy"
    elif place_type in hard_types:
        return "Hard"
    return "Neutral"

def difficulty_color(place_type: str) -> str:
    """Return the accent color for the given place type's difficulty."""
    return DIFFICULTY_COLORS[difficulty_name(place_type)]

def difficulty_label(place_type: str) -> str:
    """Return the short badge string for the given place type's difficulty."""
    return difficulty_name(place_type)