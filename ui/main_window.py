import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QSizePolicy
from ui.content_area import ContentArea
from ui.sidebar import Sidebar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LP Problems Solver")
        self.setMinimumSize(1100, 750)

        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(central_widget)

        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # ── Sidebar ──
        self.sidebar = Sidebar()
        self.main_layout.addWidget(self.sidebar)

        # ── Content area ──
        self.content = ContentArea()
        self.main_layout.addWidget(self.content)

        # ── Wire sidebar → content page switching ──
        self.sidebar.section_changed.connect(self.content.set_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())