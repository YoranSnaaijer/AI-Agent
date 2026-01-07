import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    # Ensure the target file is within the working directory
    working_directory_abs = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(working_directory_abs, file_path))
    if os.path.commonpath([working_directory_abs, target_directory]) != working_directory_abs:
        return f"Error: Cannot fetch content from \"{file_path}\" as it is outside the permitted working directory"
    if not os.path.isfile(target_directory):
        return f"Error: File not found or is not a regular file: \"{file_path}\""
    try:
        with open(target_directory, "r") as file:
            file_content_string = file.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if file.read(1):
                file_content_string += f'[...File "\"{file_path}\"" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f"Error reading file \"{file_path}\": {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Fetches the content of a specified file relative to the working directory, up to a maximum character limit",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to fetch content from, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)