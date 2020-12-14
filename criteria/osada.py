import sympy
import sys

from irreduc_utils import create_polynomial, poly_non_zero_exps, check_common
from irreduc_types import IRREDUCIBLE, UNKNOWN


class OsadaCriterion:
    def __init__(self, max_p=None):
        self.name = "Osada's irreducibility criterion"
        self.max_p = max_p

    def name(self):
        return self.name

    def check(self, f):
        # Polynomials - Prasolov - Theorem 2.2.7 ([Os1]) part a)
        lead_coeff = f.LC()
        if lead_coeff != 1:
            return UNKNOWN, None

        const_coeff = abs(f.TC())
        if not sympy.isprime(const_coeff):
            return UNKNOWN, None

        if self.max_p and const_coeff >= self.max_p:
            return UNKNOWN, None

        s = 0
        for exp, coeff in poly_non_zero_exps(f):
            if exp != f.degree() and exp != 0:
                s += abs(coeff)

        if const_coeff > 1 + s:
            return IRREDUCIBLE, {'s': const_coeff}
        return UNKNOWN, None


class OsadaCriterionNonSharp:
    def __init__(self, max_p=None):
        self.name = "Osada's (non-sharp) irreducibility criterion"
        self.max_p = max_p

    def name(self):
        return self.name

    def check(self, f):
        # Polynomials - Prasolov - Theorem 2.2.7 ([Os1]) part b)
        lead_coeff = f.LC()
        if lead_coeff != 1:
            return UNKNOWN, None

        const_coeff = abs(f.TC())
        if not sympy.isprime(const_coeff):
            return UNKNOWN, None

        if self.max_p and const_coeff >= self.max_p:
            return UNKNOWN, None

        s = 0
        for exp, coeff in poly_non_zero_exps(f):
            if exp != f.degree() and exp != 0:
                s += abs(coeff)

        if const_coeff < 1 + s:
            return UNKNOWN, None

        import mpmath

        # check if there are roots inside as well as outside of unit circle
        try:
            all = mpmath.polyroots(f.all_coeffs(), maxsteps=100)
            inside_unit_circle = 0
            outside_unit_circle = 0
            on_unit_circle = 0
            for root in all:
                root_size = abs(root)
                if root_size == 1:
                    on_unit_circle += 1
                elif root_size < 1:
                    inside_unit_circle += 1
                else:
                    outside_unit_circle += 1

            if on_unit_circle == 0:
                return IRREDUCIBLE, {'s': const_coeff,
                                                 "on": on_unit_circle}
        except mpmath.libmp.libhyper.NoConvergence:
            # could not get complex roots, too bad
            pass

        return UNKNOWN, None


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], OsadaCriterion())
    check_common(poly, sys.argv[1], OsadaCriterionNonSharp())
