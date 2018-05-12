import sympy
import sys
from irreducibility_common import create_polynomial
from irreducibility_common import CheckResult
from irreducibility_common import ResultEnum
from irreducibility_common import check_common


class PolyaCriterion:
    def __init__(self):
        self.name = "Polya's irreducibility criterion"

    def name(self):
        return self.name

    def check(self, f):
        # Polynomials by Prasolov, Theorem 2.2.8 (Polya)
        n = f.degree()
        m = (n + 1) // 2
        suitable = []
        rhs = sympy.factorial(m) / (2 ** m)
        for a in range(-20, 20 + 1):
            val = abs(f.eval(a))
            if val == 0:
                # clearly this is reducible...
                return CheckResult(ResultEnum.UNKNOWN)
            if val < rhs:
                suitable.append(a)
        if len(suitable) >= n:
            return CheckResult(ResultEnum.IRREDUCIBLE, {'a': suitable})
        return CheckResult(ResultEnum.UNKNOWN)


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], PolyaCriterion())