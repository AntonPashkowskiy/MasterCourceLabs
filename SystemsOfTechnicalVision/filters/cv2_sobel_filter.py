#!/usr/bin/python3
"""Filter from gray image to gray image with extracted borders"""
import cv2


def cv2_sobel_filter(gray_image, filter_parameters):
    """Sobel filter via OpenCV"""
    key = "extract_gradient"
    default_mode = "vertical"
    extract_gradient_mode = filter_parameters[key] if key in filter_parameters else default_mode

    if _is_invalid_mode(extract_gradient_mode):
        raise ValueError("Unsopported extract gradient mode")

    gradient_x = cv2.Sobel(gray_image, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradient_y = cv2.Sobel(gray_image, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

    if extract_gradient_mode == "vertical":
        gradient = cv2.subtract(gradient_x, gradient_y)
    else:
        gradient = cv2.subtract(gradient_y, gradient_x)
    return cv2.convertScaleAbs(gradient)


def _is_invalid_mode(extract_gradient_mode):
    return extract_gradient_mode is not None and extract_gradient_mode not in ["vertical", "horizontal"]
