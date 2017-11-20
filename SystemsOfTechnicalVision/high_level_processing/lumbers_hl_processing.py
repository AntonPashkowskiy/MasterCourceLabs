#!/usr/bin/python3
"""TVS lumbers vulume calculating high-level processing"""
import cv2
import numpy as np
from high_level_processing.common import save_to_output_directory


def lumbers_hl_processing(raw_image, processed_image, image_details, detection_results):
    """High-level function for lumbers volume processing"""
    _, lumbers_area = image_details[0]
    lumbers_length = 20
    lumbers_volume = lumbers_length * lumbers_area
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(raw_image, f"Lumbers volume: {lumbers_volume} m2", (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    save_to_output_directory(raw_image)
