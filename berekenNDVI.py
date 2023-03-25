import cv2
import numpy as np
import os
from fastiecm import fastiecm

def contrast_stretch(image):
    in_min = np.percentile(image, 5)
    in_max = np.percentile(image, 95)

    out_min, out_max = 0.0, 255.0

    out = image - in_min
    out *= ((out_min - out_max)/(in_min-in_max))
    out += in_min

    return out

def calc_ndvi(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float)+b.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (b.astype(float) - r) / bottom
    return ndvi
    
orig_fns = os.listdir('original')

for orig_fn in orig_fns:
    orig_fp = f"original/{orig_fn}"
    ndvi_bw_fp = f"ndvi/bw_{orig_fn}"
    ndvi_color_fp = f"ndvi/color_{orig_fn}"

    print(f"Processing {orig_fp} into {ndvi_bw_fp} and {ndvi_color_fp}")

    original = cv2.imread(orig_fp)
    contrasted = contrast_stretch(original)
    ndvi = calc_ndvi(contrasted)
    ndvi_contrasted = contrast_stretch(ndvi)
    cv2.imwrite(ndvi_bw_fp, ndvi_contrasted)
    color_mapped_prep = ndvi_contrasted.astype(np.uint8)
    color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
    cv2.imwrite(ndvi_color_fp, color_mapped_image)

