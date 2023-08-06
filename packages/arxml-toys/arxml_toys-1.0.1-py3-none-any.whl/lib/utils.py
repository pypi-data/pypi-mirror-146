from datetime import datetime
import shutil
import os.path

def backup_original_file(filename):
    (root, ext) = os.path.splitext(filename)
    dt = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_filename = root + "-" + dt + ext
    print(backup_filename)

    if os.path.isfile(filename):
        shutil.copy(filename, backup_filename)