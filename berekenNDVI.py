import cv2
import numpy as np
import os
import math
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
    ndvi = (r.astype(float) - b) / bottom
    return ndvi

def compute_stats(image):
    raw_values = [value for line in image for value in line]
    # Remap greyscale value [0, 255] to [-1.0, 1.0]
    values = [2*v/255-1 for v in raw_values]
<<<<<<< HEAD
    values = [x for x in values if 1 >= x >= 0]
    avg = sum(values) / len(values)
    var = sum([(x - avg) * (x - avg) for x in values]) / len(values)
    std = math.sqrt(var)
=======
    values = [x for x in values if x>=0]
    avg, std = 0.0, 0.0
    if values:
        avg = sum(values) / len(values)
        var = sum([(v - avg) * (v - avg) for v in values]) / len(values)
        std = math.sqrt(var)
>>>>>>> 93b9d5a3ebf8a4975068b9af944aa79365ded8f4
    return avg, std

orig_fns = os.listdir('original')
orig_fns.sort()

if not os.path.exists('ndvi'):
    os.mkdir('ndvi')

with open('data.csv', 'w') as data_file:
    data_file.write('foto\tavg\tstd\n')
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

        avg, std = compute_stats(ndvi)
        data_file.write(f"{orig_fn}\t{avg}\t{std}\n")

