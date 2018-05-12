import sympy
import sys
from irreducibility_common import create_polynomial
from irreducibility_common import poly_non_zero_exps
from irreducibility_common import CheckResult
from irreducibility_common import ResultEnum
from irreducibility_common import check_common


class OsadaCriterion:
    def __init__(self):
        self.name = "Galois Fields irreducibility"

    def name(self):
        return self.name

    def check(self, f):
        # Polynomials - Prasolov - Theorem 2.2.7 ([Os1]) part a)
        lead_coeff = f.LC()
        if lead_coeff != 1:
            return CheckResult(ResultEnum.UNKNOWN)

        const_coeff = abs(f.TC())
        if not sympy.isprime(const_coeff):
            return CheckResult(ResultEnum.UNKNOWN)

        s = 0
        for exp, coeff in poly_non_zero_exps(f):
            if exp != f.degree() and exp != 0:
                s += abs(coeff)

        if const_coeff > 1 + s:
            return CheckResult(ResultEnum.IRREDUCIBLE, {'s': const_coeff})
        return CheckResult(ResultEnum.UNKNOWN)


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], OsadaCriterion())
