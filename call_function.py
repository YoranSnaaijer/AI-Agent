from google.genai import types
from config import WORKING_DIRECTORY
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

# Define the set of tools available to the AI model
# Each tool maps to a Python function with a JSON schema describing its parameters
available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],
)

def call_function(function_call, verbose=False):
    """Execute a function call requested by the AI model.
    
    Args:
        function_call: The function call object from the GenAI model containing
                      the function name and arguments.
        verbose (bool): If True, print detailed information about the function call.
    
    Returns:
        types.Content: A Content object containing the function result formatted
                      for the GenAI model.
    """
    # Log the function call
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    # Map function names to their implementations
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    function_name = function_call.name or ""
    
    # Check if the requested function is available
    if function_name not in function_map:
        # Return error response if function doesn't exist
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                    ),
                ],
            )
    else:
        # Extract arguments and inject the working directory
        args = dict(function_call.args) if function_call.args else {}
        args["working_directory"] = WORKING_DIRECTORY
        # Execute the function with the provided arguments
        function_result = function_map[function_name](**args)
        # Return the result wrapped in the GenAI Content format
        return types.Content(
            role="tool",
            parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
                )
            ],
        )