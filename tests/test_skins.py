import unittest
import sys
sys.path.append('..\\') # Windows path for module folder
from module.commands import skins

class TestSkins(unittest.TestCase):
    def test_skin(self):
        user_input = "m4a1"
        sql_query = f"SELECT * FROM skins WHERE name LIKE '%{user_input}%';"
        result = list(skins.getSkins(all_skins=False, query=sql_query))
        expected_result = "M4A1-S | Bright Water (Minimal Wear)", "tracked", 151.84, "arrMY"

        self.assertEqual(result[0], expected_result)