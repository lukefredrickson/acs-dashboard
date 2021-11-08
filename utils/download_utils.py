import time
import sys


def fix_bad_zip_file(zip_file):
    f = open(zip_file, 'r+b')
    data = f.read()
    pos = data.find(b'\x50\x4b\x05\x06')  # End of central directory signature
    if (pos > 0):
        print(" ... Truncating file at location " + str(pos + 22) + ".", end="")
        f.seek(pos + 22)  # size of 'ZIP end of central directory record'
        f.truncate()
        f.close()
    else:
        # raise error, file is truncated
        print(" ... Error: File is truncated")


class ReportHook:
    def __init__(self):
        self.current_file = ""
        self.start_time = None

    def reporthook(self, count, block_size, total_size):
        if count == 0:
            self.start_time = time.time()
            return
        duration = time.time() - self.start_time
        progress_size = int(count * block_size)
        speed = int(progress_size / ((1024 * duration) + 1))
        sys.stdout.write("\rDownloading file '%s' ... %d KB, %d KB/s, %0.2f sec elapsed" %
                         (self.current_file, progress_size, speed, duration))
        sys.stdout.flush()
