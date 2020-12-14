import sympy
import sys

from irreduc_utils import create_polynomial, poly_non_zero_exps, check_common, get_coeff
from irreduc_types import IRREDUCIBLE, REDUCIBLE, UNKNOWN


class EisensteinCriterionV2:
    def __init__(self):
        self.name = "Modified Eisenstein's irreducibility criterion"

    def check(self, f):
        # see https://www.lehigh.edu/~shw2/preprints/eisenstein.pdf,
        # and https://math.stackexchange.com/questions/3589657/prove-polynomial-is-irreducible/3590300#3590300
        const_coeff = f.TC()
        if const_coeff == 0:
            return REDUCIBLE, None
        linear_coeff = get_coeff(f, 1)
        if linear_coeff == 0:
            return UNKNOWN, None
        primes = sympy.ntheory.factorint(linear_coeff)
        for p in primes:
            power = primes[p]
            if power == 1:
                # good candidate, it must not divide leading term
                lead_coeff = f.LC()
                if lead_coeff % p == 0:
                    # bad luck
                    continue
                # it must divide or other terms
                for exp, coeff in poly_non_zero_exps(f):
                    if exp != f.degree():
                        if coeff % p != 0:
                            # bad luck...
                            return UNKNOWN, None

                # finally the polynomial must not have rational roots
                numerators = sympy.ntheory.factorint(const_coeff)
                denominators = sympy.ntheory.factorint(lead_coeff)
                for num in numerators:
                    for denom in denominators:
                        for sign in (-1, 1):
                            if f.eval(sympy.Rational(sign * num, denom)) == 0:
                                # rational root...
                                return UNKNOWN, None

                return IRREDUCIBLE, {"p": p}
        return UNKNOWN, None


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], EisensteinCriterionV2())
