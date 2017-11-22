#!/usr/bin/python3
"""TVS smile detection method"""
import cv2


def smile_detection_method(image_data, image_details, method_parameters):
    """Smile detection method via OpenCV"""
    if "smile_cascade_path" not in method_parameters:
        raise ValueError("Smile cascade path not defined for the smile detection method.")

    smile_cascade_path = method_parameters["smile_cascade_path"]
    smile_cascade = cv2.CascadeClassifier(smile_cascade_path)
    scale_factor = 1.3
    min_neighbors = 5
    smiles = smile_cascade.detectMultiScale(image_data, scale_factor, min_neighbors)
    return image_data, smiles
