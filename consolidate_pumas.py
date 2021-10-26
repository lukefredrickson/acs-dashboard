import os
import json
from utils.globals import *


def main():
    # setup the skeleton for the GEOJSON file
    # we'll read all the pumas into the 'features' list
    pumas_dict = {
        'type': 'FeatureCollection',
        'name': 'pumas',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'urn:ogc:def:crs:EPSG::4269'
            }
        },
        'features': []
    }
    # get list of json files in the pumas directory
    puma_files = [file for file in os.listdir(PUMAS_GEOJSON_DIRECTORY)
                  if file.endswith('.json') and file != PUMAS_GEOJSON_FILE]
    # loop through list and open all json files as python dicts
    # then add the puma data to the pumas_dict 'features' list
    print(f'Consolidating all PUMA GEOJSON files into \'{PUMAS_GEOJSON_FILE}\'')
    for puma_filename in puma_files:
        print(f'Incorporating \'{puma_filename}\'', end='')
        with open(os.path.join(PUMAS_GEOJSON_DIRECTORY, puma_filename)) as puma:
            puma_data = json.load(puma)
            for feature in puma_data['features']:
                # we need to cut down the number of coordinates so that the filesize isn't massive
                condensed_coordinates = feature['geometry']['coordinates'][0]
                # discard every other coordinate a total of 4 times, reducing file size by ~16x
                feature['geometry']['coordinates'] = [condensed_coordinates[::2][::2][::2][::2]]
                pumas_dict['features'].append(feature)
        print(' ... done!')
    # export the pumas_dict to a json file
    with open(os.path.join(PUMAS_GEOJSON_DIRECTORY, PUMAS_GEOJSON_FILE), 'w') as outfile:
        json.dump(pumas_dict, outfile)


if __name__ == '__main__':
    main()
