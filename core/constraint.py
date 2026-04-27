class Constraint:
    def __init__(self, LHS, constraint_type,RHS):
        self.LHS = LHS
        self.constraint_type = constraint_type
        self.RHS = RHS