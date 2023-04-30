import glob
import re
import os

class Meta:
    def find_all():
        r = r'original.(.+)\.jpg'
        names = [re.search(r, fp).group(1) for fp in glob.glob('original/*.jpg')]
        metas = [Meta(name) for name in names]
        metas = [meta for meta in metas if meta.valid()]
        metas.sort(key = lambda m: m.name())
        return metas
        
    def __init__(self, name):
        self.name_ = name

    def valid(self):
        return os.path.exists(self.orig_fp())

    def name(self):
        return self.name_

    def orig_fp(self):
        return f"original/{self.name_}.jpg"

    def ndvi_bw_fp(self):
        return self._ndvi_fp('bw')
    def ndvi_color_fp(self):
        return self._ndvi_fp('color')

    def rgb_mask_fp(self):
        return f"mask/{self.name_}.png"

    # Privates
    def _ndvi_fp(self, what):
        return f"ndvi/{what}_{self.name_}.png"

import unittest

class TestMeta(unittest.TestCase):
    def test_scenario(self):
        name = 'foto_plant_wittemuur'

        m = Meta(name)
        self.assertTrue(m.valid())

        self.assertEqual(f"original/{name}.jpg", m.orig_fp())
        self.assertEqual(f"ndvi/bw_{name}.png", m.ndvi_bw_fp())
        self.assertEqual(f"ndvi/color_{name}.png", m.ndvi_color_fp())
        self.assertEqual(f"mask/{name}.png", m.rgb_mask_fp())

if __name__ == '__main__':
    unittest.main()
