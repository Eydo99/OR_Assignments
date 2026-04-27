from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem, QLabel, QTableWidget, QHeaderView, QVBoxLayout, QFrame


class TableauPreviewCard(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border: 1px solid #0f3460;
                border-radius: 10px;
                padding: 8px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("Tableau preview")
        title.setStyleSheet("color: #e2e8f0; font-size: 13px; font-weight: 600; border: none; background: transparent;")
        layout.addWidget(title)

        self.table = QTableWidget(3, 7)
        self.table.setHorizontalHeaderLabels(["Basis", "x1", "x2", "x3", "s1", "s2", "RHS"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #0f3460;
                color: #e2e8f0;
                border: none;
                font-size: 12px;
                font-family: monospace;
                gridline-color: #1a4a8a;
            }
            QHeaderView::section {
                background-color: #0f3460;
                color: #4f9cf9;
                padding: 5px;
                border: none;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 5px;
                text-align: center;
            }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setMinimumHeight(35)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        data = [
            ["s₁", "6", "4", "2", "1", "0", "240"],
            ["s₂", "3", "2", "5", "0", "1", "270"],
            ["Z",  "-5", "-4", "-3", "0", "0", "0"],
        ]

        for row, rowdata in enumerate(data):
            for col, val in enumerate(rowdata):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                if row == 2:
                    item.setForeground(__import__('PySide6.QtGui', fromlist=['QColor']).QColor("#f6ad55"))
                if row == 0 and col == 1:
                    item.setBackground(__import__('PySide6.QtGui', fromlist=['QColor']).QColor("#2d3a1e"))
                    item.setForeground(__import__('PySide6.QtGui', fromlist=['QColor']).QColor("#68d391"))
                self.table.setItem(row, col, item)

        self.table.setFixedHeight(160)
        layout.addWidget(self.table)

        hint = QLabel("Pivot cell highlighted in green")
        hint.setStyleSheet("color: #4a5568; font-size: 11px; border: none; background: transparent;")
        layout.addWidget(hint)
