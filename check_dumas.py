import sympy
from irreducibility_common import poly_non_zero_exps


def check_dumas(f, force_prime=None):
    # try for prime divisors of constant term (might add leading term later too)
    const_coeff = abs(f.TC())
    if const_coeff == 0:
        return None

    if force_prime is not None:
        if const_coeff % force_prime != 0:
            return None
        primes = [force_prime]
    else:
        primes = sympy.ntheory.factorint(const_coeff)

    satisfies = []
    for p in primes:
        # calculate points for given prime p for all coeffs
        points = []
        for exp, coeff in poly_non_zero_exps(f):
            if coeff != 0:
                coeff_factors = sympy.ntheory.factorint(coeff)
                padic = coeff_factors[p] if p in coeff_factors else 0
                points.append((exp, padic))

        # if this can be of any use, length of line between end points must not cross any integers
        first = points[0]
        last = points[-1]
        x_diff = abs(first[0] - last[0])
        y_diff = abs(first[1] - last[1])
        if sympy.gcd(x_diff, y_diff) != 1:
            continue

        # now just check if all the other points are above this line
        x1 = first[0]
        y1 = first[1]
        x2 = last[0]
        y2 = last[1]

        above = True
        for i in range(1, len(points) - 1):
            x, y = points[i]
            if (y - y1) * (x2 - x1) <= (x - x1) * (y2 - y1):
                above = False
                break
        if not above:
            continue

        satisfies.append(p)
    if satisfies:
        return satisfies
    return None