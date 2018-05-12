import sympy
import sys

from irreduc_utils import create_polynomial, poly_non_zero_exps, check_common
from irreduc_types import CheckResult, IRREDUCIBLE, REDUCIBLE, UNKNOWN


class OsadaCriterion:
    def __init__(self):
        self.name = "Osada's irreducibility criterion"

    def name(self):
        return self.name

    def check(self, f):
        # Polynomials - Prasolov - Theorem 2.2.7 ([Os1]) part a)
        lead_coeff = f.LC()
        if lead_coeff != 1:
            return CheckResult(UNKNOWN)

        const_coeff = abs(f.TC())
        if not sympy.isprime(const_coeff):
            return CheckResult(UNKNOWN)

        s = 0
        for exp, coeff in poly_non_zero_exps(f):
            if exp != f.degree() and exp != 0:
                s += abs(coeff)

        if const_coeff > 1 + s:
            return CheckResult(IRREDUCIBLE, {'s': const_coeff})
        return CheckResult(UNKNOWN)


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], OsadaCriterion())
