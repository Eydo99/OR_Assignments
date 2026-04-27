from PySide6.QtWidgets import QComboBox, QSpinBox, QHBoxLayout, QLabel, QVBoxLayout, QFrame
from PySide6.QtCore import Qt


class ConfigCard(QFrame):
    """Configuration card: objective type, variable count, and constraint count."""

    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border: 1px solid #0f3460;
                border-radius: 10px;
                padding: 8px;
            }
            QLabel {
                color: #cbd5e0;
                font-size: 13px;
                border: none;
                background: transparent;
            }
            QComboBox, QSpinBox {
                background-color: #0f3460;
                color: #e2e8f0;
                border: 1px solid #1a4a8a;
                border-radius: 6px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QComboBox:focus, QSpinBox:focus {
                border: 1px solid #4f9cf9;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #0f3460;
            }
            QComboBox::down-arrow {
                width: 10px;
                height: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #16213e;
                color: #e2e8f0;
                selection-background-color: #0f3460;
                border: 1px solid #1a4a8a;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #1a4a8a;
                border: none;
                width: 16px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #4f9cf9;
            }
            QSpinBox {
                selection-background-color: #1a4a8a;
                selection-color: #e2e8f0;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        title = QLabel("Configuration")
        title.setStyleSheet("""
            color: #e2e8f0;
            font-size: 14px;
            font-weight: 600;
            border: none;
            background: transparent;
        """)
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
