import sys
from irreducibility_common import poly_all_exps
from irreducibility_common import create_polynomial


def check_brauer(f):
    # Polynomials - Prasolov - Theorem 2.2.6 ([Br])
    last = 0
    lead_coeff = f.LC()
    if lead_coeff != 1:
        return False
    for exp, coeff in poly_all_exps(f):
        if exp != f.degree():
            coeff = -coeff
            if coeff < last or coeff <= 0:
                return False
            last = coeff
    return True


if __name__ == '__main__':
    import sys
    from irreducibility_common import create_polynomial

    input = sys.argv[1]
    poly = create_polynomial(input)
    p = check_brauer(poly)
    if p is not None:
        print('Polynomial %s is irreducible by Brauer with p=%i' % (input, p))
    else:
        print('Polynomial %s is NOT irreducible by Brauer' % input)
