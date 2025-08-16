import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key = api_key)

def main():
    model_name = "gemini-2.0-flash-001"
    prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    
    response = client.models.generate_content(model = model_name, contents = prompt)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    
    print(response.text)
    print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")

if __name__ == "__main__":
    main()
