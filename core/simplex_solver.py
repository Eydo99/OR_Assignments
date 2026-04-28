import numpy as np
from utils.enums.obj_fn_type import ObjectiveFunctionType


class SimplexSolver:
    def __init__(self,tableau_matrix,lp_problem):
        self.matrix=tableau_matrix.tableau_matrix.copy()
        self.basis=tableau_matrix.initial_basis.copy()
        self.artificial_cols = tableau_matrix.artificial_cols.copy()
        self.steps=[]
        self.result=None
        self.lp_problem=lp_problem

    def _log_step(self, message="", pivot_row=None, pivot_col=None):
        step_data = {
            "message": message,
            "matrix": self.matrix.copy(),
            "basis": self.basis.copy(),
            "pivot_row": pivot_row,
            "pivot_col": pivot_col
        }
        self.steps.append(step_data)


    def simple_solve(self):
        while(True):
            z_row=self.matrix[len(self.matrix)-1]
            min_index=np.argmin(z_row[0:len(self.matrix[0])-1])

            if z_row[min_index]>=0:
                self._log_step("Optimal solution reached")
                return "optimal"


            else:
                min_pivot_index=-1
                min_current=100000
                for i in range(len(self.matrix)-1):
                    if self.matrix[i][min_index]<=0: continue
                    else:
                        current = self.matrix[i][len(self.matrix[0]) - 1] / self.matrix[i][min_index]
                        if current<0: continue
                        if current<min_current:
                            min_current=current
                            min_pivot_index=i

                if min_pivot_index==-1 :
                    self._log_step("Problem is unbounded")
                    return "unbounded"
                self._log_step(f"Pivot → Row {min_pivot_index}, Col {min_index}", pivot_row=min_pivot_index, pivot_col=min_index)
                self._pivot(min_pivot_index,min_index)



    def phase_1(self):
        self._log_step("Phase 1 — Starting (minimize artificial variables)")
        original_Zrow = self.matrix[len(self.matrix)-1].copy()
        w_row=np.zeros(len(self.matrix[0]))
        for col in self.artificial_cols:
            w_row[col]=1
        for i in range(len(self.matrix) - 1):
            basic_var = self.basis[i]
            if basic_var in self.artificial_cols:
                w_row = w_row - self.matrix[i]

        self.matrix[len(self.matrix)-1]=w_row
        self._log_step("Phase 1 — W-row constructed")
        status = self.simple_solve()
        optimal_w_value = self.matrix[-1][-1]
        if optimal_w_value < -1e-7:
            self._log_step("Phase 1 — Infeasible (W* != 0)")
            return "infeasible"

        self._log_step("Phase 1 — Feasible solution found, restoring Z-row")
        self.matrix[-1] = original_Zrow
        return "success"

    def solve(self):
        if len(self.artificial_cols) > 0:
            status = self.phase_1()
            if status == "infeasible":
                self.result = "infeasible"
                return None

            self._prepare_z_row_for_phase2()

        self.result = self.simple_solve()
        if self.result == "unbounded":
            return None
        return self._write_result()

    #hany part

    def  _prepare_z_row_for_phase2(self):
        return




    def _write_result(self):
        solution_dict={}
        variables_num=len(self.lp_problem.obj_fn_values)
        variables_final_value=[]
        for i in range(variables_num):
            if i in self.basis:
                variables_final_value.append(float(self.matrix[self.basis.index(i)][len(self.matrix[0])-1]))
            else :
                variables_final_value.append(0)
        solution_dict["variables"]=variables_final_value
        optimal_value=self.matrix[len(self.matrix)-1][len(self.matrix[0])-1]
        # For min problems the Z-row stores positive coefficients,
        # so the bottom-right cell is -Z*; negate to get the true Z*.
        if self.lp_problem.obj_fn_type == ObjectiveFunctionType.min:
            optimal_value = -optimal_value
        solution_dict["optimal_value"]=float(optimal_value)
        return solution_dict

    def _pivot(self,pivot_row,pivot_column):
        self.matrix[pivot_row]=self.matrix[pivot_row]/self.matrix[pivot_row][pivot_column]
        for i in range(len(self.matrix)):
            if i==pivot_row:continue
            factor=self.matrix[i][pivot_column]*-1
            self.matrix[i]=factor*self.matrix[pivot_row]+self.matrix[i]
        self.basis[pivot_row]=pivot_column


