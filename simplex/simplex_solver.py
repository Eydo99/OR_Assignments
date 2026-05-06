import numpy as np
from utils.enums.obj_fn_type import ObjectiveFunctionType


class SimplexSolver:
    def __init__(self, tableau_matrix, lp_problem):
        self.matrix = tableau_matrix.tableau_matrix.copy()
        self.basis = tableau_matrix.initial_basis.copy()
        self.artificial_cols = tableau_matrix.artificial_cols.copy()
        self.free_var_minus_cols = getattr(tableau_matrix, "free_var_minus_cols", {})
        self.result = None
        self.lp_problem = lp_problem
        self.iteration_count = 0
        self.phase_1_iterations = 0
        self.phase_2_iterations = 0
        self.used_two_phase = False

    def solve(self):
        if len(self.artificial_cols) > 0:
            self.used_two_phase = True
            status = self._phase_1()
            if status == "infeasible":
                self.result = "infeasible"
                return None
            return self.phase2_tableau_maker()
        else:
            self.used_two_phase = False
            self.result = self._simple_solve()
            if self.result == "unbounded":
                return None
            return self._write_result()

    def _phase_1(self):
        original_z_row = self.matrix[-1].copy()

        w_row = np.zeros(len(self.matrix[0]))
        for col in self.artificial_cols:
            w_row[col] = 1

        self.matrix[-1] = w_row
        for i in range(len(self.matrix) - 1):
            if self.basis[i] in self.artificial_cols:
                w_row = w_row - self.matrix[i]

        self.matrix[-1] = w_row

        phase_1_start = self.iteration_count
        self._simple_solve()
        self.phase_1_iterations = self.iteration_count - phase_1_start

        optimal_w_value = self.matrix[-1][-1]
        if optimal_w_value < -1e-7:
            return "infeasible"

        self._basis_fault_checker()
        self.matrix[-1] = original_z_row
        return "success"

    def _basis_fault_checker(self):
        for i, basic_var in enumerate(self.basis):

            if basic_var not in self.artificial_cols:
                continue

            if abs(self.matrix[i][-1]) > 1e-9:
                continue
            replacement_col = None
            for col in range(len(self.matrix[0]) - 1):
                if col not in self.artificial_cols:
                    if abs(self.matrix[i][col]) > 1e-9:
                        replacement_col = col
                        break

            self._basis_fault_corrector(i, basic_var, replacement_col)

    def _basis_fault_corrector(self, row, artificial_col, replacement_col):
        if replacement_col is not None:
            self._pivot(row, replacement_col)
    def phase2_tableau_maker(self):
        num_cols = self.matrix.shape[1]
        cols_to_keep = [c for c in range(num_cols) if c not in self.artificial_cols]

        old_to_new = {}
        new_idx = 0
        for old_idx in range(num_cols):
            if old_idx in cols_to_keep:
                old_to_new[old_idx] = new_idx
                new_idx += 1

        self.matrix = self.matrix[:, cols_to_keep]
        self.basis = [old_to_new[b] for b in self.basis if b in old_to_new]

        num_constraint_rows = len(self.matrix) - 1
        if len(self.basis) != num_constraint_rows:
            self.result = "infeasible"
            return None

        self.free_var_minus_cols = {
            var: old_to_new[col]
            for var, col in self.free_var_minus_cols.items()
            if col in old_to_new
        }

        self.artificial_cols = type(self.artificial_cols)()
        z_row = np.zeros(self.matrix.shape[1])

        for i, coeff in enumerate(self.lp_problem.obj_fn_values):
            if i < self.matrix.shape[1] - 1:
                if self.lp_problem.obj_fn_type == ObjectiveFunctionType.max:
                    z_row[i] = -coeff
                else:
                    z_row[i] = coeff

        for var_idx, minus_col in self.free_var_minus_cols.items():
            z_row[minus_col] = -z_row[var_idx]

        self.matrix[-1] = z_row

        return self.the_last_refiner()

    def the_last_refiner(self):
        num_rows = len(self.matrix) - 1
        for i in range(num_rows):
            basic_var_col = self.basis[i]
            z_coeff = self.matrix[-1][basic_var_col]

            if abs(z_coeff) < 1e-9:
                continue

            self.matrix[-1] -= z_coeff * self.matrix[i]
        
        phase_2_start = self.iteration_count
        self.result = self._simple_solve()
        self.phase_2_iterations = self.iteration_count - phase_2_start

        if self.result == "unbounded":
            return None

        return self._write_result()

    def _simple_solve(self):
        while True:
            z_row = self.matrix[-1]
            min_index = np.argmin(z_row[:-1])

            if z_row[min_index] >= 0:
                return "optimal"

            min_pivot_index = -1
            min_ratio = float("inf")
            for i in range(len(self.matrix) - 1):
                if self.matrix[i][min_index] <= 0:
                    continue
                ratio = self.matrix[i][-1] / self.matrix[i][min_index]
                if ratio < 0:
                    continue
                if ratio < min_ratio:
                    min_ratio = ratio
                    min_pivot_index = i

            if min_pivot_index == -1:
                return "unbounded"

            self._pivot(min_pivot_index, min_index)
            self.iteration_count += 1

    def _write_result(self):
        solution_dict = {}
        num_original_vars = len(self.lp_problem.obj_fn_values)
        variables_final_value = []

        for i in range(num_original_vars):
            if i in self.basis:
                row_of_var = self.basis.index(i)
                val = round(float(self.matrix[row_of_var][-1]),4)
            else:
                val = 0.0
            variables_final_value.append(val)

        if self.free_var_minus_cols:
            for var_idx, minus_col in self.free_var_minus_cols.items():
                if minus_col in self.basis:
                    minus_row = self.basis.index(minus_col)
                    minus_val = float(self.matrix[minus_row][-1])
                else:
                    minus_val = 0.0

                variables_final_value[var_idx] -= minus_val

        solution_dict["variables"] = variables_final_value

        optimal_value = float(self.matrix[-1][-1])

        if self.lp_problem.obj_fn_type == ObjectiveFunctionType.min and optimal_value != 0:
            optimal_value = -optimal_value

        solution_dict["optimal_value"] = optimal_value
        solution_dict["iteration_count"] = self.iteration_count
        solution_dict["phase_1_iterations"] = self.phase_1_iterations
        solution_dict["phase_2_iterations"] = self.phase_2_iterations
        solution_dict["used_two_phase"] = self.used_two_phase
        solution_dict["status"] = "Optimal"
        return solution_dict

    def _pivot(self, pivot_row, pivot_column):
        self.matrix[pivot_row] = self.matrix[pivot_row] / self.matrix[pivot_row][pivot_column]
        for i in range(len(self.matrix)):
            if i == pivot_row:
                continue
            factor = -self.matrix[i][pivot_column]
            self.matrix[i] = factor * self.matrix[pivot_row] + self.matrix[i]
        self.basis[pivot_row] = pivot_column