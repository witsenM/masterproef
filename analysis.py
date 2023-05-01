from meta import Meta
import image
import numpy as np
import os
import math

class Analysis:
    def __init__(self, name):
        self.meta_ = Meta(name)

    def valid(self):
        return self.meta_.valid()

    def orig(self):
        if not hasattr(self, 'orig_'):
            orig_ = image.load(self.meta_.orig_fp())
        return orig_

    def masked_orig(self, mask):
        return self.orig()*np.repeat(mask[:, :, np.newaxis], 3, axis=2)

    def ndvi(self):
        if not hasattr(self, 'ndvi_'):
            orig = self.orig()
            orig_cs = image.contrast_stretch(orig)

            ndvi = image.calc_ndvi(orig_cs)
            self.ndvi_ = image.contrast_stretch(ndvi)
        return self.ndvi_

    def blank_rgb_mask(self):
        return image.to_gray(self.orig())

    def rgb_mask_is_valid(self, count):
        rgb_mask_fp = self.meta_.rgb_mask_fp()
        if not os.path.exists(rgb_mask_fp):
            return False
        rgb_mask = image.load(rgb_mask_fp)
        ms = image.extract_ab_masks(rgb_mask)
        (a, b) = (1 if np.any(m) else 0 for m in  ms)
        return a+b >= count

    def mask_ab(self):
        if not self.rgb_mask_is_valid(2):
            raise Exception(f"RGB mask {self.meta_.rgb_mask_fp()} is either not present or does not contain any colors")
        return image.extract_ab_masks(image.load(self.meta_.rgb_mask_fp()))

    def size_matches_with(self, ab):
        ndvi = self.ndvi()
        print(f"{ndvi.shape} {ab[0].shape} {ab[1].shape}")
        return ab[0].shape == ndvi.shape and ab[1].shape == ndvi.shape

    def save_ndvi(self):
        image.save(self.meta_.ndvi_color_fp(), image.color_map(self.ndvi()))

    def save_blank_rgb_mask(self):
        image.save(self.meta_.rgb_mask_fp(), self.blank_rgb_mask())

    def compute_stats(self, ab):
        img = self.ndvi()

        stats = []
        for m in ab:
            raw_values = [value for line in img*m for value in line]
            # Remap greyscale value [0, 255] to [-1.0, 1.0]
            values = [2*v/255-1 for v in raw_values]
            values = [x for x in values if x>=0]
            avg, std = 0.0, 0.0
            if values:
                avg = sum(values) / len(values)
                var = sum([(v - avg) * (v - avg) for v in values]) / len(values)
                std = math.sqrt(var)
            stats.append((avg, std))
        return stats

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
