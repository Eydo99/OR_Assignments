from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea, QHBoxLayout,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont


class TableauStepsPage(QWidget):
    """Page 3 – Shows step-by-step simplex tableau iterations."""

    def __init__(self):
        super().__init__()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        outer.addWidget(scroll)

        container = QWidget()
        container.setObjectName("TransparentWidget")
        scroll.setWidget(container)

        self._layout = QVBoxLayout(container)
        self._layout.setContentsMargins(28, 28, 28, 28)
        self._layout.setSpacing(20)

        header = QLabel("TABLEAU STEPS")
        header.setObjectName("SectionHeader")
        self._layout.addWidget(header)

        self._summary_label = QLabel()
        self._summary_label.setObjectName("SuccessMsg")
        self._summary_label.hide()
        self._layout.addWidget(self._summary_label)

        self._placeholder_card = self._build_placeholder()
        self._layout.addWidget(self._placeholder_card)

        self._steps_container = QWidget()
        self._steps_container.setObjectName("StepsContainer")
        self._steps_layout = QVBoxLayout(self._steps_container)
        self._steps_layout.setContentsMargins(0, 0, 0, 0)
        self._steps_layout.setSpacing(16)
        self._steps_container.hide()
        self._layout.addWidget(self._steps_container)

        self._layout.addStretch()

        self._num_vars = 0

    def _build_placeholder(self):
        card = QFrame()
        card.setObjectName("PlaceholderCard")
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(16)

        icon_label = QLabel("📋")
        icon_label.setObjectName("IconLabel")
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)

        msg = QLabel("No tableau steps yet")
        msg.setObjectName("PlaceholderMsg")
        msg.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(msg)

        sub = QLabel("Tableau iterations will appear here step-by-step after you solve a problem.")
        sub.setObjectName("CardSubHint")
        sub.setAlignment(Qt.AlignCenter)
        sub.setWordWrap(True)
        card_layout.addWidget(sub)

        return card

    # ── Public API ──
    def show_steps(self, steps: list, num_vars: int = 0):
        if not steps:
            self.reset()
            return

        self._num_vars = num_vars
        self._clear_steps()
        self._placeholder_card.hide()
        self._steps_container.show()

        pivot_count = sum(1 for s in steps if s.get("pivot_row") is not None)
        self._summary_label.setText(
            f"✔  Solved in {pivot_count} iteration{'s' if pivot_count != 1 else ''}"
        )
        self._summary_label.show()

        for idx, step in enumerate(steps):
            card = self._build_step_card(step, idx)
            self._steps_layout.addWidget(card)

    def _build_step_card(self, step, index):
        card = QFrame()
        card.setObjectName("StepCard")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)

        message = step.get("message", "")
        title = QLabel(f"Step {index + 1}  —  {message}")
        title.setObjectName("StepTitle")
        card_layout.addWidget(title)

        basis = step.get("basis", [])
        matrix = step.get("matrix", None)
        pivot_row = step.get("pivot_row", None)
        pivot_col = step.get("pivot_col", None)

        if matrix is not None:
            num_rows, num_cols = matrix.shape
            # num_cols includes the RHS column; data columns = num_cols - 1
            num_data_cols = num_cols - 1
            total_display_cols = num_data_cols + 1 + 1  # Basis + data cols + RHS

            table = QTableWidget(num_rows, num_data_cols + 2)  # Basis + data + RHS
            table.setObjectName("StepTableau")

            # Build per-step column headers based on actual matrix width
            headers = ["Basis"]
            for c in range(num_data_cols):
                headers.append(self._col_name_for_step(c, num_data_cols))
            headers.append("RHS")
            table.setHorizontalHeaderLabels(headers)

            table.verticalHeader().setVisible(False)

            # Row labels from basis
            row_labels = []
            for r in range(num_rows - 1):
                if r < len(basis):
                    row_labels.append(
                        self._col_name_for_step(int(basis[r]), num_data_cols)
                    )
                else:
                    row_labels.append(f"R{r}")
            row_labels.append("Z")

            is_z_row = lambda r: r == num_rows - 1
            basis_col_set = set(int(b) for b in basis) if basis else set()

            for r in range(num_rows):
                # Basis label cell (col 0)
                basis_item = QTableWidgetItem(row_labels[r])
                basis_item.setTextAlignment(Qt.AlignCenter)
                basis_item.setFlags(basis_item.flags() & ~Qt.ItemIsEditable)
                basis_item.setForeground(QColor("#4f9cf9"))
                font = basis_item.font()
                font.setBold(True)
                basis_item.setFont(font)
                if is_z_row(r):
                    basis_item.setBackground(QColor("#0a1628"))
                table.setItem(r, 0, basis_item)

                # Data columns (cols 1..num_data_cols) then RHS in last col
                for c in range(num_cols):  # c iterates over actual matrix columns
                    val = matrix[r][c]
                    is_rhs = (c == num_cols - 1)
                    display_col = c + 1  # shift right by 1 for the Basis column

                    text = self._format_val(val)
                    item = QTableWidgetItem(text)
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                    # Pivot highlight: only on data columns (not RHS), use c directly
                    if (
                        pivot_row is not None
                        and pivot_col is not None
                        and r == pivot_row
                        and c == pivot_col
                        and not is_rhs
                    ):
                        item.setBackground(QColor("#92400e"))
                        item.setForeground(QColor("#fbbf24"))
                        font = item.font()
                        font.setBold(True)
                        item.setFont(font)

                    elif is_z_row(r):
                        item.setBackground(QColor("#0a1628"))
                        item.setForeground(QColor("#94a3b8"))
                        font = item.font()
                        font.setBold(True)
                        item.setFont(font)

                    elif not is_rhs and self._is_basis_col(c, basis_col_set):
                        item.setBackground(QColor("#0d2948"))
                        item.setForeground(QColor("#60a5fa"))

                    table.setItem(r, display_col, item)

            table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            table.setMinimumWidth(500)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.horizontalHeader().setMinimumSectionSize(60)
            row_height = 36
            header_height = 34
            table.setFixedHeight(header_height + (num_rows * row_height) + 6)

            card_layout.addWidget(table)

        return card

    # ── Utility methods ──

    def _format_val(self, val):
        if abs(val - round(val)) < 1e-9:
            return str(int(round(val)))
        return f"{val:.4f}"

    def _col_name_for_step(self, col_index: int, num_data_cols: int) -> str:
        """
        Generate a readable column name based on the actual matrix width for
        this specific step. This correctly handles both Phase 1 (which includes
        artificial columns) and Phase 2 (which has them stripped out).

        Layout of data columns (0-indexed, excluding RHS):
          0 .. num_vars-1          → x1, x2, ...
          num_vars .. num_data_cols-1 → s1, s2, ... (slack / surplus / artificial)
        """
        if col_index < self._num_vars:
            return f"x{col_index + 1}"
        else:
            return f"s{col_index - self._num_vars + 1}"

    def _is_basis_col(self, col_index, basis_col_set):
        return col_index in basis_col_set

    def _clear_steps(self):
        while self._steps_layout.count():
            item = self._steps_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def reset(self):
        self._clear_steps()
        self._steps_container.hide()
        self._summary_label.hide()
        self._placeholder_card.show()