#!/usr/bin/python3
"""Filter from hsv image to black-white image by color thesholds"""
import cv2
import numpy as np


def cv2_hsv_color_range_filter(hvs_image, filter_parameters):
    """HVS color range filter"""
    if "lower_color" not in filter_parameters or "upper_color" not in filter_parameters:
        raise ValueError("Color range was not specified for HVS color range filter.")

    lower_threshold = filter_parameters["lower_color"]
    upper_threshold = filter_parameters["upper_color"]

    lower_color = _get_color_from_parameter(lower_threshold)
    upper_color = _get_color_from_parameter(upper_threshold)

    print(lower_color)
    print(upper_color)

    return cv2.inRange(hvs_image, lower_color, upper_color)


# color_parameter_string = "255,255,255"
def _get_color_from_parameter(color_parameter_string):
    colour_list_string = color_parameter_string.split(',')  # ["255", "255", "255"]
    colour_list = list(map(int, colour_list_string))

    return np.array(colour_list)
