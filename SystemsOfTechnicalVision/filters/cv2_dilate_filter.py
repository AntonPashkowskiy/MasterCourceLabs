#!/usr/bin/python3
"""Filter which makes the object in white bigger"""
import cv2


def cv2_dilate_filter(black_white_image, filter_parameters):
    """Dilate filter via OpenCV"""
    if "iterations_count" not in filter_parameters:
        raise ValueError("Iterations count not specified for dilate filter")
    iterations_count = filter_parameters["iterations_count"]
    return cv2.dilate(black_white_image, None, iterations=iterations_count)