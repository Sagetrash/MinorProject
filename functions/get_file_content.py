import os


def getFileContent(working_directory, file_path):
    try:
        base_path = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(working_directory, file_path))
        if not os.path.isfile(target):
            return f"error: {file_path} file not found, or is not a regular file"

        try:
            valid = os.path.commonpath([target, base_path]) == base_path
        except ValueError:
            valid = False
        if not valid:
            return f"error: cannot the contents of {file_path} as it is outside the permited scope"
        max_chars = 10000
        with open(target, "r") as file:
            file_content_string = file.read(max_chars)
            if file.read(1):
                file_content_string += (
                    f'\n[...File "{file_path}" truncated at {max_chars} characters]'
                )

        return file_content_string
    except Exception as e:
        return f"error reading file {file_path}: {str(e)}"
