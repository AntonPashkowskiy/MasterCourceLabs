#!/usr/bin/python3
import os


def clean_directory(directory_path):
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if not os.path.isdir(filepath):
            os.remove(filepath)


def main():
    sources_directory = os.path.join(".", "data", "images", "sources")
    results_directory = os.path.join(".", "data", "images", "results")
    clean_directory(sources_directory)
    clean_directory(results_directory)


if __name__ == "__main__":
    main()
