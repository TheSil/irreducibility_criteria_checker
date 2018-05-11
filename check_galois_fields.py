import sympy


def check_galois_fields(f, min_p=2, max_p=30):
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
        return True, irreduc_primes

    # TODO check if the degrees are compatible, because if not, it also means the polynomial is irreducible
    return False, None


if __name__ == '__main__':
    import sys
    from irreducibility_common import create_polynomial

    input = sys.argv[1]
    poly = create_polynomial(input)
    b, p = check_galois_fields(poly)
    if b:
        print('Polynomial %s is irreducible over Galois fields fo p=%s' % (input, str(p)))
    else:
        print('Polynomial %s is NOT irreducible over Galois fields' % input)
