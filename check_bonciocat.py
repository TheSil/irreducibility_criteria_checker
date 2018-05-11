import sympy
from irreducibility_common import get_all_polygons


def check_bonciocat(f):
    # https://arxiv.org/pdf/1304.0874.pdf advanced use of newton polygons
    # Theorem A'
    polygons = get_all_polygons(f)

    # we need k>=2 of primes, but k==1 is okay as well
    k = len(polygons)
    if k < 1:
        return False, None

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
            Sps[prime] = S

    if not Sps:
        return False, None

    # final part, intersection...
    inter = set.intersection(*list(Sps.values()))

    if len(inter) > 0:
        return False, None

    # we have succeeded!
    return True, Sps


if __name__ == '__main__':
    import sys
    from irreducibility_common import create_polynomial

    input = sys.argv[1]
    poly = create_polynomial(input)
    p = check_bonciocat(poly)
    if p is not None:
        print('Polynomial %s is irreducible by Bonciocat with p=%i' % (input, p))
    else:
        print('Polynomial %s is NOT irreducible by Bonciocat' % input)
