import os.path
import os
from functions.config import get_max_chars
from google import genai
from google.genai import types

max_char = get_max_chars()

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Read the content of the specified file (the first {max_char} characters) withing the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to get content of, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    rel_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(rel_path)
    abs_path_root = os.path.abspath(working_directory)
    

    if not abs_path.startswith(abs_path_root):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        f = open(abs_path)
        file_content_string = f.read(max_char)
    
        if os.path.getsize(abs_path) > max_char:
            file_content_string += f'...File "{file_path}" truncated at {max_char} characters'
    
        #print(file_content_string)

        f.close() 

    except Exception as e:
        print(f"Error encountered: {e}")

    return file_content_string

#print(get_file_content("calculator", "lorem.txt"))