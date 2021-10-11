import requests
import os
import sys

with open("./puma_file_names.txt") as file_names:
    files = file_names.read().splitlines()

converter = "http://ogre.adc4gis.com/convert"
data_path = "./data/pumas/"
zip_path = "./data/pumas/zip/"
current_file = ""
json_file_path = ""

def main():
    for file_name in files:
        global current_file
        global json_file_path

        current_file = file_name
        json_file_name = (os.path.splitext(file_name)[0] + '.json')
        json_file_path = os.path.join(data_path, json_file_name)

        print("Converting '%s' to geojson" % (file_name), end="")

        if os.path.exists(json_file_path):
            print(" ... geojson already exists")
            continue

        if os.path.exists(os.path.join(zip_path, file_name)):
            shapefile = open(os.path.join(zip_path, file_name), 'rb')
            # use ogre to convert zipped shapefile to geojson
            try:
                converter_res = requests.post(converter, files={'upload': (file_name, shapefile)}, timeout=10)
            except requests.ReadTimeout:
                print(" ... conversion failed, request timed out")
                continue

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
            os.remove(json_file_path)
        except FileNotFoundError:
            pass
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)