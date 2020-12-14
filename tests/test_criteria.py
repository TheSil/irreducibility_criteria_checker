import unittest
from criteria.eisenstein import EisensteinCriterion
from criteria.perron import PerronCriterion, PerronNonSharpCriterion
from irreduc_utils import create_polynomial
from irreduc_types import IRREDUCIBLE, REDUCIBLE, UNKNOWN


class IrreducibilityTests(unittest.TestCase):
    def test_eisenstein(self):
        criterion = EisensteinCriterion()

        result, context = criterion.check(create_polynomial("x^2+2x+2"))
        self.assertEqual(IRREDUCIBLE, result)
        self.assertEqual({"p": 2}, context)

        result, _ = criterion.check(create_polynomial("x^2+2x+1"))
        self.assertNotEqual(IRREDUCIBLE, result)

    def test_perron(self):
        criterion = PerronCriterion()

        result, context = criterion.check(create_polynomial("x^2+3x+1"))
        self.assertEqual(IRREDUCIBLE, result)
        self.assertEqual(None, context)

        result, _ = criterion.check(create_polynomial("x^2+2x+1"))
        self.assertNotEqual(IRREDUCIBLE, result)


if __name__ == '__main__':
    unittest.main()
