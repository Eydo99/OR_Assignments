from PySide6.QtWidgets import QComboBox, QSpinBox, QHBoxLayout, QLabel, QVBoxLayout, QFrame
from PySide6.QtCore import Qt


class ConfigCard(QFrame):
    """Configuration card: objective type, variable count, and constraint count."""

    def __init__(self):
        super().__init__()
        self.setObjectName("CardFrame")

        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        title = QLabel("Configuration")
        title.setObjectName("CardTitle")
        layout.addWidget(title)

        self.obj_combo = self._make_combo(["Maximize", "Minimize"])
        self.variables_spin = self._make_spinbox(value=3)
        self.constraints_spin = self._make_spinbox(value=2)

        for label_text, widget in [
            ("Objective type", self.obj_combo),
            ("Variables", self.variables_spin),
            ("Constraints", self.constraints_spin),
        ]:
            row = QHBoxLayout()
            label = QLabel(label_text)
            label.setObjectName("StandardLabel")
            label.setFixedWidth(130)
            row.addWidget(label)
            row.addWidget(widget)
            row.addStretch()
            layout.addLayout(row)

    def _make_combo(self, items):
        combo = QComboBox()
        combo.setCursor(Qt.PointingHandCursor)
        for item in items:
            combo.addItem(item)
        return combo

    def _make_spinbox(self, value=1):
        spin = QSpinBox()
        spin.setMinimum(1)
        spin.setMaximum(20)
        spin.setValue(value)
        spin.setFixedWidth(70)
        return spin
