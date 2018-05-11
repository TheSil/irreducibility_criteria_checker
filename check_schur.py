from irreducibility_common import get_coeff


def check_schur(f):
    # http://www.math.uconn.edu/~kconrad/blurbs/gradnumthy/schurtheorem.pdf
    # Theorem 1, multiplied to get Z[x]
    n = f.degree()
    lead_coeff = f.LC()
    if abs(lead_coeff) != 1:
        return False
    fact = n
    for exp in reversed(range(1, n)):
        coeff = get_coeff(f, exp)
        if coeff % fact != 0:
            return False
        fact *= exp
    # fact now contains n!
    const_coeff = f.TC()
    if const_coeff != fact:
        return False

    return True
