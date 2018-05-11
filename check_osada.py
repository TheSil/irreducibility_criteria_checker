import sympy
from irreducibility_common import poly_non_zero_exps


def check_osada(f):
    # Polynomials - Prasolov - Theorem 2.2.7 ([Os1]) part a)
    lead_coeff = f.LC()
    if lead_coeff != 1:
        return False, None

    const_coeff = abs(f.TC())
    if not sympy.isprime(const_coeff):
        return False, None

    s = 0
    for exp, coeff in poly_non_zero_exps(f):
        if exp != f.degree() and exp != 0:
            s += abs(coeff)

    return const_coeff > 1 + s, const_coeff
