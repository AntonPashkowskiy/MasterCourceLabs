#!/usr/bin/python3
"""Filter from gray image to black and white image"""
import cv2


def cv2_binarization_filter(gray_image, filter_parameters):
    """RGB to gray filter"""
    if "lower_threshold" not in filter_parameters or "upper_threshold" not in filter_parameters:
        raise ValueError("Thresholds was not specified for binarization filters.")

    lower_threshold = filter_parameters["lower_threshold"]
    upper_threshold = filter_parameters["upper_threshold"]

    if _is_invalid_threshold(lower_threshold, upper_threshold):
        raise ValueError("Binarization thresholds error")

    retval, binarized_image = cv2.threshold(gray_image, lower_threshold, upper_threshold, cv2.THRESH_BINARY)
    return binarized_image


def _is_invalid_threshold(lower, upper):
    return lower > upper or (upper < 0 or upper > 255) or (lower < 0 or lower > 255)
