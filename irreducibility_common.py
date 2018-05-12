import sympy
import enum

VAR_X = sympy.Symbol('x')

class ResultEnum(enum.Enum):
    IRREDUCIBLE=0,
    REDUCIBLE=1,
    UNKNOWN=2

class CheckResult():
    def __init__(self, result, context=None):
        self.result = result
        self.context = context

def check_common(f, fname, criterion):
    res = criterion.check(f)
    if res.result == ResultEnum.IRREDUCIBLE:
        print('Polynomial %s is irreducible by %s. (%s)'
              % (fname, criterion.name, res.context))
        return True
    return False


def convex_hull(points):
    """Computes the convex hull of a set of 2D points.

    Input: an iterable sequence of (x, y) pairs representing the points.
    Output: a list of vertices of the convex hull in counter-clockwise order,
      starting from the vertex with the lexicographically smallest coordinates.
    Implements Andrew's monotone chain algorithm. O(n log n) complexity.
    """

    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = sorted(set(points))

    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 1:
        return points

    # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list.
    return lower


def get_all_polygons(f):
    # first let's collect prime factorizations of each of non zero coefficients
    coeff_factor = {}
    for exp, coeff in poly_non_zero_exps(f):
        if coeff != 0:
            coeff_factor[exp] = sympy.ntheory.factorint(abs(coeff))

    # now collect list of distinct primes that appear in the coeffs factorizations
    primes = []
    for exp in coeff_factor:
        for f in coeff_factor[exp]:
            if f not in primes:
                primes.append(f)

    # now construct newton polygons for each prime
    polygons = {}
    for p in primes:
        points = []
        # gather edges first
        for exp in coeff_factor:
            if p in coeff_factor[exp]:
                points.append((exp, coeff_factor[exp][p]))
            else:
                points.append((exp, 0))

        # lower convex hull
        hull = convex_hull(points)
        polygons[p] = hull

    return polygons


def create_polynomial(expr):
    from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
    from sympy.parsing.sympy_parser import parse_expr
    transformations = standard_transformations + (implicit_multiplication_application,)
    expr = expr.replace('^', '**')
    expr = parse_expr(expr, transformations=transformations, evaluate=True)
    return sympy.Poly(expr, VAR_X)


def get_coeff(f, exp):
    return f.all_coeffs()[f.degree() - exp]


def poly_non_zero_exps(f):
    d = f.as_dict()
    for exp in d:
        yield exp[0], d[exp]


def poly_all_exps(f):
    coeffs = list(reversed(f.all_coeffs()))
    for i in range(len(coeffs)):
        yield i, coeffs[i]


def sub_name(a, b, inverted):
    res = "f("
    if abs(a) != 1:
        res += str(a)
    if a == -1:
        res += "-"
    res += "x"
    if b > 0:
        res += "+"
    if b != 0:
        res += str(b)
    res += ")"
    if inverted:
        res += " (inverted)"
    return res


def is_perfect_power(n, p):
    factors = sympy.ntheory.factorint(n)
    for f in factors:
        if (factors[f] % p) != 0:
            return False
    return True
