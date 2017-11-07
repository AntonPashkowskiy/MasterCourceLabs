#!/usr/bin/python3
"""Filter from rgb image to gray image"""
import cv2


def cv2_gray_filter(image, filter_parameters):
    """RGB to gray filter"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
