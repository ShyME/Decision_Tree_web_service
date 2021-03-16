import uuid


def get_unique_filename(extension):
    return str(uuid.uuid4()) + "." + extension


def delete_old_files_from(path):
    pass
