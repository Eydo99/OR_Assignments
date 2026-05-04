from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame)
from PySide6.QtCore import Signal, Qt

from ui.widgets.config_card import ConfigCard
from ui.widgets.restrictions_card import RestrictionsCard
from ui.widgets.tableau_preview_card import TableauPreviewCard


class ProblemSetupPage(QWidget):
    """Page 0 – Problem Setup: configuration, restrictions, and tableau preview."""

    variables_changed = Signal(int)
    constraints_changed = Signal(int)
    reset_requested = Signal()
    solve_requested = Signal()

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

        layout = QVBoxLayout(container)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(20)

        # ── Section header ──
        header = QLabel("PROBLEM SETUP")
        header.setObjectName("SectionHeader")
        layout.addWidget(header)

        # ── Cards ──
        self.config_card = ConfigCard()
        self.restrictions_card = RestrictionsCard()
        self.tableau_preview = TableauPreviewCard()

        layout.addWidget(self.config_card)
        layout.addWidget(self.restrictions_card)
        layout.addWidget(self.tableau_preview)

        # ── Action buttons ──
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setObjectName("ResetBtn")
        self.reset_btn.setFixedWidth(130)
        self.reset_btn.setFixedHeight(40)
        self.reset_btn.setCursor(Qt.PointingHandCursor)

        self.solve_btn = QPushButton("Solve →")
        self.solve_btn.setObjectName("SolveBtn")
        self.solve_btn.setFixedWidth(130)
        self.solve_btn.setFixedHeight(40)
        self.solve_btn.setCursor(Qt.PointingHandCursor)

        btn_row.addWidget(self.reset_btn)
        btn_row.addWidget(self.solve_btn)
        layout.addLayout(btn_row)
        layout.addStretch()

        # ── Internal wiring ──
        self.config_card.variables_spin.valueChanged.connect(self._on_vars_changed)
        self.config_card.constraints_spin.valueChanged.connect(self._on_constraints_changed)
        self.reset_btn.clicked.connect(self._on_reset)
        self.solve_btn.clicked.connect(lambda: self.solve_requested.emit())

    # ── Slots ──
    def _on_vars_changed(self, value):
        self.restrictions_card.update_pills(value)
        self.variables_changed.emit(value)
        self._update_tableau_preview()

    def _on_constraints_changed(self, value):
        self.constraints_changed.emit(value)
        self._update_tableau_preview()

    def _update_tableau_preview(self):
        v = self.config_card.variables_spin.value()
        c = self.config_card.constraints_spin.value()
        self.tableau_preview.rebuild_structure(v, c)

    def update_preview_data(self, coeff_data):
        v = self.config_card.variables_spin.value()
        c = self.config_card.constraints_spin.value()
        obj_type = self.config_card.obj_combo.currentText()
        self.tableau_preview.update_from_data(v, c, coeff_data, obj_type)

    def _on_reset(self):
        self.config_card.obj_combo.setCurrentIndex(0)
        self.config_card.variables_spin.setValue(1)
        self.config_card.constraints_spin.setValue(1)
        self.reset_requested.emit()

    # ── Public API ──
    def get_num_variables(self):
        return self.config_card.variables_spin.value()

    def get_num_constraints(self):
        return self.config_card.constraints_spin.value()

    def get_objective_type(self):
        text = self.config_card.obj_combo.currentText().lower()
        return "max" if text == "maximize" else "min"

    def get_restrictions(self):
        return [
            "free" if s else "non_negative"
            for s in self.restrictions_card.states
        ]
