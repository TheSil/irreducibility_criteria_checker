import sys
from irreducibility_common import create_polynomial
from irreducibility_common import poly_all_exps
from irreducibility_common import CheckResult
from irreducibility_common import ResultEnum
from irreducibility_common import check_common


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
            return CheckResult(ResultEnum.UNKNOWN)
        for exp, coeff in poly_all_exps(f):
            if exp != f.degree():
                coeff = -coeff
                if coeff < last or coeff <= 0:
                    return CheckResult(ResultEnum.UNKNOWN)
                last = coeff
        return CheckResult(ResultEnum.IRREDUCIBLE)


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], BrauerCriterion())
