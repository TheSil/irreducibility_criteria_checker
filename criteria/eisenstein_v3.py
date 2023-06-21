import sympy
import sys

from irreduc_utils import create_polynomial, poly_non_zero_exps, check_common, get_coeff
from irreduc_types import IRREDUCIBLE, REDUCIBLE, UNKNOWN


class EisensteinCriterionV3:
    def __init__(self):
        self.name = "Related Eisenstein's irreducibility criterion"

    def check(self, f):
        # based on https://math.stackexchange.com/questions/4721602
        # if p is an odd prime and f(x) satisfies following conditions:
        # - leading coefficient is +-p
        # - constant coefficient is +-p
        # - all other coefficients but one are divisible by p
        # - the one coefficient not divisible by p satisfies a_n = 1 mod p
        # Then f(x) is irreducible over Q
        const_coeff = f.TC()
        if const_coeff == 0:
            return REDUCIBLE, None

        p = abs(const_coeff)
        if not sympy.isprime(p) or p == 2:
            return UNKNOWN, None

        leading_coeff = f.LC()
        if abs(leading_coeff) != p:
            return UNKNOWN, None

        cnt = 0
        n = -1
        a_n = -1
        for exp, coeff in poly_non_zero_exps(f):
            if coeff % p != 0:
                if coeff % p != 1:
                    return UNKNOWN, None
                cnt += 1
                n = exp
                a_n = coeff
                if cnt > 1:
                    return UNKNOWN, None

        if cnt == 0:
            return UNKNOWN, None

        return IRREDUCIBLE, {"n": n, "a_n": a_n, "p": p}


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], EisensteinCriterionV3())
