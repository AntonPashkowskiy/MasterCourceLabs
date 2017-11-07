#!/usr/bin/python3
"""Provides generator of images from source paths"""
import cv2
import os


class ImageSource:
    """Image sources class"""
    def __init__(self, paths):
        if paths is None or len(paths) == 0:
            raise ValueError("Path list is empty")
        self._paths = paths

    def images(self):
        """Reads images from paths"""
        for path in self._paths:
            if os.path.isdir(path):
                for image in self._images_from_dir(path):
                    yield image
            else:
                image = cv2.imread(path)
                if image is not None:
                    yield image

    def _images_from_dir(self, dir_path):
        for filename in os.listdir(dir_path):
            image = cv2.imread(os.path.join(dir_path, filename))
            if image is not None:
                yield image
