#!/usr/bin/python3
"""TVS high-level processing"""
import cv2
import os
import uuid


def sample_hl_processing(raw_image, processed_image, image_details, detected_elements_descriptions):
    """Sample of high-level processing function"""
    unique_filename = str(uuid.uuid4())
    directory_path = os.path.join(".", "images", "results")
    save_path = os.path.join(directory_path, unique_filename + ".jpg")
    cv2.imwrite(save_path, processed_image)
