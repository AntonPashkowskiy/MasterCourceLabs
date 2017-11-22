#!/usr/bin/python3
"""TVS smiles detection high-level processing"""
import cv2
from high_level_processing.common import save_to_output_directory


def smiles_hl_processing(raw_image, processed_image, image_details, detection_results):
    """High-level function for smiles processing"""
    _, detected_smiles = detection_results[0]

    for x, y, width, height in detected_smiles:
        cv2.rectangle(raw_image, (x, y), (x + width, y + height), (0, 255, 0), 2)
    save_to_output_directory(raw_image)
