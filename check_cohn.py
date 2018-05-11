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
    for b in range(max_coeff + 1, max_coeff + 1 + check_range):
        val = f.subs(VAR_X, b)
        if sympy.isprime(val):
            return (b, val)

    return None, None