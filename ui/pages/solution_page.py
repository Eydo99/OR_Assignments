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
        outer.addWidget(scroll)

        container = QWidget()
        container.setObjectName("TransparentWidget")
        scroll.setWidget(container)

        self._layout = QVBoxLayout(container)
        self._layout.setContentsMargins(28, 28, 28, 28)
        self._layout.setSpacing(20)

        # ── Section header ──
        header = QLabel("SOLUTION")
        header.setObjectName("SectionHeader")
        self._layout.addWidget(header)

        # ── Placeholder card ──
        self._placeholder_card = self._build_placeholder()
        self._layout.addWidget(self._placeholder_card)

        # ── Results card (hidden by default) ──
        self._results_card = None
        self._unbounded_card = None

        self._layout.addStretch()

    def _build_placeholder(self):
        card = QFrame()
        card.setObjectName("PlaceholderCard")
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(16)

        icon_label = QLabel("📊")
        icon_label.setObjectName("IconLabel")
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)

        msg = QLabel("No solution yet")
        msg.setObjectName("PlaceholderMsg")
        msg.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(msg)

        sub = QLabel("Configure your problem and click Solve to see the optimal solution here.")
        sub.setObjectName("CardSubHint")
        sub.setAlignment(Qt.AlignCenter)
        sub.setWordWrap(True)
        card_layout.addWidget(sub)

        return card

    def show_unbounded(self):
        self._placeholder_card.hide()
        card = QFrame()
        card.setObjectName("PlaceholderCard")
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(16)

        icon_label = QLabel("⚠️")
        icon_label.setObjectName("IconLabel")
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)

        msg = QLabel("Unbounded Problem")
        msg.setObjectName("ErrorMsg")
        msg.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(msg)

        sub = QLabel("The objective function can grow infinitely. Check your constraints.")
        sub.setObjectName("CardSubHint")
        sub.setAlignment(Qt.AlignCenter)
        sub.setWordWrap(True)
        card_layout.addWidget(sub)

        self._layout.insertWidget(1, card)
        self._unbounded_card = card

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
        card.setObjectName("ResultsCard")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)

        title = QLabel("Optimal Solution Found  ✓")
        title.setObjectName("SuccessMsg")
        card_layout.addWidget(title)

        opt_val = data.get("optimal_value", "—")
        val_label = QLabel(f"Z* = {opt_val}")
        val_label.setObjectName("OptimalVal")
        card_layout.addWidget(val_label)

        variables = data.get("variables", [])
        if variables:
            vars_row = QHBoxLayout()
            vars_row.setSpacing(16)
            for i, v in enumerate(variables):
                pill = QLabel(f"x{i + 1} = {v}")
                pill.setObjectName("VariablePill")
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

        if self._unbounded_card:
            self._unbounded_card.deleteLater()
            self._unbounded_card = None

        self._placeholder_card.show()
