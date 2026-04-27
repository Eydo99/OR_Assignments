import numpy as np
from utils.enums.obj_fn_type import ObjectiveFunctionType


class SimplexSolver:
    def __init__(self,tableau_matrix,lp_problem):
        self.matrix=tableau_matrix.tableau_matrix.copy()
        self.basis=tableau_matrix.initial_basis.copy()
        self.steps=[]
        self.result=None
        self.lp_problem=lp_problem


    def simple_solve(self):
        while(True):
            z_row=self.matrix[len(self.matrix)-1]
            min_index=np.argmin(z_row[0:len(self.matrix[0])-1])

            if z_row[min_index]>=0:
                self.result="optimal"
                return self._write_result()

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
                    self.result="unbounded"
                    return None
                self._pivot(min_pivot_index,min_index)



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
        solution_dict["optimal_value"]=float(optimal_value)
        return solution_dict

    def _pivot(self,pivot_row,pivot_column):
        self.matrix[pivot_row]=self.matrix[pivot_row]/self.matrix[pivot_row][pivot_column]
        for i in range(len(self.matrix)):
            if i==pivot_row:continue
            factor=self.matrix[i][pivot_column]*-1
            self.matrix[i]=factor*self.matrix[pivot_row]+self.matrix[i]
        self.basis[pivot_row]=pivot_column


