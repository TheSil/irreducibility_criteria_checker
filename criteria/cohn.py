import sympy
import sys

from irreduc_utils import create_polynomial, poly_non_zero_exps, check_common
from irreduc_types import VAR_X, CheckResult, IRREDUCIBLE, REDUCIBLE, UNKNOWN


class CohnCriterion:
    def __init__(self, max_p=None):
        self.name = "Cohn's irreducibility criterion"
        self.max_p = max_p

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
            if sympy.isprime(val) and (not self.max_p or val < self.max_p):
                return CheckResult(IRREDUCIBLE, {"base": base, "p": val})

        return CheckResult(UNKNOWN)


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], CohnCriterion())
