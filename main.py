import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv


def main():
    
    load_dotenv()
    
    if len(sys.argv) < 2:
        print("Error: no prompt provided")
        sys.exit(1)
        
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key = api_key)
    
    user_prompt = sys.argv[1]
    
    verbose_output: bool = "--verbose" in sys.argv
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    
    if verbose_output:
        print(f"User prompt: {user_prompt}")
    
    generate_content(client, messages, verbose_output)

        
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = messages
    )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    
    print(response.text)
    
    if verbose:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

if __name__ == "__main__":
    main()
