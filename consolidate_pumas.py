import os
import json

# directory path to the pumas directory
data_path = './data/pumas/'
# filename of big puma GEOJSON file we'll use
consolidated_puma = 'pumas.json'


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
    puma_files = [file for file in os.listdir(data_path)
                  if file.endswith('.json') and file != consolidated_puma]
    # loop through list and open all json files as python dicts
    # then add the puma data to the pumas_dict 'features' list
    for puma_filename in puma_files:
        with open(os.path.join(data_path, puma_filename)) as puma:
            puma_data = json.load(puma)
            pumas_dict['features'].append(puma_data['features'][0])
    # export the pumas_dict to a json file
    with open(os.path.join(data_path, consolidated_puma), 'w') as outfile:
        json.dump(pumas_dict, outfile)


if __name__ == '__main__':
    main()

