import requests
import os
import sys
from utils.globals import *

# script globals
current_file = ""  # current file being worked on
json_file_path = ""  # write-path of the current file
# read in filenames to convert from text file
with open(PUMAS_FILE_NAMES) as file_names:
    files = file_names.read().splitlines()


def main():
    for file_name in files:
        global current_file
        global json_file_path

        current_file = file_name
        # get the base filename from zip file, then join with .json extension for output name
        json_file_name = (os.path.splitext(file_name)[0] + '.json')
        # join json output name with output directory for full write-path
        json_file_path = os.path.join(PUMAS_GEOJSON_DIRECTORY, json_file_name)

        print("Converting '%s' to geojson" % file_name, end="")

        if os.path.exists(json_file_path):
            print(" ... geojson already exists")
            continue

        if os.path.exists(os.path.join(PUMAS_ZIP_FILE_DIRECTORY, file_name)):
            shapefile = open(os.path.join(PUMAS_ZIP_FILE_DIRECTORY, file_name), 'rb')
            # use ogre to convert zipped shapefile to geojson
            try:
                converter_res = requests.post(SHAPEFILE_TO_GEOJSON_CONVERTER, 
                                              files={'upload': (file_name, shapefile)}, timeout=100)
            # except request timeout
            except requests.ReadTimeout:
                print(" ... conversion failed, request timed out")
                continue
            # good conversion
            if converter_res.status_code == 200:
                with open(json_file_path, 'wb') as geojson:
                    geojson.write(converter_res.content)
                print(" ... conversion successful!")
            else:
                print(" ... conversion failed, invalid request to ogre conversion tool")
        else:
            print(" ... conversion failed, shapefile not found")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted, deleting incomplete conversions...\nExiting...')
        try:
            os.remove(json_file_path)  # remove incomplete file if interrupted
        except FileNotFoundError:
            pass
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)