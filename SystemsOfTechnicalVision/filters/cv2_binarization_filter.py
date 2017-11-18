#!/usr/bin/python3
"""Filter from gray image to black and white image"""
import cv2


def cv2_binarization_filter(image, filter_parameters):
    """RGB to gray filter"""
    retval, binarized_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    return binarized_image
