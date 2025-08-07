import os
import sys

from dotenv import load_dotenv

from google import genai
from google.genai import types




def main():
    print("Hello from pyllm!\n")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    arguments = sys.argv
    if len(arguments) < 2:
        print("Error: no prompt is provided")
        exit(1)

    request = arguments[1]
    verbose = False
    if len(arguments) > 2 and arguments[2] == "--verbose":
        verbose = True

    messages = [types.Content(role="user", parts=[types.Part(text=request)]),]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages
        )
    
    candidates_token_count = response.usage_metadata.candidates_token_count
    prompt_token_count = response.usage_metadata.prompt_token_count

    print(response.text)

    if verbose == True:
        print(f"User prompt: {request}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")


if __name__ == "__main__":
    main()
