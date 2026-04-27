from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea, QHBoxLayout,
    QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class SolutionPage(QWidget):
    """Page 2 – Displays the optimal solution after solving.
    Currently a placeholder; `show_solution(data)` will be wired after
    the solver logic is implemented."""

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
        header = QLabel("SOLUTION")
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

        # ── Results card (hidden by default) ──
        self._results_card = None

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

        icon_label = QLabel("📊")
        icon_label.setStyleSheet("font-size: 40px; border: none; background: transparent;")
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)

        msg = QLabel("No solution yet")
        msg.setStyleSheet("""
            color: #e2e8f0;
            font-size: 16px;
            font-weight: 600;
            border: none;
            background: transparent;
        """)
        msg.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(msg)

        sub = QLabel("Configure your problem and click Solve to see the optimal solution here.")
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

    # ── Public API (stub – to be wired after solver is implemented) ──
    def show_solution(self, data: dict):
        """Populate the results card from a solution dict.
        Expected keys: optimal_value, variables (list of floats).
        """
        if self._results_card is None:
            self._placeholder_card.hide()
            self._results_card = self._build_results_card(data)
            self._layout.insertWidget(1, self._results_card)
        else:
            self._results_card.deleteLater()
            self._results_card = self._build_results_card(data)
            self._layout.insertWidget(1, self._results_card)

    def _build_results_card(self, data):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border: 1px solid #0f3460;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)

        title = QLabel("Optimal Solution Found  ✓")
        title.setStyleSheet("""
            color: #68d391;
            font-size: 15px;
            font-weight: 600;
            border: none;
            background: transparent;
        """)
        card_layout.addWidget(title)

        opt_val = data.get("optimal_value", "—")
        val_label = QLabel(f"Z* = {opt_val}")
        val_label.setStyleSheet("""
            color: #e2e8f0;
            font-size: 22px;
            font-weight: 700;
            border: none;
            background: transparent;
            padding: 8px 0px;
        """)
        card_layout.addWidget(val_label)

        variables = data.get("variables", [])
        if variables:
            vars_row = QHBoxLayout()
            vars_row.setSpacing(16)
            for i, v in enumerate(variables):
                pill = QLabel(f"x{i + 1} = {v}")
                pill.setStyleSheet("""
                    color: #4f9cf9;
                    background-color: #0f3460;
                    border: 1px solid #1a4a8a;
                    border-radius: 8px;
                    padding: 6px 14px;
                    font-size: 13px;
                    font-weight: 500;
                """)
                pill.setAlignment(Qt.AlignCenter)
                vars_row.addWidget(pill)
            vars_row.addStretch()
            card_layout.addLayout(vars_row)

        return card

    def reset(self):
        """Hide results, show placeholder again."""
        if self._results_card:
            self._results_card.deleteLater()
            self._results_card = None
        self._placeholder_card.show()
