import os
import sys

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

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
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
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

    if verbose:
        print(f"User prompt: {request}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")

    if not response.function_calls:
        print(f"{response.text}\n")
        return

    for function_call_part in response.function_calls:
        #print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        function_call_result = call_function(function_call_part, verbose)

        if not function_call_result.parts[0].function_response.response:
            raise Exception("Fatal error!")
            print("Fatal error!")
        elif verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")


    
        


if __name__ == "__main__":
    main()
