class Constraint:
    def __init__(self, lhs, constraint_type,rhs):
        self.lhs = lhs
        self.constraint_type = constraint_type
        self.rhs = rhs