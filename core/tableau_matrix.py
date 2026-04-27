import numpy as np
from utils.enums.obj_fn_type import ObjectiveFunctionType


class TableauMatrix:
    def __init__(self,lp_problem):
        self.lp_problem = lp_problem
        self.initial_basis =[]
        self.tableau_matrix = None



    def build_tableau_matrix(self):
        constraint_rows=[]
        rhs_col=[]
        basis_index=len(self.lp_problem.obj_fn_values)

        for constraint in self.lp_problem.constraints:
            constraint_rows.append(constraint.lhs)
            rhs_col.append(constraint.rhs)
            self.initial_basis.append(basis_index)
            basis_index+=1

        self.tableau_matrix=np.array(constraint_rows)

        identity=np.eye(len(self.lp_problem.constraints))
        self.tableau_matrix=np.hstack([self.tableau_matrix,identity])

        z_row=self.lp_problem.obj_fn_values * -1 \
            if self.lp_problem.obj_fn_type==ObjectiveFunctionType.max \
            else self.lp_problem.obj_fn_values

        z_row = np.append(z_row, np.zeros(len(self.lp_problem.constraints)))
        self.tableau_matrix=np.vstack([self.tableau_matrix,z_row])

        rhs_col.append(0.0)
        self.tableau_matrix=np.hstack([self.tableau_matrix,np.array(rhs_col).reshape(-1,1)])











