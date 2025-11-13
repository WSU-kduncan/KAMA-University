from enum import Enum

class Term(str, Enum):
    F = "Fall"
    S = "Spring"
    Q = "Summer"

    def next(self):
        order = [Term.F, Term.S, Term.Q]
        idx = order.index(self)
        return order[(idx + 1) % len(order)]  # wrap around