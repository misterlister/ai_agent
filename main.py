import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.call_function import call_function, available_functions
from prompts import system_prompt
from constants import MAX_ITERATIONS


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
    
    iterations = 0
    while True:
        iterations += 1
        if iterations > MAX_ITERATIONS:
            print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, verbose_output)
            if final_response:
                print("Final Response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generating content: {e}")
            break


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt),
    )
    
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    
    if verbose:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        
    if not response.function_calls:
        return response.text
    
    function_responses = []
    
    for function_call in response.function_calls:
        result: types.Content = call_function(function_call, verbose)
        if not result.parts or not result.parts[0].function_response.response:
            raise Exception(f"no response from function {function_call.name}.")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])
        
    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    
    messages.append(types.Content(role="user", parts=function_responses))
        
    return None

if __name__ == "__main__":
    main()
