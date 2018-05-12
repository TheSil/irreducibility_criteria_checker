import sympy


VAR_X = sympy.Symbol('x')

IRREDUCIBLE=0
REDUCIBLE=1
UNKNOWN=2

class CheckResult():
    def __init__(self, result, context=None):
        self.result = result
        self.context = context