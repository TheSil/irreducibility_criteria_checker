import sympy
import sys
from itertools import chain, combinations

from irreduc_utils import create_polynomial, check_common
from irreduc_types import CheckResult, IRREDUCIBLE, REDUCIBLE, UNKNOWN


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def subsets_sums(s):
    sums = set()
    for subset in powerset(s):
        d = sum(subset)
        if d > 0:
            sums.add(d)
    return sums

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

        res = {}
        if irreduc_primes:
            res["p"] = irreduc_primes

        # check if the degrees are compatible, first for degrees in Fp[x], we calculate by summing
        # all possible degrees of irreducible factors in Z[x]
        sums = {}
        trivial = set(range(1, f.degree()+1))
        for p in irreduc_factors_degrees:
            sums_p = subsets_sums(irreduc_factors_degrees[p])
            if sums_p != trivial:
                sums[p] = sums_p

        if not sums:
            return CheckResult(UNKNOWN)

        # then if intersection of these is empty or {deg(f)}, then lesser degree factor is impossible
        # thus polynomial will have to be irreducible
        inter = set.intersection(*list(sums.values()))
        if f.degree() in inter:
            inter.remove(f.degree())

        if not inter:
            # intersection is empty, imcompatible factors!
            res["degrees"] = sums

        if res:
            return CheckResult(IRREDUCIBLE, res)

        return CheckResult(UNKNOWN)


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], GaloisFieldsCriterion())
