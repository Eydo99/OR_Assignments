

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor, QMouseEvent

from ui import theme


class ClickableCard(QFrame):

    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    # After children are added, make them all transparent to mouse so
    # clicks reach this frame's mousePressEvent.
    def _seal_children(self):
        for child in self.findChildren(QWidget):
            child.setAttribute(Qt.WA_TransparentForMouseEvents, True)


class SetupPage(QWidget):
    # Signal: (world_size, role, mode, dimension)
    setup_complete = Signal(int, str, str, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SetupPage")

        self.world_size         = 5
        self.selected_role      = None
        self.selected_mode      = "Interactive"
        self.selected_dimension = 1   # 1 = 1D strip, 2 = 2D grid

        self._build_ui()
        self._refresh_state()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        title = QLabel("Initialize Hide & Seek\nSimulation")
        title.setAlignment(Qt.AlignCenter)
        title.setProperty("class", "page-title")

        subtitle = QLabel("Configure your tactical parameters")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setProperty("class", "page-subtitle")

        main_layout.addWidget(title)
        main_layout.addSpacing(6)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(32)

        # ── World Size (N) ──────────────────────────
        size_section_lbl = QLabel("WORLD SIZE (N)")
        size_section_lbl.setAlignment(Qt.AlignCenter)
        size_section_lbl.setProperty("class", "section-label")
        main_layout.addWidget(size_section_lbl)
        main_layout.addSpacing(12)

        size_card = QFrame()
        size_card.setProperty("class", "size-container")
        size_card.setFixedSize(240, 76)

        size_card_lay = QHBoxLayout(size_card)
        size_card_lay.setContentsMargins(14, 12, 14, 12)
        size_card_lay.setSpacing(0)

        self.btn_minus = QPushButton("−")
        self.btn_minus.setProperty("class", "stepper-btn")
        self.btn_minus.setFixedSize(40, 40)
        self.btn_minus.setCursor(Qt.PointingHandCursor)
        self.btn_minus.clicked.connect(self._decrease_n)

        val_lay = QVBoxLayout()
        val_lay.setSpacing(0)
        val_lay.setAlignment(Qt.AlignCenter)

        self.lbl_n = QLabel(str(self.world_size))
        self.lbl_n.setAlignment(Qt.AlignCenter)
        self.lbl_n.setProperty("class", "cyan-number")

        self.lbl_locations = QLabel("locations  (2 – 20)")
        self.lbl_locations.setAlignment(Qt.AlignCenter)
        self.lbl_locations.setStyleSheet(
            f"color: {theme.MUTED2}; font-size: 10px; background: transparent;"
        )

        val_lay.addWidget(self.lbl_n)
        val_lay.addWidget(self.lbl_locations)

        self.btn_plus = QPushButton("+")
        self.btn_plus.setProperty("class", "stepper-btn")
        self.btn_plus.setFixedSize(40, 40)
        self.btn_plus.setCursor(Qt.PointingHandCursor)
        self.btn_plus.clicked.connect(self._increase_n)

        size_card_lay.addWidget(self.btn_minus)
        size_card_lay.addStretch()
        size_card_lay.addLayout(val_lay)
        size_card_lay.addStretch()
        size_card_lay.addWidget(self.btn_plus)

        main_layout.addWidget(size_card, alignment=Qt.AlignCenter)
        main_layout.addSpacing(24)

        dim_widget = QWidget()
        dim_widget.setFixedWidth(520)
        dim_layout = QVBoxLayout(dim_widget)
        dim_layout.setContentsMargins(0, 0, 0, 0)
        dim_layout.setSpacing(12)

        dim_lbl = QLabel("WORLD DIMENSION")
        dim_lbl.setProperty("class", "section-label")
        dim_layout.addWidget(dim_lbl)

        dim_toggle_bg = QFrame()
        dim_toggle_bg.setStyleSheet(f"""
            QFrame {{
                background: {theme.SURFACE};
                border-radius: 14px;
                border: 1px solid {theme.BORDER};
            }}
        """)
        dim_toggle_bg.setFixedHeight(54)

        dim_t_lay = QHBoxLayout(dim_toggle_bg)
        dim_t_lay.setContentsMargins(6, 6, 6, 6)
        dim_t_lay.setSpacing(6)

        self.btn_dim_1d = QPushButton("1D Strip")
        self.btn_dim_1d.setCursor(Qt.PointingHandCursor)
        self.btn_dim_1d.clicked.connect(lambda: self._set_dimension(1))

        self.btn_dim_2d = QPushButton("2D Grid")
        self.btn_dim_2d.setCursor(Qt.PointingHandCursor)
        self.btn_dim_2d.clicked.connect(lambda: self._set_dimension(2))

        dim_t_lay.addWidget(self.btn_dim_1d)
        dim_t_lay.addWidget(self.btn_dim_2d)
        dim_layout.addWidget(dim_toggle_bg)

        main_layout.addWidget(dim_widget, alignment=Qt.AlignCenter)
        main_layout.addSpacing(24)

        # ── Choose Your Role ────────────────────────
        role_widget = QWidget()
        role_widget.setFixedWidth(520)
        role_widget.setMinimumHeight(130)
        role_layout = QVBoxLayout(role_widget)
        role_layout.setContentsMargins(0, 0, 0, 0)
        role_layout.setSpacing(12)

        role_lbl = QLabel("CHOOSE YOUR ROLE")
        role_lbl.setProperty("class", "section-label")
        role_layout.addWidget(role_lbl)

        cards_lay = QHBoxLayout()
        cards_lay.setSpacing(16)
        cards_lay.setAlignment(Qt.AlignTop)
        self.btn_hider  = self._create_role_card("🙈", "Hider",
            "Pick a hiding spot · maximize your concealment score")
        self.btn_seeker = self._create_role_card("🔍", "Seeker",
            "Search for the Hider · maximize your detection score")

        self.btn_hider.clicked.connect(lambda: self._set_role("Hider"))
        self.btn_seeker.clicked.connect(lambda: self._set_role("Seeker"))

        # Make all child labels pass mouse events through to the card frame
        self.btn_hider._seal_children()
        self.btn_seeker._seal_children()

        cards_lay.addWidget(self.btn_hider)
        cards_lay.addWidget(self.btn_seeker)
        role_layout.addLayout(cards_lay)

        main_layout.addWidget(role_widget, alignment=Qt.AlignCenter)
        main_layout.addSpacing(28)

        # ── Game Mode ───────────────────────────────
        mode_widget = QWidget()
        mode_widget.setFixedWidth(520)
        mode_layout = QVBoxLayout(mode_widget)
        mode_layout.setContentsMargins(0, 0, 0, 0)
        mode_layout.setSpacing(12)

        mode_lbl = QLabel("GAME MODE")
        mode_lbl.setProperty("class", "section-label")
        mode_layout.addWidget(mode_lbl)

        toggle_bg = QFrame()
        toggle_bg.setStyleSheet(f"""
            QFrame {{
                background: {theme.SURFACE};
                border-radius: 14px;
                border: 1px solid {theme.BORDER};
            }}
        """)
        toggle_bg.setFixedHeight(54)

        t_lay = QHBoxLayout(toggle_bg)
        t_lay.setContentsMargins(6, 6, 6, 6)
        t_lay.setSpacing(6)

        self.btn_interactive = QPushButton("⚡  Interactive  (you play)")
        self.btn_interactive.setCursor(Qt.PointingHandCursor)
        self.btn_interactive.clicked.connect(lambda: self._set_mode("Interactive"))

        self.btn_simulation = QPushButton("🤖  Auto-Sim  (100 rounds)")
        self.btn_simulation.setCursor(Qt.PointingHandCursor)
        self.btn_simulation.clicked.connect(lambda: self._set_mode("Simulation"))

        t_lay.addWidget(self.btn_interactive)
        t_lay.addWidget(self.btn_simulation)
        mode_layout.addWidget(toggle_bg)

        self._mode_hint = QLabel("")
        self._mode_hint.setAlignment(Qt.AlignCenter)
        self._mode_hint.setStyleSheet(
            f"color: {theme.MUTED2}; font-size: 10px; background: transparent;"
        )
        mode_layout.addWidget(self._mode_hint)

        main_layout.addWidget(mode_widget, alignment=Qt.AlignCenter)
        main_layout.addSpacing(36)

        # ── CTA Button ──────────────────────────────
        self.btn_continue = QPushButton("SELECT A ROLE TO CONTINUE")
        self.btn_continue.setFixedWidth(520)
        self.btn_continue.setFixedHeight(62)
        self.btn_continue.setCursor(Qt.PointingHandCursor)
        self.btn_continue.clicked.connect(self._on_continue)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(32)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(99, 102, 241, 120))
        self.btn_continue.setGraphicsEffect(shadow)

        main_layout.addWidget(self.btn_continue, alignment=Qt.AlignCenter)
        main_layout.addStretch()

    def _create_role_card(self, icon: str, title: str, subtitle: str) -> ClickableCard:
        """
        Returns a ClickableCard (QFrame subclass with a .clicked Signal).
        Child widgets have WA_TransparentForMouseEvents set after construction
        via _seal_children(), so every click — on the icon, the title label,
        the subtitle label, or the background — reaches the card's
        mousePressEvent and emits .clicked.
        """
        card = ClickableCard()
        card.setFixedSize(252, 120)
        card.setCursor(Qt.PointingHandCursor)
        card.setObjectName("RoleCard")

        card._style_inactive = f"""
            QFrame#RoleCard {{
                background-color: {theme.SURFACE};
                border: 1.5px solid {theme.BORDER};
                border-radius: 16px;
            }}
            QFrame#RoleCard:hover {{
                background-color: #263245;
                border: 1.5px solid {theme.HIGHLIGHT};
            }}
        """
        card._style_active = f"""
            QFrame#RoleCard {{
                background-color: rgba(99, 102, 241, 0.12);
                border: 2px solid {theme.INDIGO};
                border-radius: 16px;
            }}
        """
        card.setStyleSheet(card._style_inactive)

        lay = QVBoxLayout(card)
        lay.setAlignment(Qt.AlignCenter)
        lay.setSpacing(6)
        lay.setContentsMargins(12, 12, 12, 12)

        icon_box = QFrame()
        icon_box.setFixedSize(38, 38)
        icon_box.setStyleSheet(
            f"background: {theme.SURFACE2}; border-radius: 10px; border: none;"
        )
        icon_box_lay = QHBoxLayout(icon_box)
        icon_box_lay.setContentsMargins(0, 0, 0, 0)

        icon_lbl = QLabel(icon)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setFont(QFont(theme.FONT_UI, 16))
        icon_lbl.setStyleSheet("background: transparent; border: none;")
        icon_box_lay.addWidget(icon_lbl)

        title_lbl = QLabel(title)
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setFont(QFont(theme.FONT_UI, 13, QFont.Weight.Bold))
        title_lbl.setStyleSheet(
            f"background: transparent; color: {theme.TEXT}; border: none;"
        )

        lay.addWidget(icon_box, alignment=Qt.AlignCenter)
        lay.addWidget(title_lbl)

        return card

    # ── Logic ──────────────────────────────────

    def _decrease_n(self):
        if self.world_size > 2:
            self.world_size -= 1
            self.lbl_n.setText(str(self.world_size))
            self._refresh_state()

    def _increase_n(self):
        if self.world_size < 20:
            self.world_size += 1
            self.lbl_n.setText(str(self.world_size))
            self._refresh_state()

    def _set_role(self, role: str):
        self.selected_role = role
        self._refresh_state()

    def _set_mode(self, mode: str):
        self.selected_mode = mode
        self._refresh_state()

    def _set_dimension(self, dim: int):
        self.selected_dimension = dim
        self._refresh_state()

    def _refresh_state(self):
        # ── Role cards ──
        for card, role in ((self.btn_hider, "Hider"), (self.btn_seeker, "Seeker")):
            if self.selected_role == role:
                card.setStyleSheet(card._style_active)
            else:
                card.setStyleSheet(card._style_inactive)

        # ── Mode toggle ──
        if self.selected_mode == "Interactive":
            self.btn_interactive.setProperty("class", "toggle-on")
            self.btn_simulation.setProperty("class", "toggle-off")
            self._mode_hint.setText(
                "You choose a location each round — vs. the Nash-optimal AI opponent"
            )
        else:
            self.btn_interactive.setProperty("class", "toggle-off")
            self.btn_simulation.setProperty("class", "toggle-on")
            self._mode_hint.setText(
                "Both sides play their mixed strategy automatically for 100 rounds"
            )

        for btn in (self.btn_interactive, self.btn_simulation):
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # ── Dimension toggle ──
        if self.selected_dimension == 1:
            self.btn_dim_1d.setProperty("class", "toggle-on")
            self.btn_dim_2d.setProperty("class", "toggle-off")
            self.lbl_locations.setText("locations  (2 – 20)")
        else:
            self.btn_dim_1d.setProperty("class", "toggle-off")
            self.btn_dim_2d.setProperty("class", "toggle-on")
            n = self.world_size
            self.lbl_locations.setText(f"{n} × {n} grid  =  {n*n} cells")

        for btn in (self.btn_dim_1d, self.btn_dim_2d):
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # ── CTA ──
        if self.selected_role:
            icon = "🙈" if self.selected_role == "Hider" else "🔍"
            self.btn_continue.setText(
                f"{icon}  PLAY AS {self.selected_role.upper()}  ·  ENTER WAR ROOM"
            )
            self.btn_continue.setStyleSheet(f"""
                QPushButton {{
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {theme.INDIGO}, stop:1 {theme.INDIGO_D});
                    color: {theme.TEXT};
                    border: none;
                    border-radius: 14px;
                    font-weight: 800;
                    font-size: 15px;
                    letter-spacing: 1.5px;
                }}
                QPushButton:hover {{
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #818CF8, stop:1 {theme.INDIGO});
                }}
                QPushButton:pressed {{
                    background-color: {theme.INDIGO_D};
                }}
            """)
            self.btn_continue.setEnabled(True)
        else:
            self.btn_continue.setText("SELECT A ROLE TO CONTINUE")
            self.btn_continue.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {theme.MUTED2};
                    border: 1.5px dashed {theme.BORDER};
                    border-radius: 14px;
                    font-weight: 700;
                    font-size: 14px;
                    letter-spacing: 1px;
                }}
            """)
            self.btn_continue.setEnabled(False)

    def _on_continue(self):
        self.setup_complete.emit(
            self.world_size,
            self.selected_role,
            self.selected_mode,
            self.selected_dimension,
        )