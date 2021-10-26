import urllib.request
import os
import sys
from utils.download_utils import ReportHook, fix_bad_zip_file
from utils.globals import *

# script globals
current_file = ""  # keep track of the current file being worked on
# read in filenames to download from text file
with open(PUMAS_FILE_NAMES) as file_names:
    files = file_names.read().splitlines()


def main():
    # create data path folders if they don't already exist
    for directory in [DATA_DIRECTORY, PUMAS_GEOJSON_DIRECTORY, PUMAS_ZIP_FILE_DIRECTORY]:
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass

    for file_name in files:
        global current_file
        current_file = file_name
        
        # download file if it doesn't already exist
        if os.path.exists(os.path.join(PUMAS_GEOJSON_DIRECTORY, file_name)):
            file_path = os.path.join(PUMAS_GEOJSON_DIRECTORY, file_name)
            print("Downloading file '%s' ... done!" % file_name)
        elif os.path.exists(os.path.join(PUMAS_ZIP_FILE_DIRECTORY, file_name)):
            file_path = os.path.join(PUMAS_ZIP_FILE_DIRECTORY, file_name)
            print("Downloading file '%s' ... done!" % file_name)
        else:
            try:
                file_path = os.path.join(PUMAS_GEOJSON_DIRECTORY, file_name)
                report_hook = ReportHook()
                report_hook.current_file = current_file
                urllib.request.urlretrieve((PUMAS_DOWNLOAD_URL + file_name), file_path, reporthook=report_hook.reporthook)
                print(" ... done!")
                sys.stdout.flush()
            except urllib.error.HTTPError:
                print("Downloading file '%s' ... failed, invalid file!" % file_name)
                continue
        
        # move zip file to ./data/puma/zip if it's in ./data/puma
        new_file_path = os.path.join(PUMAS_ZIP_FILE_DIRECTORY, file_name)
        if file_path != new_file_path:
            os.rename(file_path, new_file_path)

    # prompt user to delete leftover zip files to free up space
    del_zips = ""
    while del_zips != "y" and del_zips != "n":
        del_zips = input("Do you wish to delete leftover zip files? (y/n): ")

    files_in_directory = os.listdir(PUMAS_ZIP_FILE_DIRECTORY)
    zip_files = [f for f in files_in_directory if f.endswith(".zip")]
    if del_zips == "y":
        print("Removing leftover zip files.")
        for f in zip_files:
            path_to_file = os.path.join(PUMAS_ZIP_FILE_DIRECTORY, f)
            os.remove(path_to_file)
    else:
        print("Leftover zip files transfered to '%s'." % PUMAS_ZIP_FILE_DIRECTORY)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted, deleting incomplete downloads...\nExiting...')
        try:
            os.remove(PUMAS_GEOJSON_DIRECTORY + current_file)
        except FileNotFoundError:
            pass
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)