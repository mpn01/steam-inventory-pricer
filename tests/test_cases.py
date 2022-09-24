import unittest
import sys
sys.path.append('..\\')
from module.commands import cases

class TestCases(unittest.TestCase):
    def test_case(self):
        user_input = "riptide"
        sql_query = f"SELECT * FROM cases WHERE name LIKE '%{user_input}%';"
        result = list(cases.getCases(all_cases=False, query=sql_query))
        expected_result = "Operation Riptide Case", 45, "tracked"

        self.assertEqual(result[0], expected_result)
