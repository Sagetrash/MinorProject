import os

"""
Result for current directory:
  - main.py: file_size=719 bytes, is_dir=False
  - tests.py: file_size=1331 bytes, is_dir=False
  - pkg: file_size=44 bytes, is_dir=True
"""


def getFilesInfo(working_directory, directory="."):
    try:
        base_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, directory))
        if not os.path.isdir(target_path):
            return f"error: {directory} is not a directory"
        try:
            valid = os.path.commonpath([target_path, base_path]) == base_path
        except ValueError:
            valid = False

        if not valid:
            return f"error: cannot list the contents of {directory} as it is outside the permited scope"
        res = "Results for current directory: \n"

        for i in os.listdir(target_path):
            filepath = os.path.join(target_path, i)
            isDir = os.path.isdir(filepath)
            fileSize = os.path.getsize(filepath)
            res += f"- {i}: file_size = {fileSize} bytes, is_dir = {isDir} \n"
        return res
    except Exception as e:
        return f"error listing files in {directory}: {str(e)}"
