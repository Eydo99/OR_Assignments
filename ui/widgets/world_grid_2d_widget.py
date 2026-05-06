
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QHBoxLayout
)
from PySide6.QtCore import Qt, Signal

from ui import theme
from ui.theme import difficulty_name, difficulty_color, difficulty_label


# Emoji lookup per place-type code
_TYPE_ICONS: dict[str, str] = {
    "F": "🌲", "C": "🪨", "B": "🏖", "M": "⛰",
    "V": "🌄", "R": "🌊", "P": "🌿", "H": "🏠",
    "S": "🏪", "D": "⚠",  "N": "⬛", "E": "✅", "X": "🔴",
}


class WorldGrid2DWidget(QWidget):
    """
    A self-contained N×N interactive world grid.

    Each cell shows:
      · An emoji icon for the place type  (type still communicated visually)
      · Its (row, col) coordinate
      · A SINGLE colour-coded bottom border by difficulty (Easy/Neutral/Hard)
        — matches the difficulty legend shown above the grid.

    The tooltip includes: place name, type, coordinates, and difficulty.

    Signals:
        cell_clicked(int)  — emits the flat index of the clicked cell
    """

    cell_clicked = Signal(int)

    def __init__(self, title: str = "2D WORLD GRID", parent=None):
        super().__init__(parent)
        self.setObjectName("WorldGrid2DPanel")

        self._buttons:    list[QPushButton] = []
        self._base_styles: list[str]        = []
        self._grid_size:   int              = 0

        outer = QVBoxLayout(self)
        outer.setContentsMargins(12, 10, 12, 10)
        outer.setSpacing(6)

        self._title = QLabel(title)
        self._title.setProperty("class", "section-label")
        outer.addWidget(self._title)

        # Difficulty legend — the ONLY colour legend shown
        legend = self._build_legend()
        outer.addWidget(legend)

        # Scrollable grid area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._grid_container = QWidget()
        self._grid_container.setStyleSheet("background: transparent;")
        self._grid_layout = QGridLayout(self._grid_container)
        self._grid_layout.setSpacing(4)
        self._grid_layout.setContentsMargins(4, 4, 4, 4)
        scroll.setWidget(self._grid_container)

        outer.addWidget(scroll, stretch=1)

        # Panel styling
        self.setStyleSheet(f"""
            #WorldGrid2DPanel {{
                background-color: {theme.SURFACE};
                border: 1px solid {theme.BORDER};
                border-radius: 16px;
            }}
        """)


    def _build_legend(self) -> QWidget:
        """Difficulty legend row — Easy / Neutral / Hard only."""
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        for diff, color in theme.DIFFICULTY_COLORS.items():
            badge = QLabel(f"▬ {diff}")
            badge.setStyleSheet(
                f"color: {color}; font-size: 10px; font-weight: 700;"
                f" background: transparent; letter-spacing: 1px;"
            )
            lay.addWidget(badge)
        lay.addStretch()
        return w

    #  PUBLIC API

    def load_world(
        self,
        grid_size:   int,
        place_types: list[str],
        place_names: list[str],
    ):
        """
        Build a K×K grid of clickable place cells.

        grid_size   : K  (grid is K×K, total places = K²)
        place_types : flat list of single-char codes, length K²
        place_names : flat list of human names, length K²
        """
        self.clear()
        self._grid_size = grid_size

        cell_px = max(44, min(80, 400 // grid_size))
        font_px = max(8, min(11, cell_px // 6))

        for idx, (ptype, pname) in enumerate(zip(place_types, place_names)):
            row, col = divmod(idx, grid_size)

            # The place_color top-border tint is removed to eliminate the
            # dual-colour confusion.  Type is still visible via the emoji.
            diff_color = difficulty_color(ptype)
            diff_name  = difficulty_name(ptype)
            icon       = _TYPE_ICONS.get(ptype, "❓")

            btn = QPushButton(f"{icon}\n({row},{col})")
            base_style = f"""
                QPushButton {{
                    background-color: {theme.SURFACE2};
                    color: {theme.TEXT};
                    border: 1px solid {theme.BORDER};
                    border-bottom: 4px solid {diff_color};
                    border-radius: 8px;
                    font-family: "{theme.FONT_MONO}";
                    font-size: {font_px}px;
                    font-weight: bold;
                    padding: 2px;
                    min-width:  {cell_px}px; max-width:  {cell_px}px;
                    min-height: {cell_px}px; max-height: {cell_px}px;
                }}
                QPushButton:hover {{
                    background-color: {theme.HIGHLIGHT};
                    border: 1px solid {diff_color};
                    border-bottom: 4px solid {diff_color};
                }}
                QPushButton:pressed {{
                    background-color: {diff_color};
                }}
            """
            btn.setStyleSheet(base_style)
            btn.setToolTip(
                f"<b>{pname}</b><br/>"
                f"Type: {ptype} · Icon: {icon}<br/>"
                f"Cell ({row}, {col})  ·  Index: {idx}<br/>"
                f"Difficulty: <span style='color:{diff_color};'>{diff_name}</span>"
            )
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, i=idx: self._on_cell_clicked(i))

            self._grid_layout.addWidget(btn, row, col)
            self._buttons.append(btn)
            self._base_styles.append(base_style)

        # Row index labels on the right edge
        for r in range(grid_size):
            lbl = QLabel(str(r))
            lbl.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            lbl.setFixedWidth(16)
            lbl.setStyleSheet(
                f"color: {theme.MUTED2}; font-size: 8px; background: transparent;"
            )
            self._grid_layout.addWidget(lbl, r, grid_size)

        # Column index labels on the bottom
        for c in range(grid_size):
            lbl = QLabel(str(c))
            lbl.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            lbl.setFixedHeight(14)
            lbl.setStyleSheet(
                f"color: {theme.MUTED2}; font-size: 8px; background: transparent;"
            )
            self._grid_layout.addWidget(lbl, grid_size, c)

    def highlight_cell(self, index: int, color: str | None = None):
        """Highlight a cell with a colour, or restore original style."""
        if 0 <= index < len(self._buttons):
            btn = self._buttons[index]
            if color:
                btn.setStyleSheet(
                    self._base_styles[index]
                    + f"\nQPushButton {{ background-color: {color}; }}"
                )
            else:
                btn.setStyleSheet(self._base_styles[index])

    def clear(self):
        """Remove all cells from the grid."""
        self._buttons.clear()
        self._base_styles.clear()
        while self._grid_layout.count():
            item = self._grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def set_title(self, text: str):
        self._title.setText(text)

    @property
    def grid_size(self) -> int:
        return self._grid_size

    @property
    def buttons(self) -> list[QPushButton]:
        return self._buttons

    @property
    def base_styles(self) -> list[str]:
        return self._base_styles


    def _on_cell_clicked(self, index: int):
        self.cell_clicked.emit(index)