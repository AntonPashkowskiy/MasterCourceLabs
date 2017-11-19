#!/usr/bin/python3
"""Filter which applies blur effect to image"""
import cv2


def cv2_blur_filter(image, filter_parameters):
    """Blur filter via OpenCV"""
    if "radius" not in filter_parameters:
        raise ValueError("Radius for blur filter was not specified")

    radius = filter_parameters["radius"]
    return cv2.blur(image, (radius, radius))
