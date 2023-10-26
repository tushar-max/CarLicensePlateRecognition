# import pytesseract

# path = 'C:\Users\\tusharawasthi\AppData\Local\Programs\Tesseract-OCR\\tesseract.exe'
import os
import cv2
import pytesseract
import numpy as np
from matplotlib import pyplot as plt

def visualize(**images):
    """PLot images in one row."""
    n = len(images)
    plt.figure(figsize=(16, 5))
    for i, (name, image) in enumerate(images.items()):
        plt.subplot(1, n, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.title(' '.join(name.split('_')).title())
        plt.imshow(image, cmap="gray")
    plt.show()

def preprocess_license_plate(plate_img, is_visualize_steps = False):
    # Extrat the value channel from the HSV format
    V = cv2.split(cv2.cvtColor(plate_img, cv2.COLOR_RGB2HSV))[2]
    
    # Binarize the image by applying adaptive thresholding. 
    threshold_img = cv2.adaptiveThreshold(V, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY,
                                   11, 2)

    if is_visualize_steps:
        visualize(
            hsv_v_image=V,
            threshold_image=threshold_img
        )
    
    return threshold_img

# def preprocess_license_plate(plate_img, is_visualize_steps = False):
#     # Extrat the value channel from the HSV format
#     V = cv2.split(cv2.cvtColor(plate_img, cv2.COLOR_RGB2HSV))[2]
#     imgBlurred = cv2.GaussianBlur(V, (3, 3), 0)
#     # Binarize the image by applying adaptive thresholding. 
#     threshold_img = cv2.adaptiveThreshold(imgBlurred, 255,
#                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                    cv2.THRESH_BINARY,
#                                    11, 2)

#     if is_visualize_steps:
#         visualize(
#             hsv_v_image=V,
#             threshold_image=threshold_img
#         )
    
#     return threshold_img


def get_characters_from_bnw_image(bnw_img):
    txt = pytesseract.image_to_string(bnw_img, config="--psm 4")
    txt = txt.strip().split("\n")[0]
    return txt

