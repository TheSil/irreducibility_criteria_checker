import sys

from irreduc_utils import create_polynomial, poly_non_zero_exps, check_common, get_coeff
from irreduc_types import VAR_X, CheckResult, IRREDUCIBLE, REDUCIBLE, UNKNOWN


class ComplexRootsCriterion:
    def __init__(self):
        self.name = "Complex roots hunting"

    def name(self):
        return self.name

    def check(self, f):
        import mpmath
        import sympy

        const_coeff = f.TC()
        if const_coeff == 0:
            return CheckResult(REDUCIBLE)

        # const coefficient needs to be prime
        if not sympy.isprime(abs(const_coeff)):
            return CheckResult(UNKNOWN)

        # need to be monic
        lead_coeff = f.LC()
        if lead_coeff != 1:
            return CheckResult(UNKNOWN)

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

            if (inside_unit_circle + on_unit_circle == 0) or (outside_unit_circle == 0):
                return CheckResult(IRREDUCIBLE, {"inside": inside_unit_circle + on_unit_circle,
                                                 "outside": outside_unit_circle,
                                                 "p": const_coeff})
        except mpmath.libmp.libhyper.NoConvergence as e:
            # could not get complex roots, too bad
            pass

        return CheckResult(UNKNOWN)



if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], ComplexRootsCriterion())
