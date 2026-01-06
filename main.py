import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()
# Set up API key from environment variable
api_key = os.environ.get("GEMINI_API_KEY")
# Raise an error if the API key is not found
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")



def main():
    print("Hello from ai-agent!")
    # Initialize the GenAI client
    client = genai.Client(api_key=api_key)
    prompt ="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    if response.usage_metadata is None:
        raise RuntimeError("Usage metadata is None")
    print(f"User Prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count} \nResponse tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: \n{response.text}")

if __name__ == "__main__":
    main()
