from meta import Meta
import image
import os

class Analysis:
    def __init__(self, name):
        self.meta_ = Meta(name)

    def valid(self):
        return self.meta_.valid()

    def ndvi(self):
        if not hasattr(self, 'ndvi_'):
            orig_raw = image.load(self.meta_.orig_fp())
            orig = image.contrast_stretch(orig_raw)

            ndvi_raw = image.calc_ndvi(orig)
            self.ndvi_ = image.contrast_stretch(ndvi_raw)
        return self.ndvi_

    def blank_rgb_mask(self):
        return image.gray_to_color(self.ndvi())

    def rgb_mask_is_valid(self):
        rgb_mask_fp = self.meta_.rgb_mask_fp()
        if not os.path.exists(rgb_mask_fp):
            return False
        rgb_mask = image.load(rgb_mask_fp)
        return image.is_valid_rgb_mask(rgb_mask)

    def mask_ab(self):
        if not self.rgb_mask_is_valid():
            raise Exception(f"RGB mask {self.meta_.rgb_mask_fp()} is either not present or does not contain any colors")

    def save_ndvi(self):
        image.save(self.meta_.ndvi_color_fp(), image.color_map(self.ndvi()))

    def save_blank_rgb_mask(self):
        image.save(self.meta_.rgb_mask_fp(), self.blank_rgb_mask())

    def compute_stats(self, image):
        raw_values = [value for line in image for value in line]
        # Remap greyscale value [0, 255] to [-1.0, 1.0]
        values = [2*v/255-1 for v in raw_values]
        values = [x for x in values if x>=0]
        avg = sum(values) / len(values)
        var = sum([(v - avg) * (v - avg) for v in values]) / len(values)
        std = math.sqrt(var)
        return avg, std

import unittest

class TestAnalysis(unittest.TestCase):
    def test_scenario(self):
        name = 'foto_plant_wittemuur'

        a = Analysis(name)
        self.assertTrue(a.valid())

        a.save_ndvi()

        if not a.rgb_mask_is_valid():
            print("Creating RGB mask")
            a.save_blank_rgb_mask()

if __name__ == '__main__':
    unittest.main()
