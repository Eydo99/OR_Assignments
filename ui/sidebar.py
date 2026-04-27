from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        self.setAutoFillBackground(True)

        palette = self.palette()
        from PySide6.QtGui import QColor
        palette.setColor(self.backgroundRole(), QColor("#16213e"))
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(0)

        self.buttons = []
        items = ["Problem Setup", "Coefficients", "Solution", "Tableau Steps"]

        for item in items:
            btn = QPushButton(item)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #718096;
                    border: none;
                    padding: 12px 16px;
                    text-align: left;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #0f3460;
                    color: #e2e8f0;
                }
            """)
            layout.addWidget(btn)
            self.buttons.append(btn)

        layout.addStretch()
