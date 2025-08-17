import os.path
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    rel_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(rel_path)
    abs_path_root = os.path.abspath(working_directory)

    if not abs_path.startswith(abs_path_root):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_path):
        return f'Error: File "{file_path}" not found.'

    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    
    process_args = ["python3", rel_path] + args

    try:
        complete_process = subprocess.run(process_args, capture_output=True, text=True, timeout=30)

        subprocess_string = f"STDOUT:\n{complete_process.stdout}\nSTDERR:\n{complete_process.stderr}\n"
        if complete_process.returncode != 0:
            subprocess_string += f'Process exited with code {complete_process.returncode}\n'

        if subprocess_string == None:
            return f'No output produced.'

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    return subprocess_string