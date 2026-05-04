from enum import Enum

class ConstraintType(Enum):
    smaller_equal = "<="
    greater_equal = ">="
    equal = "="