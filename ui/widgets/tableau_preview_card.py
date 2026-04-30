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
        if not coeff_data or "obj_fn_values" not in coeff_data:
            return self.rebuild_structure(num_vars, num_constraints)

        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        constraints = coeff_data["constraints"]

        # Count extra columns needed
        slack_count = 0
        artificial_count = 0
        extra_info = []  # per constraint: (has_slack, has_surplus, has_artificial)
        for i in range(num_constraints):
            c_type = constraints[i]["constraint_type"] if i < len(constraints) else "<="
            if c_type == "<=":
                extra_info.append(("slack", None))
                slack_count += 1
            elif c_type == ">=":
                extra_info.append(("surplus", "artificial"))
                slack_count += 1  # surplus
                artificial_count += 1
            elif c_type == "=":
                extra_info.append((None, "artificial"))
                artificial_count += 1

        # Build headers
        headers = ["Basis"]
        for i in range(num_vars):
            headers.append(f"x{i + 1}".translate(SUB))
        s_idx = 1
        a_idx = 1
        col_meta = []  # track column types for identity filling
        for info in extra_info:
            if info[0] == "slack":
                headers.append(f"s{s_idx}".translate(SUB))
                col_meta.append(("slack", s_idx - 1))
                s_idx += 1
            elif info[0] == "surplus":
                headers.append(f"s{s_idx}".translate(SUB))
                col_meta.append(("surplus", s_idx - 1))
                s_idx += 1
                headers.append(f"a{a_idx}".translate(SUB))
                col_meta.append(("artificial", a_idx - 1))
                a_idx += 1
            elif info[0] is None:
                headers.append(f"a{a_idx}".translate(SUB))
                col_meta.append(("artificial", a_idx - 1))
                a_idx += 1
        headers.append("RHS")

        num_extra_cols = len(col_meta)

        # Build basis labels
        basis_labels = []
        slack_counter = 0
        artificial_counter = 0
        for i, info in enumerate(extra_info):
            if info[0] == "slack":
                basis_labels.append(f"s{slack_counter + 1}")
                slack_counter += 1
            else:
                basis_labels.append(f"a{artificial_counter + 1}")
                artificial_counter += 1

        # Build rows
        rows = []
        extra_col_start = num_vars + 1  # offset in headers (after Basis col)

        for i in range(num_constraints):
            c_type = constraints[i]["constraint_type"] if i < len(constraints) else "<="
            if c_type == "<=":
                row_label = f"s{sum(1 for x in extra_info[:i + 1] if x[0] == 'slack')}".translate(SUB)
            elif c_type == ">=":
                a_num = sum(1 for x in extra_info[:i + 1] if x[1] == 'artificial')
                row_label = f"a{a_num}".translate(SUB)
            else:
                a_num = sum(1 for x in extra_info[:i + 1] if x[1] == 'artificial')
                row_label = f"a{a_num}".translate(SUB)

            row = [row_label]

            # x coefficients
            lhs = constraints[i]["LHS"] if i < len(constraints) else [0] * num_vars
            for v in lhs:
                row.append(str(float(v)))

            # extra columns
            col_offset = 0
            for info in extra_info[:i]:
                if info[0] == "slack":
                    col_offset += 1
                elif info[0] == "surplus":
                    col_offset += 2
                elif info[0] is None:
                    col_offset += 1

            for j, meta in enumerate(col_meta):
                kind = meta[0]
                if c_type == "<=":
                    row.append("1.0" if (kind == "slack" and j == col_offset) else "0.0")
                elif c_type == ">=":
                    if kind == "surplus" and j == col_offset:
                        row.append("-1.0")
                    elif kind == "artificial" and j == col_offset + 1:
                        row.append("1.0")
                    else:
                        row.append("0.0")
                elif c_type == "=":
                    row.append("1.0" if (kind == "artificial" and j == col_offset) else "0.0")

            # RHS
            rhs = constraints[i]["RHS"] if i < len(constraints) else 0
            row.append(str(float(rhs)))
            rows.append(row)

        # Z row
        z_row = ["Z"]
        obj_vals = coeff_data["obj_fn_values"]
        is_max = "max" in obj_type.lower()
        for v in obj_vals:
            z_row.append(str(-float(v)) if is_max else str(float(v)))
        for _ in col_meta:
            z_row.append("0.0")
        z_row.append("0.0")
        rows.append(z_row)

        self.update_data(headers, rows)