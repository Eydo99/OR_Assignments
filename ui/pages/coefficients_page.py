from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea,
    QDoubleSpinBox, QComboBox, QGridLayout)
from PySide6.QtCore import Qt, Signal


# ── Shared stylesheet tokens ──
CARD_STYLE = """
    QFrame#coeffCard {
        background-color: #16213e;
        border: 1px solid #0f3460;
        border-radius: 10px;
        padding: 8px;
    }
"""

LABEL_STYLE = "color: #e2e8f0; font-size: 13px; border: none; background: transparent;"
TITLE_STYLE = "color: #e2e8f0; font-size: 14px; font-weight: 600; border: none; background: transparent;"
HINT_STYLE = "color: #4a5568; font-size: 11px; border: none; background: transparent;"

SPINBOX_STYLE = """
    QDoubleSpinBox {
        background-color: #0f3460;
        color: #e2e8f0;
        border: 1px solid #1a4a8a;
        border-radius: 6px;
        padding: 5px 8px;
        font-size: 12px;
        min-width: 65px;
    }
    QDoubleSpinBox:focus {
        border: 1px solid #4f9cf9;
    }
    QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
        background-color: #1a4a8a;
        border: none;
        width: 16px;
    }
    QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
        background-color: #4f9cf9;
    }
"""

COMBO_STYLE = """
    QComboBox {
        background-color: #0f3460;
        color: #e2e8f0;
        border: 1px solid #1a4a8a;
        border-radius: 6px;
        padding: 5px 8px;
        font-size: 12px;
        min-width: 55px;
    }
    QComboBox:focus {
        border: 1px solid #4f9cf9;
    }
    QComboBox::drop-down {
        border: none;
        background-color: #0f3460;
    }
    QComboBox QAbstractItemView {
        background-color: #16213e;
        color: #e2e8f0;
        selection-background-color: #0f3460;
        border: 1px solid #1a4a8a;
    }
"""


