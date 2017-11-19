#!/usr/bin/python3
"""Filter which deletes space between white objects on image"""
import cv2


def cv2_morphology_close_filter(image, filter_parameters):
    """Morphology close filter via OpenCV"""
    if "kernel_rectangle_width" not in filter_parameters or "kernel_rectangle_height" not in filter_parameters:
        raise ValueError("Kernel rectange parameters for morphlogy close filter were not specified")
    rectangle_width = filter_parameters["kernel_rectangle_width"]
    rectangle_height = filter_parameters["kernel_rectangle_height"]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (rectangle_width, rectangle_height))
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
