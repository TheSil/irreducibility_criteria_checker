import sympy
import math
from irreducibility_common import poly_non_zero_exps


def check_murty(f):
    # http://cms.dm.uba.ar/academico/materias/2docuat2011/teoria_de_numeros/Irreducible.pdf
    # Theorem 1
    h = 0
    for exp, coeff in poly_non_zero_exps(f):
        if exp != f.degree():
            h = max(h, abs(coeff / f.LC()))

    nmin = math.ceil(h + 2)
    for n in range(nmin, nmin + 5):
        val = f.eval(n)
        if sympy.isprime(val):
            return n, val
    return None, None


if __name__ == '__main__':
    import sys
    from irreducibility_common import create_polynomial

    input = sys.argv[1]
    poly = create_polynomial(input)
    n, p = check_murty(poly)
    if n is not None:
        print('Polynomial %s is irreducible by Murty for n=%i, p=%i' % (input, n, p))
    else:
        print('Polynomial %s is NOT irreducible by Murty' % input)
