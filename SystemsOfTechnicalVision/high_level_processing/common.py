#!/usr/bin/python3
"""TVS common functions for high-level processing"""
import cv2
import os
import uuid


OUTPUT_DIRECTORY_PATH = os.path.join(".", "data", "images", "results")


def save_to_output_directory(image, filename=None):
    output_filename = filename if filename is not None else str(uuid.uuid4())
    save_path = os.path.join(OUTPUT_DIRECTORY_PATH, output_filename + ".jpg")
    cv2.imwrite(save_path, image)