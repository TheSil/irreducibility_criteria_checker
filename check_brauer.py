from irreducibility_common import poly_all_exps


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
