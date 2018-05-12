import sympy
import sys

from irreducibility_common import create_polynomial, get_all_polygons, check_common
from irreducibility_common import CheckResult
from irreducibility_common import IRREDUCIBLE, REDUCIBLE, UNKNOWN


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
            return CheckResult(UNKNOWN)

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
            return CheckResult(UNKNOWN)

        # final part, intersection...
        inter = set.intersection(*list(Sps.values()))

        if len(inter) > 0:
            return CheckResult(UNKNOWN)

        # we have succeeded!
        return CheckResult(IRREDUCIBLE, Sps)


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], BonciocatCriterion())
