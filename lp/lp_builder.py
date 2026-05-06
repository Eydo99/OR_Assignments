from utils.enums.role import Role


class LPBuilder:
    def __init__(self,payoff_matrix,computer_role):
        self.payoff_matrix = payoff_matrix
        self.computer_role = computer_role

    def build_lp_problem(self)->dict:
        lp_problem_dict=dict()
        lp_problem_dict['obj_fn_type']="max" if(self.computer_role==Role.hider) else "min"
        lp_list=[0]*len(self.payoff_matrix)
        lp_list.append(1)
        lp_problem_dict['obj_fn_values']=lp_list
        lp_problem_dict['constraints']=self._build_constraint_list()
        lp_problem_dict['restrictions']=["non_negative"]*len(self.payoff_matrix)+["free"]

        return lp_problem_dict



    def _build_constraint_list(self)->list:
        constraint_list = self._build_hider_constraints() if(self.computer_role==Role.hider) else self._build_seeker_constraints()

        constraint_dict = dict()
        constraint_dict['RHS'] = 1
        constraint_dict["constraint_type"] = "="
        LHS=[]
        for _ in range(len(self.payoff_matrix)):
            LHS.append(1)
        LHS.append(0)
        constraint_dict['LHS'] = LHS
        constraint_list.append(constraint_dict)

        return constraint_list


    def _build_hider_constraints(self)->list:
        constraint_list = []
        for col in range(len(self.payoff_matrix)):
            constraint_dict = dict()
            constraint_dict['RHS'] = 0
            constraint_dict["constraint_type"] = "<="
            LHS = []
            for row in range(len(self.payoff_matrix)):
                LHS.append(-1 * self.payoff_matrix[row][col])
            LHS.append(1)
            constraint_dict['LHS'] = LHS
            constraint_list.append(constraint_dict)
        return constraint_list

    def _build_seeker_constraints(self)->list:
        constraint_list = []
        for row in range(len(self.payoff_matrix)):
            constraint_dict = dict()
            constraint_dict['RHS'] = 0
            constraint_dict["constraint_type"] = ">="
            LHS = []
            for col in range(len(self.payoff_matrix)):
                LHS.append(-1 * self.payoff_matrix[row][col])
            LHS.append(1)
            constraint_dict['LHS'] = LHS
            constraint_list.append(constraint_dict)

        return constraint_list




