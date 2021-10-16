from sympy.functions.combinatorial.factorials import RisingFactorial
import sys

from irreduc_utils import create_polynomial, check_common
from irreduc_types import IRREDUCIBLE, REDUCIBLE, UNKNOWN


class LevitCriterion:
    def __init__(self):
        self.name = "Levit's irreducibility criterion"

    def name(self):
        return self.name

    def check(self, f):
        # Levit, Irreducibility of Polynomials with Low Absolute Values, Theorem 2
        n = f.degree()
        N = (n + 1) // 2
        suitable = []

        rhs = RisingFactorial((n//2)/2, N) / (2 ** (N-1))
        for a in range(-20, 20 + 1):
            val = abs(f.eval(a))
            if val == 0:
                # clearly this is reducible...
                return REDUCIBLE, None
            if val < rhs:
                suitable.append(a)
        if len(suitable) >= n:
            return IRREDUCIBLE, {'a': suitable}
        return UNKNOWN, None


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], LevitCriterion())
