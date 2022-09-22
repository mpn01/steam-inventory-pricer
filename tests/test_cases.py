import unittest
import sys
sys.path.append('..\\')
from module.commands import cases

class TestCases(unittest.TestCase):
    def test_case(self):
        result = list(cases.getCasePrices(all_cases=False, input="riptide"))
        expected_result = "Operation Riptide Case", 45, "tracked"

        self.assertEqual(result[0], expected_result)

