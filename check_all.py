import sympy
from irreduc_types import VAR_X
from irreduc_utils import sub_name
from criteria.eisenstein import EisensteinCriterion
from criteria.eisenstein_v2 import EisensteinCriterionV2
from criteria.murty import MurtyCriterion
from criteria.cohn import CohnCriterion
from criteria.perron import PerronCriterion
from criteria.perron import PerronNonSharpCriterion
from criteria.dumas import DumasCriterion
from criteria.brauer import BrauerCriterion
from criteria.osada import OsadaCriterion, OsadaCriterionNonSharp
from criteria.polya import PolyaCriterion
from criteria.schur import SchurCriterion
from criteria.bonciocat import BonciocatCriterion
from criteria.galois_fields import GaloisFieldsCriterion
from criteria.complex_roots import ComplexRootsCriterion, ComplexRootsCriterion2, ComplexRootsCriterion3
from criteria.filaseta import FilasetaDegree31Criterion, FilasetaBoundedCoeffsCriterion
from criteria.levit import LevitCriterion
from irreduc_utils import check_common

# TODO: find On the irreducibility of polynomials taking small values by Tverberg H., 1973, should have nice criteria

# TODO: checking if polynomial is attain just enough of (small) primes

if __name__ == '__main__':
    import sys
    from irreduc_utils import create_polynomial

    input = sys.argv[1]

    poly = create_polynomial(input)
    polys = list()
    subs = True

    polys.append((poly, 1, 0, False))

    if subs:
        # generate list of polynomials (including substitutions) to check on
        poly_reverted = sympy.Poly(reversed(poly.all_coeffs()), VAR_X)
        polys.append((poly_reverted, 1, 0, True))
        #for a in (1,):
        for a in (-1, 1,):  # we need to substitute only units... which in Z are just -1, +1
            #for b in range(0,):
            for b in range(-5, 5 + 1):
                if a == 0 or (a == 1 and b == 0):
                    continue

                expr = poly.subs(VAR_X, a * VAR_X + b).simplify().as_expr()
                subpoly = sympy.Poly(expr, VAR_X)

                polys.append((subpoly, a, b, False))

                if subpoly.TC() != 0:
                    subpoly_reverted = sympy.Poly(reversed(subpoly.all_coeffs()), VAR_X)
                    polys.append((subpoly_reverted, a, b, True))

    max_p=1000

    criteria = [
        EisensteinCriterion(),
        EisensteinCriterionV2(),
        CohnCriterion(max_p=max_p),
        PerronCriterion(),
        PerronNonSharpCriterion(),
        DumasCriterion(),
        MurtyCriterion(max_p=max_p),
        BrauerCriterion(),
        OsadaCriterion(max_p=max_p),
        OsadaCriterionNonSharp(max_p=max_p),
        PolyaCriterion(),
        LevitCriterion(),
        SchurCriterion(),
        BonciocatCriterion(),
        GaloisFieldsCriterion(),
        ComplexRootsCriterion2(),
        ComplexRootsCriterion(max_p=max_p),
        ComplexRootsCriterion3(max_p=max_p),
        FilasetaDegree31Criterion(),
        FilasetaBoundedCoeffsCriterion()
    ]

    tryWithSubs = []
    for criterion in criteria:
        poly=polys[0]
        if not check_common(poly[0], sub_name(poly[1], poly[2], poly[3]), criterion):
            tryWithSubs.append(criterion)

    print('')
    print('Trying failed criteria with substitutions')

    if subs:
        for criterion in tryWithSubs:
            # original poly does not satisfy this criterion directly, now try substitutions
            #print("No result for '%s', trying substitutions" % criterion.name)
            for poly in polys:
                check_common(poly[0], sub_name(poly[1], poly[2], poly[3]), criterion)
                if isinstance(criterion, GaloisFieldsCriterion):  # dirty hack
                        break



