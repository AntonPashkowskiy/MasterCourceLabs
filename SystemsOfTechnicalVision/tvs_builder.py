#!/usr/bin/python3
"""System of technical vision builder"""
from tvs import TechnicalVisionSystem

class TechnicalVisionSystemBuilder:
    """TVS builder class"""
    def __init__(self):
        self._technical_vision_system = TechnicalVisionSystem()

    def in_parallel(self):
        """Enables parallel processing of target vision system"""
        self._technical_vision_system.is_parrallel_processing = True
        return self

    def from_source(self, source):
        """Applies single source to target vision system"""
        self._technical_vision_system.add_sources([source])

    def from_sources(self, sources):
        """Applies image sources to target vision system"""
        self._technical_vision_system.add_sources(sources)
        return self

    def with_filter(self, filter_name):
        """Determines single filter for target vision system"""
        self._technical_vision_system.add_filters([filter_name])

    def with_filters(self, filters):
        """Determines filters chain for target vision system"""
        self._technical_vision_system.add_filters(filters)
        return self

    def with_details_extraction_method(self, method_name):
        """Determines single method for details extraction"""
        self._technical_vision_system.add_details_extraction_methods([method_name])
        return self

    def with_details_extraction_methods(self, methods):
        """Determines methods of image details extraction"""
        self._technical_vision_system.add_details_extraction_methods(methods)
        return self

    def with_detection_method(self, method_name):
        """Determines single method of interest details detection or image segmentation"""
        self._technical_vision_system.add_detection_methods([method_name])
        return self

    def with_detection_methods(self, methods):
        """Determines methods of interest details detection or image segmentation"""
        self._technical_vision_system.add_detection_methods(methods)
        return self

    def result_processed_by(self, result_processing_function):
        """Determines high-level result processing function"""
        self._technical_vision_system.add_result_processing_function(result_processing_function)
        return self

    def build(self):
        """Returns ready-for-start technical vision system object"""
        return self._technical_vision_system
