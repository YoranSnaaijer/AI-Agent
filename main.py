import os
import argparse
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    # Load environment variables from .env file
    load_dotenv()
    # Set up API key from environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    # Raise an error if the API key is not found
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables")
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="AI Agent using Google GenAI")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to the AI model")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Prepare the message content as list for memory (maintains conversation history)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    # Initialize the GenAI client with the API key
    client = genai.Client(api_key=api_key)
    # Main agent loop: processes model responses and function calls
    # Continues until model provides a final text response (no function calls)
    for _ in range(20):
        # Call the GenAI model with conversation history and available tools
        response = client.models.generate_content(model="gemini-2.5-flash",
                                                  contents=messages, 
                                                  config=types.GenerateContentConfig(tools=[available_functions],
                                                                                     system_instruction=system_prompt,
                                                                                     temperature=0))
        # Add model response to conversation history
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate)
        # Log token usage if verbose mode is enabled
        if args.verbose:
            # Ensure usage metadata is available
            if response.usage_metadata is None:
                raise RuntimeError("Usage metadata is None")
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count} \nResponse tokens: {response.usage_metadata.candidates_token_count}")
        
        # Check if model requested any function calls
        function_results = []
        if response.function_calls:
            # Process each function call requested by the model
            for function_call in response.function_calls:
                # Execute the requested function and capture the result
                function_call_result = call_function(function_call, verbose=args.verbose)
                # Validate response structure
                if function_call_result.parts is None:
                    raise Exception("Function response has no parts")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("Function response is None")
                if  function_call_result.parts[0].function_response is None:
                    raise Exception("Function response content is None")
                else:
                    function_results.append(function_call_result.parts[0])
                # Log function response if verbose mode is enabled
                if args.verbose:
                    # Ensure usage metadata is available
                    if response.usage_metadata is None:
                        raise RuntimeError("Usage metadata is None")
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            # No function calls - model provided a final text response
            print(f"Response: \n{response.text}")
            return
        # Add function results to conversation history to continue the loop
        messages.append(types.Content(role="user", parts=function_results))
    # Exit with error code if loop completes without a final response
    sys.exit(1)

if __name__ == "__main__":
    main()
