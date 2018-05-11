import sympy
from irreducibility_common import poly_non_zero_exps
from irreducibility_common import VAR_X


def check_cohn(f):
    # first we need to ensure coefficients are non-negative
    max_coeff = 0
    for exp, coeff in poly_non_zero_exps(f):
        if coeff < 0:
            return None, None
        max_coeff = max(max_coeff, coeff)

    check_range = 30
    for base in range(max_coeff + 1, max_coeff + 1 + check_range):
        val = f.subs(VAR_X, base)
        if sympy.isprime(val):
            return base, val

    return None, None


if __name__ == '__main__':
    import sys
    from irreducibility_common import create_polynomial

    input = sys.argv[1]
    poly = create_polynomial(input)
    b, p = check_cohn(poly)
    if b is not None:
        print('Polynomial %s is irreducible by Cohn with p=%i' % (input, p))
    else:
        print('Polynomial %s is NOT irreducible by Cohn' % input)
