#!/usr/bin/python3
"""TVS barcodes detection high-level processing"""
import cv2
from high_level_processing.common import save_to_output_directory


def barcodes_hl_processing(raw_image, processed_image, image_details, detection_results):
    """High-level function for barcodes processing"""
    _, barcode_box = image_details[0]
    cv2.drawContours(raw_image, [barcode_box], -1, (0, 255, 0), 3)
    save_to_output_directory(raw_image)
