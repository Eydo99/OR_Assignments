import numpy as np
from utils.enums.obj_fn_type import ObjectiveFunctionType


class TableauMatrix:
    def __init__(self,lp_problem):
        self.lp_problem = lp_problem
        self.initial_basis =[]
        self.artificial_cols = []
        self.tableau_matrix = None



    def build_tableau_matrix(self):
        constraint_rows=[]
        rhs_col=[]
        original_vars_count = len(self.lp_problem.obj_fn_values)

        total_extra_cols = 0
        for constraint in self.lp_problem.constraints:
            c_type = constraint.constraint_type
            if c_type.value == "<=" or c_type.value == "=":
                total_extra_cols += 1
            elif c_type.value == ">=":
                total_extra_cols += 2

        extra_matrix = np.zeros((len(self.lp_problem.constraints), total_extra_cols))
        current_col_idx = 0

        for i, constraint in enumerate(self.lp_problem.constraints):
            constraint_rows.append(constraint.lhs)
            rhs_col.append(constraint.rhs)
            c_type = constraint.constraint_type

            if c_type.value == "<=":
                extra_matrix[i, current_col_idx] = 1
                self.initial_basis.append(original_vars_count + current_col_idx)
                current_col_idx += 1

            elif c_type.value == ">=":
                extra_matrix[i, current_col_idx] = -1
                current_col_idx += 1

                extra_matrix[i, current_col_idx] = 1
                self.initial_basis.append(original_vars_count + current_col_idx)
                self.artificial_cols.append(original_vars_count + current_col_idx)
                current_col_idx += 1

            elif c_type.value == "=":
                extra_matrix[i, current_col_idx] = 1
                self.initial_basis.append(original_vars_count + current_col_idx)
                self.artificial_cols.append(original_vars_count + current_col_idx)
                current_col_idx += 1

        self.tableau_matrix=np.array(constraint_rows)
        self.tableau_matrix = np.hstack([self.tableau_matrix, extra_matrix])

        z_row=self.lp_problem.obj_fn_values * -1 \
            if self.lp_problem.obj_fn_type==ObjectiveFunctionType.max \
            else self.lp_problem.obj_fn_values

        z_row = np.append(z_row, np.zeros(total_extra_cols))
        self.tableau_matrix = np.vstack([self.tableau_matrix, z_row])

        rhs_col.append(0.0)
        self.tableau_matrix=np.hstack([self.tableau_matrix,np.array(rhs_col).reshape(-1,1)])











