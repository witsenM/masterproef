import cv2
import numpy as np
import os
from fastiecm import fastiecm

def load(fp):
    return cv2.imread(fp)

def save(fp, img):
    dir = os.path.dirname(fp)
    if not os.path.exists(dir):
        os.mkdir(dir)
    cv2.imwrite(fp, img)

def contrast_stretch(img):
    in_min = np.percentile(img, 5)
    in_max = np.percentile(img, 95)

    out_min, out_max = 0.0, 255.0
    out = img - in_min
    out *= ((out_min - out_max)/(in_min-in_max))
    out += in_min

    return out

def calc_ndvi(img):
    b, g, r = cv2.split(img)
    bottom = (r.astype(float)+b.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (r.astype(float) - b) / bottom
    return ndvi

def color_map(img):
    color_mapped_prep = img.astype(np.uint8)
    return cv2.applyColorMap(color_mapped_prep, fastiecm)

def gray_to_color(img):
    if len(img.shape) != 2:
        raise ValueError("Input array must be 2-dimensional")
    
    array_3d = np.repeat(img[:, :, np.newaxis], 3, axis=2)
    return array_3d

def extract_ab_masks(img):
    # Check if the image is 3-dimensional (Height, Width, Channels)
    if len(img.shape) != 3 or img.shape[2] != 3:
        raise ValueError("Input image must be a 3-channel (RGB) image")

    a = (0,0,255) # Red
    b = (0,255,0) # Green

    mask_a = np.all(img == a, axis=2).astype(np.uint8)
    mask_b = np.all(img == b, axis=2).astype(np.uint8)

    return (mask_a, mask_b)

def is_valid_rgb_mask(img):
    (a, b) = extract_ab_masks(img)

    return np.all(a) and np.all(b)
