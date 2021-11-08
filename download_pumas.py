import urllib.request
import os
import sys
import zipfile
from utils.download_utils import ReportHook
from utils.globals import *

# script globals
current_file = ""  # keep track of the current file being worked on
# read in filenames to download from text file
with open(PUMAS_FILE_NAMES) as file_names:
    files = file_names.read().splitlines()


def main():
    # create data path folders if they don't already exist
    for directory in [DATA_DIRECTORY, PUMAS_GEOJSON_DIRECTORY, PUMAS_SHAPE_FILE_DIRECTORY, PUMAS_ZIP_FILE_DIRECTORY]:
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass

    for file_name in files:
        global current_file
        current_file = file_name
        # download file if it doesn't already exist
        if os.path.exists(os.path.join(PUMAS_ZIP_FILE_DIRECTORY, file_name)):
            file_path = os.path.join(PUMAS_ZIP_FILE_DIRECTORY, file_name)
            print("Downloading file '%s' ... done!" % file_name)
        else:
            try:
                file_path = os.path.join(PUMAS_ZIP_FILE_DIRECTORY, file_name)
                report_hook = ReportHook()
                report_hook.current_file = current_file
                urllib.request.urlretrieve((PUMAS_DOWNLOAD_URL + file_name), file_path, reporthook=report_hook.reporthook)
                print(" ... done!")
                sys.stdout.flush()
            except urllib.error.HTTPError:
                print("Downloading file '%s' ... failed, invalid file!" % file_name)
                continue

        # unzip file
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            base_file_name, _ = os.path.splitext(file_name)
            shp_file_name = base_file_name + ".shp"
            zip_ref.extract(shp_file_name, PUMAS_SHAPE_FILE_DIRECTORY)
        print(" ... zip file extracted!")



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted, deleting incomplete downloads...\nExiting...')
        try:
            os.remove(PUMAS_ZIP_FILE_DIRECTORY + current_file)
        except FileNotFoundError:
            pass
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)