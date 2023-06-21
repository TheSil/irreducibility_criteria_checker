import sympy
import sys

from irreduc_utils import create_polynomial, get_all_polygons, check_common, poly_non_zero_exps
from irreduc_types import VAR_X, IRREDUCIBLE, UNKNOWN


class BonciocatCriterion:
    def __init__(self):
        self.name = "Bonciocat's irreducibility criterion"

    def name(self):
        return self.name

    def check(self, f):
        # https://arxiv.org/pdf/1304.0874.pdf advanced use of newton polygons
        # Theorem A'
        polygons = get_all_polygons(f)

        # we need k>=2 of primes, but k==1 is okay as well
        k = len(polygons)
        if k < 1:
            return UNKNOWN, None

        Sps = {}

        # dummy set used for comparsion later
        i = 1
        trivial = set()
        while 2 * i <= f.degree():
            trivial.add(i)
            i += 1

        for prime in polygons:
            # compute mi_s, xi_s
            ms = []
            xs = []
            r = len(polygons[prime])
            for point_ind in range(r - 1):
                point = polygons[prime][point_ind]
                point_next = polygons[prime][point_ind + 1]
                j = point[0]
                vp = point[1]
                j_next = point_next[0]
                vp_next = point_next[1]
                m = sympy.gcd(vp - vp_next, j_next - j)
                ms.append(m)

                x = (j_next - j) // m
                xs.append(x)

            # generate all linear combinations...
            S = set()
            S.add(0)
            for l in range(1, r):
                tmp = set()
                m = ms[l - 1]
                for n in range(0, m + 1):
                    for s in S:
                        new = s + n * xs[l - 1]
                        if new > 0 and (2 * new <= f.degree()):
                            tmp.add(new)

                S = S.union(tmp)

            S.remove(0)

            # we are interested only in those sets that are not just full set of {1,2,...,n/2}
            if S != trivial:
                Sps['S%i' % prime] = S

        if not Sps:
            return UNKNOWN, None

        # final part, intersection...
        inter = set.intersection(*list(Sps.values()))

        if len(inter) > 0:
            return UNKNOWN, None

        # we have succeeded!
        return IRREDUCIBLE, Sps


class BonciocatPrimeCriterion:
    def __init__(self):
        self.name = "Bonciocat's prime at large enough input criterion"

    def name(self):
        return self.name

    def check(self, f):
        # https://www.tandfonline.com/doi/epdf/10.1080/00927872.2021.2014514?needAccess=true&role=button
        # f non-negative integer coefficients and deg f >= 2
        # If f(m) is prime for m > (deg f)/3 + 1, then f is irreducible
        # in fact m > 1/ sin(pi/n), so we have a weaker version where

        # ensure coefficients are non-negative
        for _, coeff in poly_non_zero_exps(f):
            if coeff < 0:
                return UNKNOWN, None

        # deg f >= 2
        if f.degree() < 2:
            return UNKNOWN, None

        m = f.degree() // 3 + 2
        max_m = m + 100
        max_p = 1000000
        val = f.subs(VAR_X, m)
        while m <= max_m and val <= max_p:
            if sympy.isprime(val):
                return IRREDUCIBLE, {"m": m, "p": val}
            m += 1

        return UNKNOWN, None


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], BonciocatCriterion())
