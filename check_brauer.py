import sys

from irreduc_utils import create_polynomial, poly_all_exps, check_common
from irreduc_types import CheckResult, IRREDUCIBLE, REDUCIBLE, UNKNOWN


class BrauerCriterion:
    def __init__(self):
        self.name = "Brauer's irreducibility criterion"

    def name(self):
        return self.name

    def check(self, f):
        # Polynomials - Prasolov - Theorem 2.2.6 ([Br])
        last = 0
        lead_coeff = f.LC()
        if lead_coeff != 1:
            return CheckResult(UNKNOWN)
        for exp, coeff in poly_all_exps(f):
            if exp != f.degree():
                coeff = -coeff
                if coeff < last or coeff <= 0:
                    return CheckResult(UNKNOWN)
                last = coeff
        return CheckResult(IRREDUCIBLE)


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], BrauerCriterion())
