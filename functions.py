import cv2
import numpy as np
import argparse
import time
from scipy import ndimage

def gamma_correction(img, gamma=1.0):
    gamma = max(1e-3, gamma)
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(img, table)

def contrast_correction(img, alpha=1.0, beta=0.0):
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def hue_correction(img, hue=0):
    if hue < 0:
        hue = hue + 180
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = hsv_img[:, :, 0], hsv_img[:, :, 1], hsv_img[:, :, 2]
    h = h + hue
    cond = h[:,:] > 180
    h[cond] = h[cond] - 180
    hsv_img[:, :, 0] = h
    return cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)

def rotate_image(img, degree):
    degree = int(degree)
    if degree <= 0:
        return img
    return ndimage.rotate(img, degree)

def mirror_image(img, flip=False):
    if flip:
        return cv2.flip(img, 1)
    return img

def gaussian_filter(img, size=3, sigma=1):
    size, sigma = int(size), int(sigma)
    if size < 3 or sigma < 1:
        return img
    return cv2.filter2D(img, -1, get_gaussian_kernel(size=size, sigma=sigma), borderType=cv2.BORDER_REPLICATE)

def get_gaussian_kernel(size=3, sigma=1):
    x = np.linspace(-(size-1)/2, (size-1)/2, size)**2 / (2 * sigma**2)
    kernel = np.exp(- x[:, None] - x[None, :])
    return kernel / kernel.sum()

if __name__ == "__main__":
    print(np.array([[1,2,3]]))