from enum import Enum

class Term(str, Enum):
    F = "Fall"
    S = "Spring"
    Q = "Summer"

    def next(self):
        order = [Term.F, Term.S, Term.Q]
        idx = order.index(self)
        return order[(idx + 1) % len(order)]  # wrap around
    
    def int_to_Term(value: int):
        if value == 0:
            return "Fall"
        elif value == 1:
            return "Spring"
        else:
            return "Summer"