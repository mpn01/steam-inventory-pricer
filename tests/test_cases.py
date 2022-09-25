import unittest
import sys
sys.path.append('..\\')
from module.commands import cases

class TestCases(unittest.TestCase):
    def test_case(self):
        self.maxDiff = None
        user_input = "riptide"
        sql_query = f"SELECT * FROM cases WHERE name LIKE '%{user_input}%';"
        result = list(cases.getCases(all_cases=False, query=sql_query))
        expected_result = "Operation Riptide Case", 45, "tracked", "https://steamcommunity.com/market/listings/730/Operation%20Riptide%20Case", 8.82, 396.9, "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFU5narKKW4SvIrhw9PZlaPwNuqAxmgBucNz2L3C8dyj31Xn-0VtMW3wdY6LMlhplna0TPI/360fx360f"

        self.assertEqual(result[0], expected_result)
