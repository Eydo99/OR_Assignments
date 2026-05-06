from PySide6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView,
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QStackedWidget, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QFontMetrics, QTransform, QPainter

from ui import theme
from ui.theme import cell_color, cell_text_color


class RotatedLabel(QLabel):
    """A QLabel that renders its text rotated 90° counter-clockwise."""

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setMinimumWidth(20)
        self.setMaximumWidth(20)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QColor(theme.MUTED2))

        font = QFont(theme.FONT_UI.split(",")[0].strip(), theme.FONT_SM)
        font.setBold(True)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 2)
        painter.setFont(font)

        # Rotate 90° CCW: translate origin to bottom-left, then rotate
        painter.translate(self.width(), self.height())
        painter.rotate(-90)
        painter.drawText(
            0, 0, self.height(), self.width(),
            Qt.AlignmentFlag.AlignCenter,
            self.text(),
        )
        painter.end()


class PayoffMatrixWidget(QWidget):
    """
    A complete payoff-matrix panel.
    Includes its own title label + axis labels:
      · Y-axis (rotated):  "HIDER'S ACTIONS"   (rows)
      · X-axis (top):      "SEEKER'S ACTIONS"   (columns)
    The QTableWidget stretches to fill ALL available space with zero scrollbars.
    Works cleanly up to 20×20.
    Accepts both int and float matrix values.
    """

    def __init__(self, title: str = "PAYOFF MATRIX (HIDER POV)", parent=None):
        super().__init__(parent)
        self.setObjectName("PayoffMatrixPanel")

        # ── Outer layout ──────────────────────────
        outer = QVBoxLayout(self)
        outer.setContentsMargins(12, 10, 12, 10)
        outer.setSpacing(6)

        # Title
        self._title_lbl = QLabel(title)
        self._title_lbl.setProperty("class", "section-label")
        outer.addWidget(self._title_lbl)

        # Stack: placeholder vs matrix view
        self._stack = QStackedWidget()
        outer.addWidget(self._stack, stretch=1)

        # ── Placeholder ───────────────────────────
        placeholder = QLabel("No matrix loaded yet")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet(
            f"color: {theme.MUTED2}; font-size: {theme.FONT_SM}px;"
        )
        self._stack.addWidget(placeholder)   # index 0

        # ── Matrix view: axis labels + table ──────
        matrix_view = QWidget()
        matrix_view.setStyleSheet("background: transparent;")
        mv_layout = QVBoxLayout(matrix_view)
        mv_layout.setContentsMargins(0, 0, 0, 0)
        mv_layout.setSpacing(2)

        # X-axis label (above the table area, aligned with the table not the row header)
        self._x_axis_lbl = QLabel("SEEKER'S ACTIONS  →")
        self._x_axis_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._x_axis_lbl.setStyleSheet(
            f"color: {theme.RED}; font-size: {theme.FONT_SM}px;"
            f" font-weight: 800; letter-spacing: 2px;"
            f" background: transparent;"
        )
        mv_layout.addWidget(self._x_axis_lbl)

        # Row containing [rotated Y-label | table]
        body_row = QHBoxLayout()
        body_row.setContentsMargins(0, 0, 0, 0)
        body_row.setSpacing(0)  # Reduced from 4 to 0 for tighter spacing

        # Y-axis label (rotated, left of table)
        self._y_axis_lbl = RotatedLabel("HIDER'S ACTIONS  →")
        self._y_axis_lbl.setStyleSheet("background: transparent;")
        self._y_axis_lbl.setToolTip("Rows = Hider's chosen hiding location")
        body_row.addWidget(self._y_axis_lbl)

        # The actual table
        self._table = QTableWidget()
        self._table.setObjectName("PayoffMatrix")
        self._configure_table()
        body_row.addWidget(self._table, stretch=1)

        mv_layout.addLayout(body_row, stretch=1)
        self._stack.addWidget(matrix_view)   # index 1

        # Panel styling (dark card)
        self.setStyleSheet(f"""
            #PayoffMatrixPanel {{
                background-color: {theme.SURFACE};
                border: 1px solid {theme.BORDER};
                border-radius: 16px;
            }}
        """)

    # ── Public API ────────────────────────────────

    def load_matrix(self, matrix: list, place_names: list[str]):
        """
        Populate the table with *matrix* values and colour-coded cells.
        Accepts both int and float values.
        place_names: row/column header labels (e.g. ["Forest", "City", ...])
        """
        if not matrix or not place_names:
            self._stack.setCurrentIndex(0)
            return

        n_rows = len(matrix)
        n_cols = len(matrix[0]) if matrix else 0

        self._table.setRowCount(n_rows)
        self._table.setColumnCount(n_cols)

        col_labels = self._abbreviate(place_names, n_cols)
        row_labels = self._abbreviate(place_names, n_rows)

        self._table.setHorizontalHeaderLabels(col_labels)
        self._table.setVerticalHeaderLabels(row_labels)

        cell_font_size = self._adaptive_font_size(max(n_rows, n_cols))
        hdr_font_size = max(cell_font_size - 1, 7)

        mono_family = theme.FONT_MONO.split(",")[0].strip()
        cell_font = QFont(mono_family, cell_font_size)
        cell_font.setBold(True)
        hdr_font = QFont(mono_family, hdr_font_size)
        hdr_font.setBold(True)

        self._table.horizontalHeader().setFont(hdr_font)
        self._table.verticalHeader().setFont(hdr_font)

        for r in range(n_rows):
            for c in range(n_cols):
                val = matrix[r][c]
                # Support both int and float values
                try:
                    if val == 0:
                        text = "0"
                    elif isinstance(val, float):
                        if val == int(val):
                            text = f"{int(val):+d}"   # -3.0 → "-3"
                        else:
                            text = f"{val:+.2f}"       # 1.5  → "+1.50"
                    else:
                        text = f"{val:+d}"             # plain int
                except (ValueError, TypeError):
                    text = str(val)

                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFont(cell_font)
                item.setBackground(QColor(cell_color(val)))
                item.setForeground(QColor(cell_text_color(val)))
                self._table.setItem(r, c, item)

        fm = QFontMetrics(hdr_font)
        max_label_px = max(
            (fm.horizontalAdvance(lbl) for lbl in row_labels),
            default=40,
        )
        self._table.verticalHeader().setFixedWidth(max_label_px + 16)

        self._stack.setCurrentIndex(1)

    def set_title(self, text: str):
        self._title_lbl.setText(text)

    # ── Private helpers ───────────────────────────

    def _configure_table(self):
        t = self._table
        t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        t.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        t.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        t.verticalHeader().setVisible(True)
        t.horizontalHeader().setVisible(True)
        t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        t.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        t.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        t.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        t.setFrameShape(QTableWidget.Shape.NoFrame)
        t.setShowGrid(False)

    @staticmethod
    def _adaptive_font_size(n: int) -> int:
        if n <= 5:    return 16
        elif n <= 7:  return 14
        elif n <= 10: return 13
        elif n <= 14: return 11
        elif n <= 17: return 10
        else:         return 9

    @staticmethod
    def _abbreviate(names: list[str], count: int) -> list[str]:
        if count <= 10:   return names[:count]
        elif count <= 15: return [n[:4] for n in names[:count]]
        else:             return [n[:2] for n in names[:count]]