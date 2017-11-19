#!/usr/bin/python3
"""Filter which deletes small white blobes from an image"""
import cv2


def cv2_erode_filter(black_white_image, filter_parameters):
    """Erode filter via OpenCV"""
    if "iterations_count" not in filter_parameters:
        raise ValueError("Iterations count not specified for erode filter")
    iterations_count = filter_parameters["iterations_count"]
    return cv2.erode(black_white_image, None, iterations=iterations_count)
