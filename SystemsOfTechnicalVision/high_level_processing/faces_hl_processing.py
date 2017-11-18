#!/usr/bin/python3
"""TVS faces detection high-level processing"""
import cv2
from high_level_processing.common import save_to_output_directory


def faces_hl_processing(raw_image, processed_image, image_details, detection_results):
    _, detected_faces = detection_results[0]

    for face, eyes in detected_faces:
        x, y, width, height = face
        cv2.rectangle(raw_image, (x, y), (x + width, y + height), (0, 0, 255), 2)

        if eyes is not None:
            face_area = raw_image[y:y + height, x:x + width]
            for eye_x, eye_y, eye_width, eye_height in eyes:
                cv2.rectangle(face_area, (eye_x, eye_y), (eye_x + eye_width, eye_y + eye_height), (255, 255, 255), 2)
    save_to_output_directory(raw_image)
