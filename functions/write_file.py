import os


def writeToFile(working_directory, file_path, content=""):
    try:
        abs_path = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(abs_path, file_path))

        if os.path.commonpath([target, abs_path]) != abs_path:
            return f"error: given file path {file_path} is out of permited scope"

        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target), exist_ok=True)

        with open(target, "w") as f:
            f.write(content)
        return "File successfully written to disk."
    except Exception as e:
        return f"unable to write file: {file_path}, {e}"
