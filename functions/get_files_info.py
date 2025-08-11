import os.path
import os

def get_files_info(working_directory, directory="."):
    rel_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(rel_path)
    abs_path_root = os.path.abspath(working_directory)
    #print(abs_path)
    #print(abs_path_root)

    if not abs_path.startswith(abs_path_root):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'

    try:
        files_data = []
        for file_name in os.listdir(abs_path):
            file_path = os.path.join(abs_path, file_name)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            files_data.append(f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(files_data)

    except Exception as e:
        print(f"Error encountered: {e}")


    return rel_path

#print(get_files_info("calculator"))
#print(get_files_info("calculator", "pkg"))
#print(get_files_info("calculator", "bin"))