from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea, QHBoxLayout,
    QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class TableauStepsPage(QWidget):
    """Page 3 – Shows step-by-step simplex tableau iterations.
    Currently a placeholder; `show_steps(steps)` will be wired
    after the solver logic is implemented."""

    def __init__(self):
        super().__init__()

        # ── Scroll wrapper ──
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical {
                background: #0d1b2a; width: 8px; border: none;
            }
            QScrollBar::handle:vertical {
                background: #1a4a8a; border-radius: 4px; min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        outer.addWidget(scroll)

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        scroll.setWidget(container)

        self._layout = QVBoxLayout(container)
        self._layout.setContentsMargins(28, 28, 28, 28)
        self._layout.setSpacing(20)

        # ── Section header ──
        header = QLabel("TABLEAU STEPS")
        header.setStyleSheet("""
            color: #4f9cf9;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2.5px;
        """)
        self._layout.addWidget(header)

        # ── Placeholder card ──
        self._placeholder_card = self._build_placeholder()
        self._layout.addWidget(self._placeholder_card)

        # ── Step cards container ──
        self._steps_container = QWidget()
        self._steps_container.setStyleSheet("background: transparent;")
        self._steps_layout = QVBoxLayout(self._steps_container)
        self._steps_layout.setContentsMargins(0, 0, 0, 0)
        self._steps_layout.setSpacing(16)
        self._steps_container.hide()
        self._layout.addWidget(self._steps_container)

        self._layout.addStretch()

    def _build_placeholder(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border: 1px solid #0f3460;
                border-radius: 10px;
                padding: 40px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(16)

        icon_label = QLabel("📋")
        icon_label.setStyleSheet("font-size: 40px; border: none; background: transparent;")
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)

        msg = QLabel("No tableau steps yet")
        msg.setStyleSheet("""
            color: #e2e8f0;
            font-size: 16px;
            font-weight: 600;
            border: none;
            background: transparent;
        """)
        msg.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(msg)

        sub = QLabel("Tableau iterations will appear here step-by-step after you solve a problem.")
        sub.setStyleSheet("""
            color: #718096;
            font-size: 12px;
            border: none;
            background: transparent;
        """)
        sub.setAlignment(Qt.AlignCenter)
        sub.setWordWrap(True)
        card_layout.addWidget(sub)

        return card

    # ── Public API (stub) ──
    def show_steps(self, steps: list):
        """Display a list of tableau iteration dicts.
        Each step dict is expected to have:
          - iteration: int
          - headers: list[str]
          - rows: list[list[str]]
          - pivot: (row, col) or None
        """
        self._clear_steps()
        self._placeholder_card.hide()
        self._steps_container.show()

        for step in steps:
            card = self._build_step_card(step)
            self._steps_layout.addWidget(card)

    def _build_step_card(self, step):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border: 1px solid #0f3460;
                border-radius: 10px;
                padding: 16px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)

        iteration = step.get("iteration", "?")
        title = QLabel(f"Iteration {iteration}")
        title.setStyleSheet("""
            color: #4f9cf9;
            font-size: 13px;
            font-weight: 600;
            border: none;
            background: transparent;
        """)
        card_layout.addWidget(title)

        info = QLabel("Tableau data will be rendered here.")
        info.setStyleSheet("""
            color: #718096;
            font-size: 12px;
            border: none;
            background: transparent;
        """)
        card_layout.addWidget(info)

        return card

    def _clear_steps(self):
        while self._steps_layout.count():
            item = self._steps_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def reset(self):
        """Hide steps, show placeholder again."""
        self._clear_steps()
        self._steps_container.hide()
        self._placeholder_card.show()
