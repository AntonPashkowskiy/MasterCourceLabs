#!/usr/bin/python3
"""TVS white area size in pixels"""
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
import numpy as np


WHITE_PIXEL_VALUE = 255


def white_area_size(black_white_image, method_parameters):
    """Method which calculates white pixels area on images"""
    scale = method_parameters["scale"] if "scale" in method_parameters else 1

    if scale <= 0:
        raise ValueError("Scale in white area size method should be positive")

    cpu_count = multiprocessing.cpu_count()
    with ThreadPool(cpu_count) as pool:
        result = pool.map(_count_white_pixels, black_white_image)
        return sum(result) / scale


def _count_white_pixels(line):
    return np.count_nonzero(line == WHITE_PIXEL_VALUE)
