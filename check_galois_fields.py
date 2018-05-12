import sympy
import sys
from irreducibility_common import create_polynomial
from irreducibility_common import CheckResult
from irreducibility_common import ResultEnum
from irreducibility_common import check_common


class GaloisFieldsCriterion:
    def __init__(self):
        self.name = "Galois Fields irreducibility"

    def name(self):
        return self.name

    def check(self, f, min_p=2, max_p=30):
        # checking through few small primes to see if it is perhaps
        # either irreducible in one of those, or the degrees of irreducible factors
        # are imcompatible
        from sympy.polys.galoistools import gf_factor
        from sympy.polys.domains import ZZ
        from sympy import primerange

        irreduc_factors_degrees = {}
        irreduc_primes = []
        for p in primerange(min_p, max_p + 1):
            try:
                irreduc_factors = gf_factor(f.all_coeffs(), p, ZZ)
                degrees = []
                for x in irreduc_factors[1]:
                    pol = x[0]
                    e = x[1]
                    degrees += e*[(len(pol)-1)]

                if len(degrees) == 1:
                    # irreducible by p...
                    irreduc_primes.append(p)

                # store irreducibility factors degrees for later
                irreduc_factors_degrees[p] = degrees
            except sympy.polys.polyerrors.NotInvertible:
                pass

        if irreduc_primes:
            return CheckResult(ResultEnum.IRREDUCIBLE, {"p": irreduc_primes})

        # TODO check if the degrees are compatible, because if not, it also means the polynomial is irreducible
        return CheckResult(ResultEnum.UNKNOWN)


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], GaloisFieldsCriterion())
