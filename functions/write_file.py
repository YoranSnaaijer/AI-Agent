import os

def write_file(working_directory, file_path, content):
    # Ensure the target file is within the working directory
    working_directory_abs = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(working_directory_abs, file_path))
    if os.path.commonpath([working_directory_abs, target_directory]) != working_directory_abs:
        return f"Error: Cannot write to {file_path} as it is outside the permitted working directory"
    # Check if the target is a directory
    if os.path.isdir(target_directory):
        return f"Error: Cannot write to {file_path} as it is a directory"
    # Create parent directories if they do not exist
    os.makedirs(os.path.dirname(target_directory), exist_ok=True)
    # Write content to the file
    try:
        with open(target_directory, "w") as file:
            file.write(content)
        return f"Successfully wrote to {file_path} ({len(content)} characters written)."
    except Exception as e:
        return f"Error writing to {file_path}: {e}"
    return