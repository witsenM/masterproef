import cv2
import numpy as np
from fastiecm import fastiecm

def display(image, name):
    image = np.array(image, dtype=float)/float(255)

    shape = image.shape
    factor = 4
    height = int(shape[0]/factor)
    width = int(shape[1]/factor)

    image = cv2.resize(image, (width, height))

    cv2.namedWindow(name)
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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
    

original = cv2.imread('test.jpg')
display(original, 'Original')

contrasted = contrast_stretch(original)
display(contrasted, 'Contrasted')

ndvi = calc_ndvi(contrasted)
display(ndvi, 'NDVI')
cv2.imwrite('ndvi.png', ndvi)

ndvi_contrasted = contrast_stretch(ndvi)
display(ndvi_contrasted, 'NDVI Contrasted')
cv2.imwrite('ndvi_contrasted.png', ndvi_contrasted)

color_mapped_prep = ndvi_contrasted.astype(np.uint8)
color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
display(color_mapped_image, 'Color mapped')
cv2.imwrite('color_mapped_image.png', color_mapped_image)
