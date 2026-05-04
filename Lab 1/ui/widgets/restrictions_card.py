from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QFrame, QPushButton
from PySide6.QtCore import Qt


class RestrictionsCard(QFrame):
    """Card for toggling variable restrictions (non-negative / free)."""

    def __init__(self, num_variables=3):
        super().__init__()
        self.setObjectName("CardFrame")

        self._main_layout = QVBoxLayout(self)
        self._main_layout.setSpacing(12)

        title = QLabel("Variable restrictions")
        title.setObjectName("CardTitle")
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
        hint.setObjectName("CardHint")
        self._main_layout.addWidget(hint)

    def _add_pill(self, i):
        btn = QPushButton(f"x{i + 1} ≥ 0")
        btn.setCheckable(True)
        btn.setChecked(False)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setObjectName("PillBtn")
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
