import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    # Ensure the target file is within the working directory
    # Convert the working directory to an absolute path for secure path comparison
    working_directory_abs = os.path.abspath(working_directory)
    # Normalize the full target path by joining working directory with requested file path
    target_directory = os.path.normpath(os.path.join(working_directory_abs, file_path))
    # Security check: verify that the target file is still within the working directory
    if os.path.commonpath([working_directory_abs, target_directory]) != working_directory_abs:
        return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
    # Verify that the path points to a regular file that actually exists
    if not os.path.isfile(target_directory):
        return f"Error: \"{file_path}\" does not exist or is not a regular file"
    # Additional security check: ensure we're only executing Python files (must end with .py)
    if not file_path.endswith('.py'):
        return f"Error: \"{file_path}\" is not a Python file"
    try:
        # Build the command: ["python", absolute_path_to_file]
        command = ["python", target_directory]
        # Add optional command-line arguments if provided
        command.extend(args) if args else []
        # Execute the Python file using subprocess with safety measures:
        result = subprocess.run(command, cwd=working_directory_abs, capture_output=True, text=True, timeout=30)
        # Check if the process execution failed (non-zero exit code)
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}."
        else:
            # Return output based on what the process produced
            if result.stdout:
                return f"STDOUT:\n{result.stdout}"
            if result.stderr:
                return f"STDERR:\n{result.stderr}"
            if not result.stdout and not result.stderr:
                return "No output produced."
    except subprocess.TimeoutExpired:
        # Catch timeout errors (script ran longer than 30 seconds)
        return f"Error executing \"{file_path}\": Script execution timed out (exceeded 30 seconds)"
    except Exception as e:
        # Catch any other subprocess or OS errors (permissions, missing interpreter, etc.)
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