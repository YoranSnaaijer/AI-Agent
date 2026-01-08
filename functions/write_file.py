import os
from google.genai import types

def write_file(working_directory, file_path, content):
    # Ensure the target file is within the working directory
    # Convert the working directory to an absolute path for secure path comparison
    working_directory_abs = os.path.abspath(working_directory)
    # Normalize the full target path by joining working directory with requested file path
    target_directory = os.path.normpath(os.path.join(working_directory_abs, file_path))
    # Security check: verify that the target file path is still within the working directory
    if os.path.commonpath([working_directory_abs, target_directory]) != working_directory_abs:
        return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
    # Verify that the target is not a directory (we need to write to a file, not modify a directory)
    if os.path.isdir(target_directory):
        return f"Error: Cannot write to \"{file_path}\" as it is a directory"
    # Create all parent directories if they don't exist
    os.makedirs(os.path.dirname(target_directory), exist_ok=True)
    # Write content to the file
    try:
        # Open the file in write mode ("w") which creates it if it doesn't exist or overwrites it if it does
        with open(target_directory, "w") as file:
            # Write the provided content to the file
            file.write(content)
        # Return success message with the number of characters written for user feedback
        return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)."
    except Exception as e:
        # Catch any file writing errors (permissions issues, disk full, invalid paths, etc.)
        return f"Error writing to \"{file_path}\": {e}"
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory, creating parent directories if necessary",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write content to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"]
    ),
)