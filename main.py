import os
import sys

from functions.get_files_info import schema_get_files_info
from dotenv import load_dotenv

from google import genai
from google.genai import types



def main():
    print("Hello from pyllm!\n")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    model_name = os.environ.get("MODEL")
    
    system_prompt = system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

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

    """
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages
        )
    """
    
    response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    
    candidates_token_count = response.usage_metadata.candidates_token_count
    prompt_token_count = response.usage_metadata.prompt_token_count

    #print(f"{response.text}\n")
    print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")

    if verbose == True:
        print(f"User prompt: {request}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")


if __name__ == "__main__":
    main()
