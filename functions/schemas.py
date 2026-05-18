from google.genai import types

schema_getFilesInfo = types.FunctionDeclaration(
    name="getFilesInfo",
    description="Lists all files in a specified directory relative to the working directory, returns the names, isDir, and file size",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The relative of path of the directory we need the info for, is always relative to the working directory",
                default=".",
            )
        },
    ),
)

schema_getFileContent = types.FunctionDeclaration(
    name="getFileContent",
    description="return the text content of the given file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path of the file to be read relative to the working directory/ root of the project",
            )
        },
    ),
)
schema_writeToFile = types.FunctionDeclaration(
    name="writeToFile",
    description="allows you to write a new file, or overWrite an existing one, by providing the relative path of the object from the root directory and the new content to write it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path of the file to write or overwrite relative the project root",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content to put in the file at file_path",
            ),
        },
        required=["file_path"],
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="used to run a python file with the file_path being relative to the root of the project / working_Directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path of the python file to be run relative to the root of the project or working_directory, should also include the extension",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="an array of arguments for the python file",
            ),
        },
        required=["file_path"],
    ),
)
avail_functions = types.Tool(
    function_declarations=[
        schema_getFilesInfo,
        schema_getFileContent,
        schema_writeToFile,
        schema_run_python_file,
    ],
)
