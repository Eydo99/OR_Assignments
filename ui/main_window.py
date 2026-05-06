
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QFrame, QStackedWidget
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from ui import theme


class NavButton(QWidget):
    """Single navigation tile: large icon + small text label below."""

    clicked = Signal(int)  # emits its own index

    def __init__(self, icon: str, label: str, index: int, parent=None):
        super().__init__(parent)
        self._index = index
        self._active = False
        self.setFixedSize(80, 80)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 10, 6, 10)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignCenter)

        self._icon_lbl = QLabel(icon)
        self._icon_lbl.setAlignment(Qt.AlignCenter)
        self._icon_lbl.setFont(QFont(theme.FONT_UI, 22))

        self._text_lbl = QLabel(label)
        self._text_lbl.setAlignment(Qt.AlignCenter)
        self._text_lbl.setWordWrap(True)
        text_font = QFont(theme.FONT_UI, 8)
        text_font.setWeight(QFont.Weight.DemiBold)
        self._text_lbl.setFont(text_font)

        layout.addWidget(self._icon_lbl)
        layout.addWidget(self._text_lbl)

        self._refresh_style()

    # ── public ────────────────────────────────
    def set_active(self, active: bool):
        self._active = active
        self._refresh_style()

    # ── internal ──────────────────────────────
    def _refresh_style(self):
        if self._active:
            self.setStyleSheet(
                f"background: {theme.BG}; border: 2px solid {theme.TEXT}; border-radius: 12px;"
            )
            self._icon_lbl.setStyleSheet(
                f"color: {theme.CYAN}; background: transparent; border: none;"
            )
            self._text_lbl.setStyleSheet(
                f"color: {theme.MUTED2}; background: transparent; font-size: 10px; border: none;"
            )
        else:
            self.setStyleSheet("background: transparent; border-radius: 12px;")
            self._icon_lbl.setStyleSheet(
                f"color: {theme.MUTED}; background: transparent;"
            )
            self._text_lbl.setStyleSheet(
                f"color: {theme.MUTED}; background: transparent; font-size: 8px;"
            )

    def mousePressEvent(self, event):
        self.clicked.emit(self._index)

    def enterEvent(self, event):
        if not self._active:
            self.setStyleSheet(
                f"background: {theme.SURFACE2}; border-radius: 12px;"
            )

    def leaveEvent(self, event):
        if not self._active:
            self.setStyleSheet("background: transparent; border-radius: 12px;")



