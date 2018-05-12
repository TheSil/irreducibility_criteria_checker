import sympy
import sys

from irreducibility_common import create_polynomial, poly_non_zero_exps, check_common
from irreducibility_common import VAR_X
from irreducibility_common import CheckResult
from irreducibility_common import IRREDUCIBLE, REDUCIBLE, UNKNOWN


class CohnCriterion:
    def __init__(self):
        self.name = "Cohn's irreducibility criterion"

    def name(self):
        return self.name

    def check(self, f):
        # first we need to ensure coefficients are non-negative
        max_coeff = 0
        for exp, coeff in poly_non_zero_exps(f):
            if coeff < 0:
                return CheckResult(UNKNOWN)
            max_coeff = max(max_coeff, coeff)

        check_range = 30
        for base in range(max_coeff + 1, max_coeff + 1 + check_range):
            val = f.subs(VAR_X, base)
            if sympy.isprime(val):
                return CheckResult(IRREDUCIBLE, {"base": base, "p": val})

        return CheckResult(UNKNOWN)


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], CohnCriterion())
