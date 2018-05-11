import sympy
from irreducibility_common import VAR_X
from irreducibility_common import sub_name
from check_eisenstein import check_eisenstein
from check_murty import check_murty
from check_cohn import check_cohn
from check_perron import check_perron
from check_perron import check_perron_non_sharp
from check_dumas import check_dumas
from check_brauer import check_brauer
from check_osada import check_osada
from check_polya import check_polya
from check_schur import check_schur
from check_bonciocat import check_bonciocat
from check_galois_fields import check_galois_fields


# TODO: find On the irreducibility of polynomials taking small values by Tverberg H., 1973, should have nice criteria

# TODO: Incorporated check in answer to print that given polynomial cannot be proven irreducible by Eisenstein
#  https://math.stackexchange.com/questions/791930/eisenstein-criterion-shift-conditions?noredirect=1&lq=1


if __name__ == '__main__':
    import sys
    from irreducibility_common import create_polynomial

    input = sys.argv[1]

    poly = create_polynomial(input)
    polys = list()

    # generate list of polynomials (including substitutions) to check on
    polys.append((poly, 1, 0, False))
    for a in (-1, 1,):  # we need to substitute only units... which in Z are just -1, +1
        if a == 0:
            continue
        if a==1 and b==0:
            continue
        for b in range(-30, 30 + 1):
            subpoly = poly.subs(VAR_X, a * VAR_X + b).simplify()

            polys.append((subpoly, a, b, False))
            # irreducibility is conserved only when there is non zero constant coeff

            if subpoly.TC() != 0:
                subpoly_reverted = sympy.Poly(reversed(subpoly.all_coeffs()), VAR_X)
                polys.append((subpoly_reverted, a, b, True))

    max_p = 1000000000

    print('Checking by Eisenstein criteria:')
    found = False
    for poly in polys:
        p = check_eisenstein(poly[0])
        if p is not None and p <= max_p:
            print('Polynomial %s is Eisenstein by p=%i' % (sub_name(poly[1], poly[2], poly[3]), p))
            found = True
    if not found:
        print('NONE')
    print('')

    print('Checking by Cohn\'s criteria:')
    found = False
    for poly in polys:
        b, p = check_cohn(poly[0])
        if b is not None and p <= max_p:
            print('Polynomial %s is Cohn irreducible by base b=%i, p=%i' % (sub_name(poly[1], poly[2], poly[3]), b, p))
            found = True
    if not found:
        print('NONE')
    print('')

    print('Checking by Perron\'s criteria:')
    found = False
    for poly in polys:
        is_perron = check_perron(poly[0])
        if is_perron:
            print('Polynomial %s is irreducible by Perron\'s criterion' % (sub_name(poly[1], poly[2], poly[3])))
            found = True
    if not found:
        print('NONE')
    print('')

    print('Checking by Perron\'s criteria (non sharp inequality):')
    found = False
    for poly in polys:
        is_perron = check_perron_non_sharp(poly[0])
        if is_perron:
            print('Polynomial %s is irreducible by Perron\'s criterion'
                  % (sub_name(poly[1], poly[2], poly[3])))
            found = True
    if not found:
        print('NONE')
    print('')

    print('Checking by Dumas theorem:')
    found = False
    for poly in polys:
        plist = check_dumas(poly[0])
        if plist is not None:
            print('Polynomial %s is irreducible by Dumas theorem for p=%s'
                  % (sub_name(poly[1], poly[2], poly[3]), str(plist)))
            found = True
    if not found:
        print('NONE')
    print('')

    print('Checking by Murty\'s:')
    found = False
    for poly in polys:
        n, p = check_murty(poly[0])
        if n is not None and p <= max_p:
            print('Polynomial %s is irreducible by Murty for n=%i, p=%i'
                  % (sub_name(poly[1], poly[2], poly[3]), n, p))
            found = True
    if not found:
        print('NONE')
    print('')

    print('Checking by Brauer\'s:')
    found = False
    for poly in polys:
        b = check_brauer(poly[0])
        if b:
            print('Polynomial %s is irreducible by Brauer'
                  % (sub_name(poly[1], poly[2], poly[3])))
            found = True
    if not found:
        print('NONE')
    print('')

    print('Checking by Osada\'s:')
    found = False
    for poly in polys:
        b, p = check_osada(poly[0])
        if b:
            print('Polynomial %s is irreducible by Osada [p=%i]'
                  % (sub_name(poly[1], poly[2], poly[3]), p))
            found = True
    if not found:
        print('NONE')
    print('')

    print('Checking by Polya\'s:')
    found = False
    for poly in polys:
        siutable = check_polya(poly[0])
        if siutable:
            print('Polynomial %s is irreducible by Poyla for a\'s in %s'
                  % (sub_name(poly[1], poly[2], poly[3]), str(siutable)))
            found = True
    if not found:
        print('NONE')
    print('')

    print('Checking by Schur\'s:')
    found = False
    for poly in polys:
        b = check_schur(poly[0])
        if b:
            print('Polynomial %s is irreducible by Schur.'
                  % (sub_name(poly[1], poly[2], poly[3])))
            found = True
    if not found:
        print('NONE')
    print('')

    print('Checking by Bonciocat\'s:')
    found = False
    for poly in polys:
        b, S = check_bonciocat(poly[0])
        if b:
            print('Polynomial %s is irreducible by Bonciocat. (Sps=%s)'
                  % (sub_name(poly[1], poly[2], poly[3]), str(S)))
            found = True
    if not found:
        print('NONE')
    print('')

    print('Checking Galois Fields:')
    found = False
    for poly in polys:
        b, p = check_galois_fields(poly[0])
        if b:
            print('Polynomial %s is irreducible in Galois (finite) field. (p=%s)'
                  % (sub_name(poly[1], poly[2], poly[3]), str(p)))
            found = True
        break  # END after first one, others are irrelevant
    if not found:
        print('NONE')
    print('')