class CoefficientsPage(QWidget):
    """Page 1 – Enter objective function coefficients and constraint matrix."""

    data_changed = Signal(dict)

    def __init__(self):
        super().__init__()
        self._num_vars = 1
        self._num_constraints = 1

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

        self._container = QWidget()
        self._container.setStyleSheet("background: transparent;")
        scroll.setWidget(self._container)

        self._layout = QVBoxLayout(self._container)
        self._layout.setContentsMargins(28, 24, 28, 28)
        self._layout.setSpacing(16)

        # ── Section header (matches Problem Setup / Solution style) ──
        header = QLabel("COEFFICIENTS")
        header.setStyleSheet("""
            color: #4f9cf9;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
        """)
        self._layout.addWidget(header)

        # Placeholders for cards
        self._obj_card = None
        self._constraints_card = None
        self._obj_spins = []
        self._constraint_spins = []   # list of lists
        self._constraint_types = []   # list of QComboBox
        self._rhs_spins = []          # list of QDoubleSpinBox

        self.rebuild(self._num_vars, self._num_constraints)

    # ────────────────────────────────────
    # Public API
    # ────────────────────────────────────
    def rebuild(self, num_vars, num_constraints):
        """Tear down and recreate the coefficient input cards."""
        self._num_vars = num_vars
        self._num_constraints = num_constraints

        # Remove every layout item after the header (index 0)
        while self._layout.count() > 1:
            item = self._layout.takeAt(1)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self._obj_card = None
        self._constraints_card = None
        self._obj_spins.clear()
        self._constraint_spins.clear()
        self._constraint_types.clear()
        self._rhs_spins.clear()

        self._build_obj_card()
        self._build_constraints_card()
        self._layout.addStretch()


    def get_data(self):
        """Return a dict with obj_fn_values, constraints (LHS, type, RHS)."""
        obj_vals = [s.value() for s in self._obj_spins]
        constraints = []
        for i in range(self._num_constraints):
            lhs = [self._constraint_spins[i][j].value() for j in range(self._num_vars)]
            c_type = self._constraint_types[i].currentText()
            rhs = self._rhs_spins[i].value()
            constraints.append({"LHS": lhs, "constraint_type": c_type, "RHS": rhs})
        return {"obj_fn_values": obj_vals, "constraints": constraints}

    def reset(self):
        """Clear all spinboxes to 0."""
        for s in self._obj_spins:
            s.blockSignals(True)
            s.setValue(0)
            s.blockSignals(False)
        for row in self._constraint_spins:
            for s in row:
                s.blockSignals(True)
                s.setValue(0)
                s.blockSignals(False)
        for c in self._constraint_types:
            c.blockSignals(True)
            c.setCurrentIndex(0)
            c.blockSignals(False)
        for s in self._rhs_spins:
            s.blockSignals(True)
            s.setValue(0)
            s.blockSignals(False)
        self._emit_data_changed()

    def _emit_data_changed(self, *_):
        self.data_changed.emit(self.get_data())

    # ────────────────────────────────────
    # Internal builders
    # ────────────────────────────────────
    def _make_spinbox(self):
        spin = QDoubleSpinBox()
        spin.setRange(-9999, 9999)
        spin.setDecimals(2)
        spin.setValue(0)
        spin.setStyleSheet(SPINBOX_STYLE)
        return spin

    def _make_combo(self):
        combo = QComboBox()
        combo.addItems(["<=", ">=", "="])
        combo.setStyleSheet(COMBO_STYLE)
        return combo

    def _build_obj_card(self):
        card = QFrame()
        card.setObjectName("coeffCard")
        card.setStyleSheet(CARD_STYLE)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)

        title = QLabel("Objective Function Coefficients")
        title.setStyleSheet(TITLE_STYLE)
        card_layout.addWidget(title)

        hint = QLabel("Enter the coefficients for Z = c₁x₁ + c₂x₂ + …")
        hint.setStyleSheet(HINT_STYLE)
        card_layout.addWidget(hint)

        row = QHBoxLayout()
        row.setSpacing(12)
        for i in range(self._num_vars):
            lbl = QLabel(f"x<sub>{i + 1}</sub>")
            lbl.setStyleSheet(LABEL_STYLE)
            lbl.setAlignment(Qt.AlignCenter)
            col = QVBoxLayout()
            col.setSpacing(4)
            col.addWidget(lbl, alignment=Qt.AlignCenter)
            spin = self._make_spinbox()
            spin.valueChanged.connect(self._emit_data_changed)
            col.addWidget(spin)
            self._obj_spins.append(spin)
            row.addLayout(col)
        row.addStretch()
        card_layout.addLayout(row)

        self._obj_card = card
        self._layout.addWidget(card)

    def _build_constraints_card(self):
        card = QFrame()
        card.setObjectName("coeffCard")
        card.setStyleSheet(CARD_STYLE)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)

        title = QLabel("Constraint Coefficients")
        title.setStyleSheet(TITLE_STYLE)
        card_layout.addWidget(title)

        hint = QLabel("Enter coefficients for each constraint row, select type, and RHS value")
        hint.setStyleSheet(HINT_STYLE)
        card_layout.addWidget(hint)

        # ── Header labels ──
        grid = QGridLayout()
        grid.setSpacing(8)

        # Header row
        header_style = "color: #4f9cf9; font-size: 11px; font-weight: 600; border: none; background: transparent;"
        for j in range(self._num_vars):
            h = QLabel(f"x<sub>{j + 1}</sub>")
            h.setStyleSheet(header_style)
            h.setAlignment(Qt.AlignCenter)
            grid.addWidget(h, 0, j)
        type_h = QLabel("Type")
        type_h.setStyleSheet(header_style)
        type_h.setAlignment(Qt.AlignCenter)
        grid.addWidget(type_h, 0, self._num_vars)
        rhs_h = QLabel("RHS")
        rhs_h.setStyleSheet(header_style)
        rhs_h.setAlignment(Qt.AlignCenter)
        grid.addWidget(rhs_h, 0, self._num_vars + 1)

        # Data rows
        for i in range(self._num_constraints):
            row_spins = []
            for j in range(self._num_vars):
                spin = self._make_spinbox()
                spin.valueChanged.connect(self._emit_data_changed)
                grid.addWidget(spin, i + 1, j)
                row_spins.append(spin)
            self._constraint_spins.append(row_spins)

            combo = self._make_combo()
            combo.currentIndexChanged.connect(self._emit_data_changed)
            grid.addWidget(combo, i + 1, self._num_vars)
            self._constraint_types.append(combo)

            rhs = self._make_spinbox()
            rhs.setRange(-99999, 99999)
            rhs.valueChanged.connect(self._emit_data_changed)
            grid.addWidget(rhs, i + 1, self._num_vars + 1)
            self._rhs_spins.append(rhs)

        card_layout.addLayout(grid)

        self._constraints_card = card
        self._layout.addWidget(card)
