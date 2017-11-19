#!/usr/bin/python3
"""TVS image largest contour extraction method"""
import cv2
import numpy as np


def extract_largest_contour(black_white_image, method_parameters):
    """Extract largest contour on an black and white image via OpenCV"""
    _, contours, _ = cv2.findContours(black_white_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    largest_contour_area = cv2.minAreaRect(largest_contour)
    box = np.int0(cv2.boxPoints(largest_contour_area))

    return box
