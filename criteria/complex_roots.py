import sys

from irreduc_utils import create_polynomial, poly_non_zero_exps, check_common, get_coeff
from irreduc_types import VAR_X, IRREDUCIBLE, REDUCIBLE, UNKNOWN


class ComplexRootsCriterion:
    def __init__(self, max_p=None):
        self.name = "Complex roots hunting"
        self.max_p = max_p

    def name(self):
        return self.name

    def check(self, f):
        import mpmath
        import sympy

        const_coeff = f.TC()
        if const_coeff == 0:
            return REDUCIBLE, None

        # const coefficient needs to be prime
        if not sympy.isprime(abs(const_coeff)):
            return UNKNOWN, None

        if self.max_p and abs(const_coeff) >= self.max_p:
            return UNKNOWN, None

        # need to be monic
        lead_coeff = f.LC()
        if lead_coeff != 1:
            return UNKNOWN, None

        # check if there are roots inside as well as outside of unit circle
        try:
            coeffs = [int(x) for x in
                      f.all_coeffs()]  # converting to Python native ints, otherwise polyroots gets stuck
            all = mpmath.polyroots(coeffs, maxsteps=100)
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
                return IRREDUCIBLE, {"inside/on": inside_unit_circle + on_unit_circle,
                                                 "outside": outside_unit_circle,
                                                 "p": const_coeff}
        except mpmath.libmp.libhyper.NoConvergence as e:
            # could not get complex roots, too bad
            pass

        return UNKNOWN, None


class ComplexRootsCriterion2:
    def __init__(self):
        self.name = "Complex roots hunting 2"

    def name(self):
        return self.name

    def check(self, f):
        # see question body in https://mathoverflow.net/questions/214962/criteria-for-irreducibility-using-the-location-of-complex-roots
        import mpmath

        const_coeff = f.TC()
        if const_coeff == 0:
            return REDUCIBLE, None

        # need to be monic
        lead_coeff = f.LC()
        if lead_coeff != 1:
            return UNKNOWN, None

        # check if there are roots inside as well as outside of unit circle
        try:
            coeffs = [int(x) for x in
                      f.all_coeffs()]  # converting to Python native ints, otherwise polyroots gets stuck
            all = mpmath.polyroots(coeffs, maxsteps=100)
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

            if (outside_unit_circle + on_unit_circle == 1):
                return IRREDUCIBLE, {"inside": inside_unit_circle,
                                                 "outside/on": outside_unit_circle + on_unit_circle}
        except mpmath.libmp.libhyper.NoConvergence as e:
            # could not get complex roots, too bad
            pass

        return UNKNOWN, None

class ComplexRootsCriterion3:
    def __init__(self, max_p=None):
        self.name = "Complex roots hunting 3"
        self.max_p = max_p

    def name(self):
        return self.name

    def check(self, f):
        # reciprocal version of Dimitrov's first comment in https://mathoverflow.net/questions/214962/criteria-for-irreducibility-using-the-location-of-complex-roots
        import mpmath
        import sympy

        const_coeff = f.TC()
        if const_coeff == 0:
            return REDUCIBLE, None

        # constant coeff needs to be in form +-p^d
        primes = sympy.ntheory.factorint(abs(const_coeff))
        if len(primes) != 1:
            return UNKNOWN, None

        # extract p
        p = next(iter(primes.keys()))

        # linear coefficients must not be divisible by p
        a1 = get_coeff(f, 1)
        if a1 % p == 0:
            return UNKNOWN, None

        if self.max_p and abs(const_coeff) >= self.max_p:
            return UNKNOWN, None

        # check if there are roots inside as well as outside of unit circle
        try:
            coeffs = [int(x) for x in
                      f.all_coeffs()]  # converting to Python native ints, otherwise polyroots gets stuck
            all = mpmath.polyroots(coeffs, maxsteps=100)
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

            if (inside_unit_circle + on_unit_circle == 0):
                return IRREDUCIBLE, {"inside/on": inside_unit_circle + on_unit_circle,
                                                 "outside": outside_unit_circle,
                                                 "p": p}
        except Exception as e:
            # could not get complex roots, too bad
            pass

        return UNKNOWN, None

if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], ComplexRootsCriterion())
    check_common(poly, sys.argv[1], ComplexRootsCriterion2())
    check_common(poly, sys.argv[1], ComplexRootsCriterion3())
