#!/usr/bin/python3
"""TVS lumbers vulume calculating high-level processing"""
import cv2
from high_level_processing.common import save_to_output_directory


def lumbers_hl_processing(raw_image, processed_image, image_details, detection_results):
    """High-level function for lumbers volume processing"""
    save_to_output_directory(processed_image)
