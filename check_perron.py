from irreducibility_common import poly_non_zero_exps
from irreducibility_common import get_coeff


def check_perron(f):
    const_coeff = f.TC()
    if const_coeff == 0:
        return False
    lead_coeff = f.LC()
    if lead_coeff != 1:
        return False
    a_nm1 = abs(get_coeff(f, f.degree() - 1))
    s = 1
    for exp, coeff in poly_non_zero_exps(f):
        if exp < f.degree() - 1:
            s += abs(coeff)
    return a_nm1 > s


def check_perron_non_sharp(f):
    const_coeff = f.TC()
    if const_coeff == 0:
        return False
    lead_coeff = f.LC()
    if lead_coeff != 1:
        return False
    a_nm1 = abs(get_coeff(f, f.degree() - 1))
    s = 1
    for exp, coeff in poly_non_zero_exps(f):
        if exp < f.degree() - 1:
            s += abs(coeff)
    if a_nm1 > s:
        return True
    if a_nm1 >= s:
        f1 = f.eval(1)
        f2 = f.eval(-1)
        if f1 != 0 and f2 != 0:
            return True
    return False
