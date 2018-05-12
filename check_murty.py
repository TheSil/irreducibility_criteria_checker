import sympy
import math
import sys
from irreducibility_common import create_polynomial
from irreducibility_common import poly_non_zero_exps
from irreducibility_common import CheckResult
from irreducibility_common import ResultEnum
from irreducibility_common import check_common


class MurtyCriterion:
    def __init__(self):
        self.name = "Murty's irreducibility criterion"

    def name(self):
        return self.name

    def check(self, f):
        # http://cms.dm.uba.ar/academico/materias/2docuat2011/teoria_de_numeros/Irreducible.pdf
        # Theorem 1
        h = 0
        for exp, coeff in poly_non_zero_exps(f):
            if exp != f.degree():
                h = max(h, abs(coeff / f.LC()))

        nmin = math.ceil(h + 2)
        for n in range(nmin, nmin + 5):
            val = f.eval(n)
            if sympy.isprime(val):
                return CheckResult(ResultEnum.IRREDUCIBLE, {'n': n, 'p': val})
        return CheckResult(ResultEnum.UNKNOWN)


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], MurtyCriterion())
