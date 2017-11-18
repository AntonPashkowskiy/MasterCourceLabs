#!/usr/bin/python3
"""System of technical vision startup module"""
import argparse
import json
from tvs_builder import TechnicalVisionSystemBuilder
from high_level_processing.preprocessing import clean_output_directory
from high_level_processing.faces_hl_processing import faces_hl_processing


def _parse_arguments():
    parser = argparse.ArgumentParser(\
        description="The System of technical vision for different tasks.",\
        prog="tvs")
    parser.add_argument(\
        "-s",\
        "--settings",\
        type=str,\
        default="settings.json",\
        help="JSON file with settings")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.5")

    return parser.parse_args()


def main():
    """System of technical vision startup file"""
    args = _parse_arguments()
    with open(args.settings) as json_file:
        settings = json.load(json_file)
        technical_vision_system_builder = TechnicalVisionSystemBuilder()\
            .from_sources(settings["image_acquisition"]["sources"])\
            .with_preprocessing(clean_output_directory)\
            .with_filters(settings["preprocessing"]["filters_chain"])\
            .with_details_extraction_methods(settings["details_extraction"]["methods"])\
            .with_detection_methods(settings["detection_and_segmentation"]["methods"])\
            .result_processed_by(faces_hl_processing)

        if settings["image_acquisition"]["is_parallel_processing"]:
            print("Parallel processing")
            technical_vision_system_builder.in_parallel()

        technical_vision_system = technical_vision_system_builder.build()
        technical_vision_system.start_processing()


if __name__ == "__main__":
    main()
