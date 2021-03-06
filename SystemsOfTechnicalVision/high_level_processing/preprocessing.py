#!/usr/bin/python3
"""TVS high-level preprocessing"""
import os
from shutil import rmtree


def clean_output_directory():
    """Clean directory before new images processing"""
    directory_path = os.path.join(".", "data", "images", "results")
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if os.path.isfile(filepath):
            os.remove(filepath)
        else:
            rmtree(filepath)
