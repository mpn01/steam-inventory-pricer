import unittest
import sys
sys.path.append('..\\')
from module.commands import skins

class TestSkins(unittest.TestCase):
    def test_skin(self):
        result = list(skins.getSkinPrices(all_skins=False, input="m4a1"))
        expected_result = "M4A1-S | Bright Water (Minimal Wear)", "tracked", 151.84, "arrMY"

        self.assertEqual(result[0], expected_result)

    # def test_skins(self):
    #     result = list(skins.getSkinPrices(all_skins=False, input=None))
    #     expected_result = "M4A1-S | Bright Water (Minimal Wear)", "tracked", 151.84, "arrMY"

    #     self.assertEqual(result[0], expected_result)