#!/usr/bin/python3
"""Filter from rgb image to hsv image"""
import cv2


def cv2_hsv_filter(image, filter_parameters):
    """RGB to hsv filter"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
