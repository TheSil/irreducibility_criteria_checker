import sys

from irreduc_utils import create_polynomial, check_common, get_coeff
from irreduc_types import IRREDUCIBLE, UNKNOWN


class SchurCriterion:
    def __init__(self):
        self.name = "Schur's irreducibility criterion"

    def name(self):
        return self.name

    def check(self, f):
        # http://www.math.uconn.edu/~kconrad/blurbs/gradnumthy/schurtheorem.pdf
        # Theorem 1, multiplied to get Z[x]
        n = f.degree()
        lead_coeff = f.LC()
        if abs(lead_coeff) != 1:
            return UNKNOWN, None
        fact = n
        for exp in reversed(range(1, n)):
            coeff = get_coeff(f, exp)
            if coeff % fact != 0:
                return UNKNOWN, None
            fact *= exp
        # fact now contains n!
        const_coeff = f.TC()
        if const_coeff != fact:
            return UNKNOWN, None

        return IRREDUCIBLE, None


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], SchurCriterion())
