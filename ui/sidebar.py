from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor


class Sidebar(QWidget):
    """Left sidebar with navigation buttons and active-dot indicators."""

    section_changed = Signal(int)

    ACTIVE_STYLE = """
        QPushButton {
            background-color: rgba(15, 52, 96, 0.6);
            color: #ffffff;
            border: none;
            border-left: 3px solid #4f9cf9;
            padding: 14px 18px 14px 15px;
            text-align: left;
            font-size: 13px;
            font-weight: 600;
        }
    """

    INACTIVE_STYLE = """
        QPushButton {
            background-color: transparent;
            color: #718096;
            border: none;
            border-left: 3px solid transparent;
            padding: 14px 18px 14px 15px;
            text-align: left;
            font-size: 13px;
            font-weight: 400;
        }
        QPushButton:hover {
            background-color: rgba(15, 52, 96, 0.35);
            color: #cbd5e0;
        }
    """

    def __init__(self):
        super().__init__()
        self.setFixedWidth(220)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("#0d1b2a"))
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── App title area ──
        title_container = QWidget()
        title_container.setFixedHeight(60)
        title_container.setStyleSheet("background: transparent;")
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(18, 16, 18, 8)

        app_title = QLabel("LP Solver")
        app_title.setStyleSheet("""
            color: #4f9cf9;
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 1px;
        """)
        title_layout.addWidget(app_title)
        layout.addWidget(title_container)

        # ── Separator ──
        sep = QWidget()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #1a3050;")
        layout.addWidget(sep)

        # ── Navigation buttons ──
        self.buttons = []
        items = [
            ("●  Problem Setup",   "Problem Setup"),
            ("●  Coefficients",    "Coefficients"),
            ("●  Solution",        "Solution"),
            ("●  Tableau Steps",   "Tableau Steps"),
        ]

        for idx, (display_text, _label) in enumerate(items):
            btn = QPushButton(display_text)
            btn.setMinimumHeight(44)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, i=idx: self._on_button_clicked(i))
            layout.addWidget(btn)
            self.buttons.append(btn)

        layout.addStretch()

        # ── Footer label ──
        footer = QLabel("Operations Research")
        footer.setStyleSheet("""
            color: #4a5568;
            font-size: 10px;
            padding: 12px 18px;
            letter-spacing: 1px;
        """)
        layout.addWidget(footer)

        # Set first button active by default
        self.set_active(0)

    def _on_button_clicked(self, index):
        self.set_active(index)
        self.section_changed.emit(index)

    def set_active(self, index):
        """Highlight the button at `index` and dim the rest."""
        for i, btn in enumerate(self.buttons):
            if i == index:
                btn.setStyleSheet(self.ACTIVE_STYLE)
            else:
                btn.setStyleSheet(self.INACTIVE_STYLE)
