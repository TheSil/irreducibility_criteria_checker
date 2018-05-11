import sympy


def check_polya(f):
    # Polynomials by Prasolov, Theorem 2.2.8 (Polya)
    n = f.degree()
    m = (n + 1) // 2
    suitable = []
    rhs = sympy.factorial(m) / (2 ** m)
    for a in range(-20, 20 + 1):
        val = abs(f.eval(a))
        if val == 0:
            # clearly this is reducible...
            return None
        if val < rhs:
            suitable.append(a)
    if len(suitable) >= n:
        return suitable
    return None