class SideNavBar(QWidget):
    """Left-side navigation rail with icon + label buttons."""

    page_requested = Signal(int)

    # (unicode icon, label)
    NAV_ITEMS = [
        ("⚙",  "Setup"),
        ("⚔",  "War Room"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(92)
        self.setStyleSheet(
            f"background: {theme.SURFACE}; border-right: 1px solid {theme.BORDER};"
        )

        self._buttons: list[NavButton] = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 20, 6, 20)
        outer.setSpacing(6)
        outer.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # ── H&S logo ──────────────────────────
        logo = QLabel("H&S")
        logo.setAlignment(Qt.AlignCenter)
        logo.setFixedHeight(36)
        logo_font = QFont(theme.FONT_MONO, 13)
        logo_font.setWeight(QFont.Weight.Bold)
        logo.setFont(logo_font)
        logo.setStyleSheet(f"color: {theme.CYAN}; background: transparent;")
        outer.addWidget(logo)

        outer.addSpacing(10)

        # ── divider ───────────────────────────
        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setFixedHeight(1)
        div.setStyleSheet(f"background: {theme.BORDER}; border: none;")
        outer.addWidget(div)

        outer.addSpacing(10)

        # ── nav buttons ───────────────────────
        for i, (icon, label) in enumerate(self.NAV_ITEMS):
            btn = NavButton(icon, label, i, self)
            btn.clicked.connect(self._on_btn_clicked)
            self._buttons.append(btn)
            outer.addWidget(btn, alignment=Qt.AlignHCenter)

        outer.addStretch()

        # activate first by default
        self._set_active(0)

    # ── public ────────────────────────────────
    def navigate_to(self, index: int):
        self._set_active(index)

    # ── internal ──────────────────────────────
    def _on_btn_clicked(self, index: int):
        self._set_active(index)
        self.page_requested.emit(index)

    def _set_active(self, index: int):
        for i, btn in enumerate(self._buttons):
            btn.set_active(i == index)



class MainWindow(QMainWindow):


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hide & Seek — Tactical Simulation")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 800)

        # ── shared state (filled by pages) ────
        self.game_state   = None
        self.world        = None    # list[dict]  [{"type": str, "score": int}]
        self.probabilities = None   # dict {"hider": [], "seeker": [], "value": float}

        self._build_ui()

    # ── UI construction ───────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # side nav
        self._nav = SideNavBar()
        self._nav.page_requested.connect(self._switch_page)
        root.addWidget(self._nav)

        # 1-px vertical separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setFixedWidth(1)
        sep.setStyleSheet(f"background: {theme.BORDER}; border: none;")
        root.addWidget(sep)

        # page stack
        self._stack = QStackedWidget()
        self._stack.setStyleSheet(f"background: {theme.BG};")
        root.addWidget(self._stack, stretch=1)

        # placeholder pages
        self._stack.addWidget(self._placeholder("⚙",  "Setup",    "Page not yet loaded"))
        self._stack.addWidget(self._placeholder("⚔",  "War Room", "Page not yet loaded"))

    # ── Page injection (called from main.py) ──
    def set_pages(self, setup_page: QWidget, war_room_page: QWidget):

        for i, real_page in enumerate([setup_page, war_room_page]):
            old = self._stack.widget(i)
            self._stack.removeWidget(old)
            old.deleteLater()
            self._stack.insertWidget(i, real_page)

        self._stack.setCurrentIndex(0)

    # ── Navigation helpers ────────────────────
    def go_to_war_room(self):
        """Navigate to War Room (called by SetupPage after world generation)."""
        self._switch_page(1)
        self._nav.navigate_to(1)

    def go_to_setup(self):
        """Navigate back to Setup."""
        self._switch_page(0)
        self._nav.navigate_to(0)

    def _switch_page(self, index: int):
        if 0 <= index < self._stack.count():
            self._stack.setCurrentIndex(index)

    # ── State helpers (called by pages) ───────
    def store_game_state(self, game_state, world: list,
                         probabilities: dict | None = None):
        """
        Persist shared state from SetupPage.
        game_state   — utils.game_state.GameState instance
        world        — [{"type": str, "score": int}, ...]
        probabilities— optional; set later via store_probabilities()
        """
        self.game_state    = game_state
        self.world         = world
        self.probabilities = probabilities

    def store_probabilities(self, hider_probs: list,
                            seeker_probs: list, game_value: float):
        """Persist LP solve results (called by War Room / Solve section)."""
        self.probabilities = {
            "hider":  hider_probs,
            "seeker": seeker_probs,
            "value":  game_value,
        }

    # ── Internal helpers ─────────────────────
    @staticmethod
    def _placeholder(icon: str, name: str, hint: str) -> QWidget:
        w = QWidget()
        w.setStyleSheet(f"background: {theme.BG};")

        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignCenter)
        lay.setSpacing(12)

        icon_lbl = QLabel(icon)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setFont(QFont(theme.FONT_UI, 48))
        icon_lbl.setStyleSheet(f"color: {theme.MUTED}; background: transparent;")

        name_lbl = QLabel(name)
        name_lbl.setAlignment(Qt.AlignCenter)
        name_lbl.setFont(QFont(theme.FONT_UI, 18, QFont.Weight.Bold))
        name_lbl.setStyleSheet(f"color: {theme.MUTED}; background: transparent;")

        hint_lbl = QLabel(hint)
        hint_lbl.setAlignment(Qt.AlignCenter)
        hint_lbl.setStyleSheet(
            f"color: {theme.MUTED}; font-size: {theme.FONT_SM}px; background: transparent;"
        )

        lay.addWidget(icon_lbl)
        lay.addWidget(name_lbl)
        lay.addWidget(hint_lbl)
        return w
