#!/usr/bin/python3
"""TVS face detection method"""
import cv2


def face_detection_method(image_data, image_details, method_parameters):
    """Face detection method via OpenCV"""
    detect_eyes = method_parameters["detect_eyes"]
    face_cascade, eye_cascade = _get_cascades(method_parameters, detect_eyes)
    scale_factor = 1.3
    min_neighbors = 5

    faces = face_cascade.detectMultiScale(image_data, scale_factor, min_neighbors)

    if detect_eyes:
        result = []
        for face in faces:
            x, y, width, height = face
            face_area = image_data[y:y + height, x:x + width]
            eyes = eye_cascade.detectMultiScale(face_area)
            result.append((face, eyes))
        return image_data, result
    else:
        return image_data, ((face, None) for face in faces)


def _get_cascades(method_parameters, is_detect_eyes):
    face_cascade_path = method_parameters["face_cascade_path"]
    face_detection_cascade = cv2.CascadeClassifier(face_cascade_path)
    eye_detection_cascade = None

    if is_detect_eyes:
        eye_cascade_path = method_parameters["eye_cascade_path"]
        eye_detection_cascade = cv2.CascadeClassifier(eye_cascade_path)

    return (face_detection_cascade, eye_detection_cascade)
