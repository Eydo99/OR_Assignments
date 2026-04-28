from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidgetItem, QLabel, QTableWidget, QHeaderView, QVBoxLayout, QFrame


class TableauPreviewCard(QFrame):
    """Preview card showing the initial simplex tableau with pivot highlighting."""

    def __init__(self):
        super().__init__()
        self.setObjectName("CardFrame")

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("Tableau preview")
        title.setObjectName("CardTitle")
        layout.addWidget(title)

        self.table = QTableWidget(3, 7)
        self._setup_table()

        # Initial default structure
        self.rebuild_structure(3, 2)

        self.table.setFixedHeight(160)
        layout.addWidget(self.table)

        hint = QLabel("Pivot cell highlighted in green")
        hint.setObjectName("CardHint")
        layout.addWidget(hint)

    def _setup_table(self):
        pass

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setMinimumHeight(36)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setShowGrid(True)

    def _fill_data(self, data, pivot_cell=None):
        """Fill the table with data and optionally highlight the pivot cell."""
        self.table.setRowCount(len(data))
        if data:
            self.table.setColumnCount(len(data[0]))

        for row, row_data in enumerate(data):
            for col, val in enumerate(row_data):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)

                # Last row (Z row) in orange
                if row == len(data) - 1:
                    item.setForeground(QColor("#f6ad55"))

                # Pivot cell in green
                if pivot_cell and (row, col) == pivot_cell:
                    item.setBackground(QColor("#2d3a1e"))
                    item.setForeground(QColor("#68d391"))

                self.table.setItem(row, col, item)

    # ── Public API (to be wired after solver logic) ──
    def update_data(self, headers, rows, pivot_rc=None):
        """Update the table with new data.
        Args:
            headers: list of column header strings
            rows: list of lists of cell value strings
            pivot_rc: (row, col) tuple of the pivot cell, or None
        """
        self.table.setHorizontalHeaderLabels(headers)
        self._fill_data(rows, pivot_rc)

    def rebuild_structure(self, num_vars, num_constraints):
        """Rebuild a blank tableau structure matching the variables and constraints."""
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        
        headers = ["Basis"]
        for i in range(num_vars): headers.append(f"x{i+1}".translate(SUB))
        for i in range(num_constraints): headers.append(f"s{i+1}".translate(SUB))
        headers.append("RHS")

        # Rows
        rows = []
        num_cols = len(headers)
        for i in range(num_constraints):
            row = [f"s{i+1}".translate(SUB)] + ["0"] * (num_cols - 1)
            rows.append(row)
            
        # Z row
        rows.append(["Z"] + ["0"] * (num_cols - 1))

        self.update_data(headers, rows)

    def update_from_data(self, num_vars, num_constraints, coeff_data, obj_type):
        """Live-update the tableau values based on coefficients typed by the user."""
        if not coeff_data or "obj_fn_values" not in coeff_data:
            return self.rebuild_structure(num_vars, num_constraints)

        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        
        headers = ["Basis"]
        for i in range(num_vars): headers.append(f"x{i+1}".translate(SUB))
        for i in range(num_constraints): headers.append(f"s{i+1}".translate(SUB))
        headers.append("RHS")

        rows = []
        # Constraint rows
        constraints = coeff_data["constraints"]
        for i in range(num_constraints):
            row = [f"s{i+1}".translate(SUB)]
            if i < len(constraints):
                c = constraints[i]
                # x variables
                for x_val in c["LHS"]:
                    row.append(str(float(x_val)))
                # slack variables identity matrix
                for j in range(num_constraints):
                    row.append("1.0" if i == j else "0.0")
                # rhs
                row.append(str(float(c["RHS"])))
            else:
                num_cols = len(headers)
                row.extend(["0.0"] * (num_cols - 1))
            rows.append(row)

        # Z row
        z_row = ["Z"]
        obj_vals = coeff_data["obj_fn_values"]
        is_max = "max" in obj_type.lower()
        for v in obj_vals:
            val = float(v)
            z_row.append(str(-val) if is_max else str(val))
        
        # Slack vars in Z row are 0
        for i in range(num_constraints):
            z_row.append("0.0")
        
        # Z RHS
        z_row.append("0.0")
        
        rows.append(z_row)

        self.update_data(headers, rows)
