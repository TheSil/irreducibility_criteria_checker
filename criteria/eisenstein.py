import sympy
import sys

from irreduc_utils import create_polynomial, poly_non_zero_exps, check_common
from irreduc_types import IRREDUCIBLE, REDUCIBLE, UNKNOWN


class EisensteinCriterion:
    def __init__(self):
        self.name = "Eisenstein's irreducibility criterion"

    def check(self, f):
        const_coeff = f.TC()
        if const_coeff == 0:
            return REDUCIBLE, None
        primes = sympy.ntheory.factorint(const_coeff)
        for p in primes:
            power = primes[p]
            if power == 1:
                # good candidate, it must not divide leading term
                lead_coeff = f.LC()
                if lead_coeff % p == 0:
                    # bad luck
                    continue
                # it must divide or other terms
                ok = True
                for exp, coeff in poly_non_zero_exps(f):
                    if exp != f.degree():
                        if coeff % p != 0:
                            # bad luck...
                            ok = False
                            break
                if ok:
                    return IRREDUCIBLE, {"p": p}
        return UNKNOWN, None


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], EisensteinCriterion())
