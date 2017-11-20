#!/usr/bin/python3
"""TVS faces detection high-level processing"""
import cv2
from high_level_processing.common import save_to_output_directory


def plates_hl_processing(raw_image, processed_image, image_details, detection_results):
    """High-level function for russian number plates processing"""
    _, detected_plates = detection_results[0]

    for x, y, width, height in detected_plates:
        cv2.rectangle(raw_image, (x, y), (x + width, y + height), (0, 0, 255), 2)
    save_to_output_directory(raw_image)
