from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QFrame, QPushButton
from PySide6.QtCore import Qt


class RestrictionsCard(QFrame):
    """Card for toggling variable restrictions (non-negative / free)."""

    def __init__(self, num_variables=3):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border: 1px solid #0f3460;
                border-radius: 10px;
                padding: 8px;
            }
        """)

        self._main_layout = QVBoxLayout(self)
        self._main_layout.setSpacing(12)

        title = QLabel("Variable restrictions")
        title.setStyleSheet("""
            color: #e2e8f0;
            font-size: 14px;
            font-weight: 600;
            border: none;
            background: transparent;
        """)
        self._main_layout.addWidget(title)

        self.pills_layout = QHBoxLayout()
        self.pills_layout.setSpacing(8)
        self._main_layout.addLayout(self.pills_layout)

        self.buttons = []
        self.states = []

        for i in range(num_variables):
            self._add_pill(i)

        self._stretch = None
        self._add_stretch()

        hint = QLabel("Click to toggle between non-negative / unrestricted")
        hint.setStyleSheet("""
            color: #4a5568;
            font-size: 11px;
            border: none;
            background: transparent;
        """)
        self._main_layout.addWidget(hint)

    def _add_pill(self, i):
        btn = QPushButton(f"x{i + 1} ≥ 0")
        btn.setCheckable(True)
        btn.setChecked(False)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(26, 58, 110, 0.7);
                color: #4f9cf9;
                border: 1px solid #4f9cf9;
                border-radius: 14px;
                padding: 5px 14px;
                font-size: 11px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(26, 58, 110, 1.0);
            }
            QPushButton:checked {
                background-color: rgba(45, 27, 105, 0.7);
                color: #a78bfa;
                border: 1px solid #a78bfa;
            }
            QPushButton:checked:hover {
                background-color: rgba(45, 27, 105, 1.0);
            }
        """)
        btn.clicked.connect(lambda checked, b=btn, idx=i: self._toggle(b, idx))
        self.pills_layout.addWidget(btn)
        self.buttons.append(btn)
        self.states.append(False)

    def _add_stretch(self):
        self._stretch = self.pills_layout.addStretch()

    def _toggle(self, btn, idx):
        self.states[idx] = not self.states[idx]
        if self.states[idx]:
            btn.setText(f"x{idx + 1} free")
        else:
            btn.setText(f"x{idx + 1} ≥ 0")

    def update_pills(self, num_variables):
        """Rebuild the pill buttons for a new variable count."""
        # Remove all items from pills_layout
        while self.pills_layout.count():
            item = self.pills_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.buttons.clear()
        self.states.clear()

        for i in range(num_variables):
            self._add_pill(i)

        self._add_stretch()
