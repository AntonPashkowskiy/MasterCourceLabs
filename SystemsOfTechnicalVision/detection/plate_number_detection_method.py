#!/usr/bin/python3
"""TVS russian plate number detection method"""
import cv2


def plate_number_detection_method(image_data, image_details, method_parameters):
    """Russian plate numbers detection method via OpenCV"""
    plates_cascade_path = method_parameters["plate_cascade_path"]
    plate_cascade = cv2.CascadeClassifier(plates_cascade_path)
    scale_factor = 1.3
    min_neighbors = 5
    plates = plate_cascade.detectMultiScale(image_data, scale_factor, min_neighbors)
    return image_data, plates
