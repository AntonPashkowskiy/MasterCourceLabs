#!/usr/bin/python3
"""Describes mappings from filter or methods names to Python functions"""
from filters.sample_filter import sample_filter
from filters.cv2_gray_filter import cv2_gray_filter
from filters.cv2_binarization_filter import cv2_binarization_filter
from details_extraction.sample_details_extraction import sample_details_extraction
from detection.sample_detection_method import sample_detection_method
from detection.face_detection_method import face_detection_method
from detection.plate_number_detection_method import plate_number_detection_method


FILTER_MAPPING = {
    "test_filter_1": sample_filter,
    "test_filter_2": sample_filter,
    "cv2_gray_filter": cv2_gray_filter,
    "cv2_binarization_filter": cv2_binarization_filter
}


DETAILS_EXTRACTION_METHODS = {
    "detail_extraction_test_method": sample_details_extraction
}


DETECTION_METHODS = {
    "detection_test_method": sample_detection_method,
    "face_detection_method": face_detection_method,
    "plate_number_detection_method": plate_number_detection_method
}
