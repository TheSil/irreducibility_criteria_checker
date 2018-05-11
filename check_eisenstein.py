import sympy
from irreducibility_common import poly_non_zero_exps


def check_eisenstein(f):
    const_coeff = f.TC()
    if const_coeff == 0:
        return None
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
                return p
    return None


if __name__ == '__main__':
    import sys
    from irreducibility_common import create_polynomial

    input = sys.argv[1]
    poly = create_polynomial(input)
    p = check_eisenstein(poly)
    if p is not None:
        print('Polynomial %s is irreducible by Eisenstein with p=%i' % (input, p))
    else:
        print('Polynomial %s is NOT irreducible by Eisenstein' % input)
