import unittest
import sys
sys.path.append('../module')
from module.commands import skins

class testSkinsFunctions(unittest.TestCase):
    skins.getSkinPrices(all_skins=True, input=None)
    skins.getSkinPrices(all_skins=False, input="m4a4")

if __name__ == '__main__':
    unittest.main()