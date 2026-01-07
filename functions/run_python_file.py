import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    # Ensure the target file is within the working directory
    working_directory_abs = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(working_directory_abs, file_path))
    if os.path.commonpath([working_directory_abs, target_directory]) != working_directory_abs:
        return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
    # Check if the target is a directory
    if not os.path.isfile(target_directory):
        return f"Error: \"{file_path}\" does not exist or is not a regular file"
    # Check if the file is a Python file
    if not file_path.endswith('.py'):
        return f"Error: \"{file_path}\" is not a Python file"
    try:
        # Construct command list to run subprocesses
        command = ["python", target_directory]
        command.extend(args) if args else []
        result = subprocess.run(command, cwd=working_directory_abs, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}."
        else:
            if result.stdout or result.stderr:
                return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            else:
                return "No output produced."
    except Exception as e:
        return f"Error executing \"{file_path}\": {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments relative to the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to fetch content from, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python file",
            ),
        },
        required=["file_path"]
    ),
)