import sys
from irreducibility_common import create_polynomial
from irreducibility_common import poly_non_zero_exps
from irreducibility_common import get_coeff
from irreducibility_common import VAR_X
from irreducibility_common import CheckResult
from irreducibility_common import ResultEnum
from irreducibility_common import check_common


class PerronCriterion:
    def __init__(self):
        self.name = "Perron's irreducibility criterion"

    def name(self):
        return self.name

    def check(self, f):
        const_coeff = f.TC()
        if const_coeff == 0:
            return CheckResult(ResultEnum.REDUCIBLE)
        lead_coeff = f.LC()
        if lead_coeff != 1:
            return CheckResult(ResultEnum.UNKNOWN)
        a_nm1 = abs(get_coeff(f, f.degree() - 1))
        s = 1
        for exp, coeff in poly_non_zero_exps(f):
            if exp < f.degree() - 1:
                s += abs(coeff)
        if a_nm1 > s:
            return CheckResult(ResultEnum.IRREDUCIBLE)
        return CheckResult(ResultEnum.UNKNOWN)


class PerronNonSharpCriterion:
    def __init__(self):
        self.name = "Perron's (non-sharp) irreducibility criterion"

    def name(self):
        return self.name

    def check(self, f):
        const_coeff = f.TC()
        if const_coeff == 0:
            return CheckResult(ResultEnum.REDUCIBLE)
        lead_coeff = f.LC()
        if lead_coeff != 1:
            return CheckResult(ResultEnum.UNKNOWN)
        a_nm1 = abs(get_coeff(f, f.degree() - 1))
        s = 1
        for exp, coeff in poly_non_zero_exps(f):
            if exp < f.degree() - 1:
                s += abs(coeff)
        if a_nm1 > s:
            return CheckResult(ResultEnum.IRREDUCIBLE)
        if a_nm1 >= s:
            f1 = f.subs(VAR_X, 1)
            f2 = f.subs(VAR_X,-1)
            if f1 != 0 and f2 != 0:
                return CheckResult(ResultEnum.IRREDUCIBLE)
        return CheckResult(ResultEnum.UNKNOWN)


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], PerronCriterion())
    check_common(poly, sys.argv[1], PerronNonSharpCriterion())
