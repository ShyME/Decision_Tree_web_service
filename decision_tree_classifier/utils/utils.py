import os
import uuid
import time


def get_unique_filename(extension):
    return str(uuid.uuid4()) + "." + extension


def delete_old_files_from(path, time_old):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if is_file_older_than(file_path, time_old):
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                print(f"The file scheduled to be deleted: {file_path} does not exist!")


def is_file_older_than(file, time_old):
    time_last_modified = os.path.getmtime(file)
    time_now = time.time()
    delta_time = time_now - time_last_modified
    return delta_time >= time_old
