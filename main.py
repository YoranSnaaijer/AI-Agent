import os
import argparse
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()
# Set up API key from environment variable
api_key = os.environ.get("GEMINI_API_KEY")
# Raise an error if the API key is not found
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")
parser = argparse.ArgumentParser(description="AI Agent using Google GenAI")
parser.add_argument("user_prompt", type=str, help="The prompt to send to the AI model")
args = parser.parse_args()


def main():
    print("Hello from ai-agent!")
    # Initialize the GenAI client
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=args.user_prompt)
    if response.usage_metadata is None:
        raise RuntimeError("Usage metadata is None")
    print(f"User Prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count} \nResponse tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: \n{response.text}")

if __name__ == "__main__":
    main()
