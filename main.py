import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

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
    # Prepare the message content as list for memory
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    # Initialize the GenAI client
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.5-flash", 
                                              contents=messages, 
                                              config=types.GenerateContentConfig(tools=[available_functions],
                                                                                 system_instruction=system_prompt,
                                                                                 temperature=2))
    if args.verbose:
        # Ensure usage metadata is available
        if response.usage_metadata is None:
            raise RuntimeError("Usage metadata is None")
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count} \nResponse tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f"Response: \n{response.text}")

if __name__ == "__main__":
    main()
