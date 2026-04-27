import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QHBoxLayout, QSizePolicy)
from PySide6.QtCore import Qt


from ui.content_area import ContentArea
from ui.sidebar import Sidebar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LP Problems Solver")
        self.setMinimumSize(1100, 750)
        self.setStyleSheet("background-color: #1a1a2e;")

        central_widget = QWidget()
        central_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        self.setCentralWidget(central_widget)

        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.setAlignment(self.sidebar, Qt.AlignLeft)

        self.content = ContentArea()
        self.main_layout.addWidget(self.content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())