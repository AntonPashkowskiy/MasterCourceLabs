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


def save_filtered_image(filtered_image, directory_name, filter_name=None):
    save_directory_path = os.path.join(OUTPUT_DIRECTORY_PATH, directory_name)
    _create_directory_if_not_exist(save_directory_path)

    unique_id = str(uuid.uuid4())
    output_filename = filter_name + "_" + unique_id if filter_name is not None else unique_id
    save_path = os.path.join(save_directory_path, output_filename + ".jpg")
    cv2.imwrite(save_path, filtered_image)


def _create_directory_if_not_exist(directory_path):
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)


_create_directory_if_not_exist(OUTPUT_DIRECTORY_PATH)
