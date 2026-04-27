import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # Set a clean default font
    font = QFont("Segoe UI", 10)
    font.setHintingPreference(QFont.PreferFullHinting)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
