#!/usr/bin/python3
"""System of technical vision class defenition"""
import multiprocessing
import uuid
from multiprocessing.dummy import Pool as ThreadPool
from high_level_processing.common import save_filtered_image
from sources.image_source import ImageSource
from tvs_mappers import FILTER_MAPPING,\
    DETAILS_EXTRACTION_METHODS,\
    DETECTION_METHODS


class TechnicalVisionSystem:
    """TVS class"""
    def __init__(self):
        self._is_parallel_processing = False
        self._is_intermediate_results_saves = False
        self._sources = []
        self._filters = []
        self._detail_extraction_methods = []
        self._detection_methods = []
        self._result_processing_function = lambda image, image_data: image
        self._preprocessing_function = None

    @property
    def is_parrallel_processing(self):
        """Determines way of sources processing (parallel or sequential)"""
        return self._is_parallel_processing

    @is_parrallel_processing.setter
    def is_parrallel_processing(self, value):
        self._is_parallel_processing = value

    @property
    def is_intermediate_results_saves(self):
        """Determines that images saves on all processing steps"""
        return self._is_intermediate_results_saves

    @is_intermediate_results_saves.setter
    def is_intermediate_results_saves(self, value):
        self._is_intermediate_results_saves = value

    def add_sources(self, sources):
        """Add an image sources to system"""
        if sources is not None:
            self._sources.extend(sources)
        else:
            raise ValueError("Sources are not exist")

    def add_filters(self, filters):
        """Add a image filters to system (filter_name, parameters)"""
        if filters is not None:
            self._filters.extend(filters)
        else:
            raise ValueError("Filters are incorrect")

    def add_details_extraction_methods(self, methods):
        """Add a image details extraction methods to system (method_name, parameters)"""
        if methods is not None:
            self._detail_extraction_methods.extend(methods)
        else:
            raise ValueError("Detail extraction methods are incorrect")

    def add_detection_methods(self, methods):
        """Add detection or segmentation methods to system (method_name)"""
        if methods is not None:
            self._detection_methods.extend(methods)
        else:
            raise ValueError("Detection or segmentation methods are incerrect")

    def add_result_processing_function(self, result_processing_function):
        """Add high level processing function to system (callable)"""
        if result_processing_function is not None:
            self._result_processing_function = result_processing_function
        else:
            raise ValueError("High level result processing function is incorrect")

    def add_preprocessing_function(self, preprocessing_function):
        """Add high level function calls before image processing"""
        if preprocessing_function is not None:
            self._preprocessing_function = preprocessing_function

    def start_processing(self):
        """Calls when vision system object is ready for processing"""
        image_source = ImageSource(self._sources)

        if self._preprocessing_function is not None:
            self._preprocessing_function()

        if self._is_parallel_processing:
            cpu_count = multiprocessing.cpu_count()
            with ThreadPool(cpu_count) as pool:
                pool.map(self._process_raw_image, image_source.images())
        else:
            for raw_image in image_source.images():
                self._process_raw_image(raw_image)

    def _process_raw_image(self, raw_image):
        processed_image = self._apply_all_filters(raw_image)
        processed_image, image_details = self._extract_all_details(processed_image)
        processed_image, detected_elements_descriptions =\
            self._apply_all_detection_methods(processed_image, image_details)
        self._result_processing_function(
            raw_image, processed_image, image_details, detected_elements_descriptions)

    def _apply_all_filters(self, image):
        filtered_image = image.copy()
        unique_directory_name = str(uuid.uuid4())

        for filter_object in self._filters:
            filter_name = filter_object["filter_name"]
            filter_function = FILTER_MAPPING[filter_name]
            filtered_image = filter_function(filtered_image, filter_object["filter_parameters"])

            if self._is_intermediate_results_saves:
                save_filtered_image(filtered_image, unique_directory_name, filter_name)

        return filtered_image

    def _extract_all_details(self, image):
        details_container = []
        for details_extraction_method in self._detail_extraction_methods:
            de_method_name = details_extraction_method["name"]
            de_method_parameters = details_extraction_method["parameters"]
            de_method = DETAILS_EXTRACTION_METHODS[de_method_name]
            details = de_method(image, de_method_parameters)
            details_container.append((de_method_name, details))
        return image, details_container

    def _apply_all_detection_methods(self, image, image_details):
        detected_elements_descriptions = []
        for detection_method_description in self._detection_methods:
            dos_method_name = detection_method_description["name"]
            dos_method_parameters = detection_method_description["parameters"]
            dos_method = DETECTION_METHODS[dos_method_name]
            image, description = dos_method(image, image_details, dos_method_parameters)
            detected_elements_descriptions.append((dos_method_name, description))
        return image, detected_elements_descriptions
