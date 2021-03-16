from django.core.exceptions import ValidationError


def validate_file_size(value):
    file_size = value.size

    MAX_FILE_SIZE = 1073741824  # 1 GB in bytes

    if file_size > MAX_FILE_SIZE:
        raise ValidationError("The maximum file size that can be uploaded is 1GB")
    else:
        return value
