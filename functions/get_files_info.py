import os

def get_files_info(working_directory, directory="."):
    # Ensure the target directory is within the working directory
    working_directory_abs = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(working_directory_abs, directory))
    if os.path.commonpath([working_directory_abs, target_directory]) != working_directory_abs:
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    if not os.path.isdir(target_directory):
        return f"Error: \"{directory}\" is not a directory"

    contents_of_directory = []
    # List files and their sizes
    try:
        for file in os.listdir(target_directory):
            contents_of_directory.append(f"- {file}: file_size={os.path.getsize(os.path.join(target_directory, file))} bytes, is_dir={os.path.isdir(os.path.join(target_directory, file))}")
    except Exception as e:
        return f"Error reading directory: {e}"
    return "\n".join(contents_of_directory)