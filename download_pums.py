import urllib.request
import zipfile
import os
from os.path import exists
import sys
import time

with open("./pums_file_names.txt") as file_names:
    files = file_names.read().splitlines()

base_url = "https://www2.census.gov/programs-surveys/acs/data/pums/2019/5-Year/"
data_path = "./data/pums/"
zip_path = "./data/pums/zip/"
current_file = ""

start_time = None
def reporthook(count, block_size, total_size):
    global start_time
    global current_file
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / ((1024 * duration) + 1))
    sys.stdout.write("\rDownloading file '%s' ... %d MB, %d KB/s, %d seconds passed" %
                    (current_file, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()

def fixBadZipfile(zipFile):  
    f = open(zipFile, 'r+b')  
    data = f.read()  
    pos = data.find(b'\x50\x4b\x05\x06') # End of central directory signature  
    if (pos > 0):  
        print(" ... Truncating file at location " + str(pos + 22)+ ".", end="")  
        f.seek(pos + 22)   # size of 'ZIP end of central directory record' 
        f.truncate()  
        f.close()  
    else:  
        # raise error, file is truncated  
        print(" ... Error: File is truncated")

def main():
    # create data path folder if it doesn't already exist
    try:
        os.mkdir(data_path)
    except FileExistsError:
        pass
    try:
        os.mkdir(zip_path)
    except FileExistsError:
        pass

    for file_name in files:
        global current_file
        current_file = file_name
        file_path = ""
        
        # download file if it doesn't already exist
        if exists(os.path.join(data_path, file_name)):
            file_path = os.path.join(data_path, file_name)
            print("Downloading file '%s' ... done!" % file_name, end="")
        elif exists(os.path.join(zip_path, file_name)):
            file_path = os.path.join(zip_path, file_name)
            print("Downloading file '%s' ... done!" % file_name, end="")
        else:
            try:
                urllib.request.urlretrieve((base_url + file_name), os.path.join(data_path, file_name), reporthook=reporthook)
                print(" ... done!", end="")
                sys.stdout.flush()
                file_path = os.path.join(data_path, file_name)
            except urllib.error.HTTPError:
                print("Downloading file '%s' ... failed, invalid file!" % file_name)
                continue
        
        # unzip
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(data_path)
            print(" ... zip file extracted!")
        except zipfile.BadZipFile:
            fixBadZipfile(file_path)
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(data_path)
                print(" ... zip file extracted!")
            except zipfile.BadZipFile:
                continue
        
        # move zip file to ./data/pums/zip if it's in ./data/pums
        new_file_path = os.path.join(zip_path, file_name)
        if (file_path != new_file_path):
            os.rename(file_path, new_file_path)

    print("All files downloaded and extracted.")

    del_zips = ""
    while del_zips != "y" and del_zips != "n":
        del_zips = input("Do you wish to delete leftover zip files? (y/n): ")
    
    files_in_directory = os.listdir(zip_path)
    zip_files = [f for f in files_in_directory if f.endswith(".zip")]
    if del_zips == "y":
        print("Removing leftover zip files.")
        for f in zip_files:
            path_to_file = os.path.join(zip_path, f)
            os.remove(path_to_file)
    else:
        print("Leftover zip files transfered to '%s'." % zip_path)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted, deleting incomplete downloads...\nExiting...')
        try:
            os.remove(data_path + current_file)
        except FileNotFoundError:
            pass
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)