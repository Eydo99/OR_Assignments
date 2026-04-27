from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QVBoxLayout, QLabel
from ui.widgets.config_card import ConfigCard
from ui.widgets.restrictions_card import RestrictionsCard
from ui.widgets.tableau_preview_card import TableauPreviewCard


class ContentArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("contentArea")
        self.setAutoFillBackground(True)

        from PySide6.QtGui import QColor
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("#1a1a2e"))
        self.setPalette(palette)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)

        label = QLabel("Problem Setup")
        label.setStyleSheet("""
            color: #4f9cf9;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 2px;
        """)
        self.layout.addWidget(label)

        self.config_card = ConfigCard()
        self.restrictions_card = RestrictionsCard()
        self.config_card.variables_spin.valueChanged.connect(self._on_variables_changed)

        self.layout.addWidget(self.config_card)
        self.layout.addWidget(self.restrictions_card)
        self.layout.addWidget(TableauPreviewCard())

        reset_btn = QPushButton("Reset")
        reset_btn.setFixedWidth(120)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #a0aec0;
                border: 1px solid #1a4a8a;
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0f3460;
            }
        """)

        solve_btn = QPushButton("Solve →")
        solve_btn.setFixedWidth(120)
        solve_btn.setStyleSheet("""
            QPushButton {
                background-color: #4f9cf9;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #378add;
            }
        """)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(reset_btn)
        btn_row.addWidget(solve_btn)
        self.layout.addLayout(btn_row)
        self.layout.addStretch()

    def _on_variables_changed(self, value):
        self.restrictions_card.update_pills(value)