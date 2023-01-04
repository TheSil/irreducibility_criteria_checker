import sympy
import sys

from irreduc_utils import create_polynomial, poly_non_zero_exps, check_common
from irreduc_types import VAR_X, IRREDUCIBLE, REDUCIBLE, UNKNOWN


class FilasetaDegree31Criterion:
    def __init__(self):
        self.name = "Filaseta's irreducibility criterion for degree <= 31"

    def name(self):
        return self.name

    def check(self, f):
        # https://doi.org/10.1016/j.jnt.2013.11.001
        # If the polynomial has non-negative coefficients, deg f <= 31 and f(10) is a prime
        # then f is irreducible

        # first we need to ensure coefficients are non-negative
        max_coeff = 0
        for _, coeff in poly_non_zero_exps(f):
            if coeff < 0:
                return UNKNOWN, None

        # f(10) must be prime
        val = f.subs(VAR_X, 10)
        if not sympy.isprime(val):
            return UNKNOWN, None

        # deg f <= 31
        if f.degree() > 31:
            return UNKNOWN, None

        return IRREDUCIBLE, {"p": val}


class FilasetaBoundedCoeffsCriterion:
    def __init__(self):
        self.name = "Filaseta's irreducibility criterion for bounded coefficients"

    def name(self):
        return self.name

    def check(self, f):
        # https://doi.org/10.1016/j.jnt.2013.11.001
        # https://oeis.org/A253280
        # If the polynomial has non-negative coefficients which are at most A253280(n)
        # and f(n) is a prime, then f is irreducible
        A253280 = {
            3: 3795,
            4: 8925840,
            5: 56446139763,
            6: 568059199631352,
            7: 4114789794835622912,
            8: 75005556404194608192050,
            9: 1744054672674891153663590400,
            10: 49598666989151226098104244512918,
            11: 1754638089240473418053140582402752512,
            12: 77040233750234318697380885880167588145722,
            13: 28717077224929268201659599157515978503356415,
            14: 274327682731486702351640132483696971555362645663790,
            15: 53237820409607236753887375170676537338756637987992240128,
            16: 8267439025097901738248191414518610393726802935783728327213632,
            17: 1268514052720791756582944613802085175096200858994963359873275789312,
            18: 210075378544004872190325829606836051632192371202216081668284609637499040,
            19: 38625368655808052927694359301620272576822252200247254369696128549408630374400,
            20: 7965097815841643900684276577174036821605756035173863133380627982979718588470528880}

        # first we need to ensure coefficients are within bounds
        max_coeff = 0
        for _, coeff in poly_non_zero_exps(f):
            if coeff < 0 or coeff > 49598666989151226098104244512918:
                return UNKNOWN, None

        # for given bases check if the result is prime and if is within specified bounds
        # report the smallest affirmative case if found
        for b, B in A253280.items():
            val = f.subs(VAR_X, b)
            if sympy.isprime(val):
                is_bounded = True
                for _, coeff in poly_non_zero_exps(f):
                    if coeff < 0 or coeff > B:
                        is_bounded = False
                        break
                if is_bounded:
                    return IRREDUCIBLE, {"base": b, "p": val, "B": B}

        return UNKNOWN, None


if __name__ == '__main__':
    poly = create_polynomial(sys.argv[1])
    check_common(poly, sys.argv[1], FilasetaDegree31Criterion())
    check_common(poly, sys.argv[1], FilasetaBoundedCoeffsCriterion())
