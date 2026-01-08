import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    # Ensure the target directory is within the working directory
    # Convert the working directory to an absolute path for secure path comparison
    working_directory_abs = os.path.abspath(working_directory)
    # Normalize the full target path by joining working directory with requested directory path
    target_directory = os.path.normpath(os.path.join(working_directory_abs, directory))
    # Security check: verify that the target directory is still within the working directory scope
    if os.path.commonpath([working_directory_abs, target_directory]) != working_directory_abs:
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    # Verify that the path points to an actual directory that exists
    if not os.path.isdir(target_directory):
        return f"Error: \"{directory}\" is not a directory"

    contents_of_directory = []
    # List files and their sizes
    try:
        # Iterate through all entries (files and directories) in the target directory
        for file in os.listdir(target_directory):
            # Build the full path for the current entry to get metadata
            file_full_path = os.path.join(target_directory, file)
            # Get the file size in bytes
            file_size = os.path.getsize(file_full_path)
            # Check if the entry is a directory (vs. a regular file)
            is_directory = os.path.isdir(file_full_path)
            # Format the entry as a string with metadata and add it to the collection
            contents_of_directory.append(f"- {file}: file_size={file_size} bytes, is_dir={is_directory}")
    except Exception as e:
        # Catch any file system errors during listing (permissions, I/O errors, etc.)
        return f"Error reading directory: {e}"
    # Join all entries with newlines to create a readable, formatted output
    return "\n".join(contents_of_directory)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)