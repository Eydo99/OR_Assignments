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

        # ── Scroll wrapper ──
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

        # ── Section header ──
        header = QLabel("TABLEAU STEPS")
        header.setObjectName("SectionHeader")
        self._layout.addWidget(header)

        # ── Summary label (hidden by default) ──
        self._summary_label = QLabel()
        self._summary_label.setObjectName("SuccessMsg")
        self._summary_label.hide()
        self._layout.addWidget(self._summary_label)

        # ── Placeholder card ──
        self._placeholder_card = self._build_placeholder()
        self._layout.addWidget(self._placeholder_card)

        # ── Step cards container ──
        self._steps_container = QWidget()
        self._steps_container.setObjectName("StepsContainer")
        self._steps_layout = QVBoxLayout(self._steps_container)
        self._steps_layout.setContentsMargins(0, 0, 0, 0)
        self._steps_layout.setSpacing(16)
        self._steps_container.hide()
        self._layout.addWidget(self._steps_container)

        self._layout.addStretch()

        # Store num_vars for column headers
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
        """Display a list of step dicts from the solver.
        Each step dict has: message, matrix (numpy), basis (list),
        pivot_row (int|None), pivot_col (int|None).
        """
        if not steps:
            self.reset()
            return

        self._num_vars = num_vars
        self._clear_steps()
        self._placeholder_card.hide()
        self._steps_container.show()

        # Count pivot iterations for summary
        pivot_count = sum(1 for s in steps if s.get("pivot_row") is not None)
        self._summary_label.setText(f"✔  Solved in {pivot_count} iteration{'s' if pivot_count != 1 else ''}")
        self._summary_label.show()

        for idx, step in enumerate(steps):
            card = self._build_step_card(step, idx)
            self._steps_layout.addWidget(card)

    def _build_step_card(self, step, index):
        card = QFrame()
        card.setObjectName("StepCard")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)

        # ── Title with message (1-indexed) ──
        message = step.get("message", "")
        title = QLabel(f"Step {index + 1}  —  {message}")
        title.setObjectName("StepTitle")
        card_layout.addWidget(title)

        # ── Tableau table with Basis as first column ──
        basis = step.get("basis", [])
        matrix = step.get("matrix", None)
        pivot_row = step.get("pivot_row", None)
        pivot_col = step.get("pivot_col", None)

        if matrix is not None:
            num_rows, num_cols = matrix.shape
            total_cols = num_cols + 1  # +1 for the Basis column

            table = QTableWidget(num_rows, total_cols)
            table.setObjectName("StepTableau")

            # Column headers: Basis | x1 | x2 | ... | s1 | s2 | ... | RHS
            headers = ["Basis"]
            for c in range(num_cols - 1):
                headers.append(self._col_name(c))
            headers.append("RHS")
            table.setHorizontalHeaderLabels(headers)

            # Hide the vertical header (row numbers) — Basis column replaces it
            table.verticalHeader().setVisible(False)

            # Build row labels for the Basis column
            row_labels = []
            for r in range(num_rows - 1):
                if r < len(basis):
                    row_labels.append(self._col_name(int(basis[r])))
                else:
                    row_labels.append(f"R{r}")
            row_labels.append("Z")

            # Fill data with styling
            is_z_row = lambda r: r == num_rows - 1
            basis_col_set = set(int(b) for b in basis) if basis else set()

            for r in range(num_rows):
                # Column 0: Basis label
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

                # Columns 1..total_cols-1: actual matrix data
                for c in range(num_cols):
                    val = matrix[r][c]
                    text = self._format_val(val)
                    item = QTableWidgetItem(text)
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                    # Pivot cell: amber highlight + bold (offset by +1 for Basis col)
                    if pivot_row is not None and pivot_col is not None and r == pivot_row and c == pivot_col:
                        item.setBackground(QColor("#92400e"))
                        item.setForeground(QColor("#fbbf24"))
                        font = item.font()
                        font.setBold(True)
                        item.setFont(font)

                    # Z row: dark bg + muted text + bold
                    elif is_z_row(r):
                        item.setBackground(QColor("#0a1628"))
                        item.setForeground(QColor("#94a3b8"))
                        font = item.font()
                        font.setBold(True)
                        item.setFont(font)

                    # Basis column cells: blue tint
                    elif self._is_basis_col(c, basis_col_set):
                        item.setBackground(QColor("#0d2948"))
                        item.setForeground(QColor("#60a5fa"))

                    table.setItem(r, c + 1, item)  # offset by 1

            # Sizing — maximize table
            table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            table.setMinimumWidth(500)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.horizontalHeader().setMinimumSectionSize(60)
            row_height = 36
            header_height = 34
            total_height = header_height + (num_rows * row_height) + 6
            table.setFixedHeight(total_height)

            card_layout.addWidget(table)

        return card

    # ── Utility methods ──

    def _format_val(self, val):
        """Format a number: integers shown cleanly, floats to 4 dp."""
        if abs(val - round(val)) < 1e-9:
            return str(int(round(val)))
        return f"{val:.4f}"

    def _col_name(self, col_index):
        """Generate a readable column name."""
        if col_index < self._num_vars:
            return f"x{col_index + 1}"
        else:
            return f"s{col_index - self._num_vars + 1}"

    def _is_basis_col(self, col_index, basis_col_set):
        """Check if a column index belongs to a current basis variable."""
        return col_index in basis_col_set

    def _clear_steps(self):
        while self._steps_layout.count():
            item = self._steps_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def reset(self):
        """Hide steps, show placeholder again."""
        self._clear_steps()
        self._steps_container.hide()
        self._summary_label.hide()
        self._placeholder_card.show()
