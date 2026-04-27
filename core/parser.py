from core.lp_problem import LPProblem
import numpy as np
from core.constraint import Constraint
from utils.enums.constraint_type import ConstraintType
from utils.enums.obj_fn_type import ObjectiveFunctionType
from utils.enums.restriction_type import RestrictionType


class Parser:
    def __init__(self,data):
        self.data = data

    def build_lp_problem(self)->LPProblem|None:
        obj_fn_type = ObjectiveFunctionType(self.data["obj_fn_type"])
        obj_fn_values =np.array(self.data["obj_fn_values"])
        constraints=[]
        for constraint in self.data["constraints"]:
            LHS=np.array(constraint["LHS"])
            RHS=constraint["RHS"]
            constraint_type=ConstraintType(constraint["constraint_type"])
            constraints.append(Constraint(LHS,constraint_type,RHS))
        restrictions =[]
        for restriction in self.data["restrictions"]:
            restrictions.append(RestrictionType(restriction))
        return LPProblem(obj_fn_type,obj_fn_values,constraints,restrictions)

