import sympy
from irreduc_types import VAR_X
from irreduc_utils import sub_name
from check_eisenstein import EisensteinCriterion
from check_murty import MurtyCriterion
from check_cohn import CohnCriterion
from check_perron import PerronCriterion
from check_perron import PerronNonSharpCriterion
from check_dumas import DumasCriterion
from check_brauer import BrauerCriterion
from check_osada import OsadaCriterion
from check_polya import PolyaCriterion
from check_schur import SchurCriterion
from check_bonciocat import BonciocatCriterion
from check_galois_fields import GaloisFieldsCriterion
from irreduc_utils import check_common

# TODO: find On the irreducibility of polynomials taking small values by Tverberg H., 1973, should have nice criteria

# TODO: Incorporated check in answer to print that given polynomial cannot be proven irreducible by Eisenstein
#  https://math.stackexchange.com/questions/791930/eisenstein-criterion-shift-conditions?noredirect=1&lq=1


if __name__ == '__main__':
    import sys
    from irreduc_utils import create_polynomial

    input = sys.argv[1]

    poly = create_polynomial(input)
    polys = list()

    # generate list of polynomials (including substitutions) to check on
    polys.append((poly, 1, 0, False))
    for a in (-1, 1,):  # we need to substitute only units... which in Z are just -1, +1
        for b in range(-30, 30 + 1):
            if a == 0 or (a == 1 and b == 0):
                continue

            subpoly = poly.subs(VAR_X, a * VAR_X + b).simplify()
            polys.append((subpoly, a, b, False))

            if subpoly.TC() != 0:
                subpoly_reverted = sympy.Poly(reversed(subpoly.all_coeffs()), VAR_X)
                polys.append((subpoly_reverted, a, b, True))

    criteria = [
        EisensteinCriterion(),
        CohnCriterion(),
        PerronCriterion(),
        PerronNonSharpCriterion(),
        DumasCriterion(),
        MurtyCriterion(),
        BrauerCriterion(),
        OsadaCriterion(),
        PolyaCriterion(),
        SchurCriterion(),
        BonciocatCriterion(),
        GaloisFieldsCriterion(),
    ]

    for criterion in criteria:
        for poly in polys:
            check_common(poly[0], sub_name(poly[1], poly[2], poly[3]), criterion)
            if isinstance(criterion, GaloisFieldsCriterion):  # dirty hack
                break
        print('')

