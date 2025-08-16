import os.path

def write_file(working_directory, file_path, content):
    rel_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(rel_path)
    abs_path_root = os.path.abspath(working_directory)

    if not abs_path.startswith(abs_path_root):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_path):
        try:
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(abs_path) and os.path.isdir(abs_path):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        f = open(abs_path, "w")
        f.write(content)
        f.close()

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        print(f"Error encountered: {e}")

    
