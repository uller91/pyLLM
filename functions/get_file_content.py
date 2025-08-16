import os.path
import os
from functions.config import get_max_chars

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
        file_content_string = f.read(get_max_chars())
    
        if os.path.getsize(abs_path) > get_max_chars():
            file_content_string += f'...File "{file_path}" truncated at {get_max_chars()} characters'
    
        #print(file_content_string)

        f.close() 

    except Exception as e:
        print(f"Error encountered: {e}")

    return file_content_string

#print(get_file_content("calculator", "lorem.txt"))