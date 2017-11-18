#!/usr/bin/python3
"""TVS sample high-level processing"""
from high_level_processing.common import save_to_output_directory


def sample_hl_processing(raw_image, processed_image, image_details, detected_elements_descriptions):
    """Sample of high-level processing function"""
    save_to_output_directory(processed_image)
