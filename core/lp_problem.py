class LPProblem:
    def __init__(self,obj_fn_type,obj_fn_values,constraints,restrictions):
        self.obj_fn_type = obj_fn_type
        self.obj_fn_values = obj_fn_values
        self.constraints = constraints
        self.restrictions = restrictions

