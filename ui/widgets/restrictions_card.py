from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QFrame, QPushButton


class RestrictionsCard(QFrame):
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

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(12)

        title = QLabel("Variable restrictions")
        title.setStyleSheet("color: #e2e8f0; font-size: 13px; font-weight: 600; border: none; background: transparent;")
        self.layout.addWidget(title)

        self.pills_layout = QHBoxLayout()
        self.pills_layout.setSpacing(8)
        self.layout.addLayout(self.pills_layout)

        self.buttons = []
        self.states = []

        for i in range(num_variables):
            self._add_pill(i)

        self.pills_layout.addStretch()

        hint = QLabel("Click to toggle between non-negative / unrestricted")
        hint.setStyleSheet("color: #4a5568; font-size: 11px; border: none; background: transparent;")
        self.layout.addWidget(hint)

    def _add_pill(self, i):
        btn = QPushButton(f"x{i + 1} ≥ 0")
        btn.setCheckable(True)
        btn.setChecked(False)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #1a3a6e;
                color: #4f9cf9;
                border: 1px solid #4f9cf9;
                border-radius: 12px;
                padding: 4px 12px;
                font-size: 11px;
            }
            QPushButton:checked {
                background-color: #2d1b69;
                color: #a78bfa;
                border: 1px solid #a78bfa;
            }
        """)
        btn.clicked.connect(lambda checked, b=btn, idx=i: self._toggle(b, idx))
        self.pills_layout.addWidget(btn)
        self.buttons.append(btn)
        self.states.append(False)

    def _toggle(self, btn, idx):
        self.states[idx] = not self.states[idx]
        if self.states[idx]:
            btn.setText(f"x{idx + 1} free")
        else:
            btn.setText(f"x{idx + 1} ≥ 0")

    def update_pills(self, num_variables):
        for btn in self.buttons:
            btn.deleteLater()
        self.buttons.clear()
        self.states.clear()
        for i in range(num_variables):
            self._add_pill(i)

