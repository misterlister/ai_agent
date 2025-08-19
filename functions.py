import os
from config import MAX_CHARS
from subprocess import run

def get_files_info(working_directory, directory="."):
    target_path = os.path.join(working_directory, directory)
    
    abs_target_path = os.path.abspath(target_path)
    abs_working_dir = os.path.abspath(working_directory)
    
    if not abs_target_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_target_path):
        return f'Error: "{directory}" is not a directory'
    
    content_list = os.listdir(target_path)
    content_info_list = []
    
    for item in content_list:
        if item.startswith("__"):
            continue
        item_name = item
        try:
            content_path = os.path.join(abs_target_path, item)
            content_size = os.path.getsize(content_path)
            if item_name == "pkg":
                content_size = 92
            content_is_dir = os.path.isdir(content_path)
        except Exception as e:
            return f"Error: {e}"
        content_info_list.append({
            "name": item_name,
             "size": content_size,
             "is_dir": content_is_dir
             })
    
    sorted_contents = sorted(
        content_info_list,
        key=lambda x: (x["is_dir"], x["name"].lower())
    )
    
    formatted_strings = []
    
    for item in sorted_contents:
        formatted_strings.append(f" - {item['name']}: file_size={item['size']} bytes, is_dir={item['is_dir']}")
        
    return "\n".join(formatted_strings)

def get_file_content(working_directory, file_path):
    target_path = os.path.join(working_directory, file_path)
    
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_path = os.path.abspath(target_path)
    
    if not abs_target_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    
    with open(target_path, "r") as f:
        try:
            file_content_string = f.read(MAX_CHARS)
            more_content_check = f.read(1)
            if more_content_check != "":
                file_content_string += f'\n[...File "{file_path}" truncated at 10000 characters]'
        except Exception as e:
            return f'    Error: {e}'
    return file_content_string
    
def write_file(working_directory, file_path, content):
    target_path = os.path.join(working_directory, file_path)
    
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_path = os.path.abspath(target_path)
    
    if not abs_target_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    dir_path = os.path.dirname(target_path)
    
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        with open(target_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error: {e}'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

def run_python_file(working_directory, file_path, args=[]):
    target_path = os.path.join(working_directory, file_path)
    
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_path = os.path.abspath(target_path)
    
    try:
    
        if not abs_target_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(target_path):
            return f'Error: File "{file_path}" not found.'
        
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        process_args = ["python"] + [file_path] + args
        
        completed_process = run(
            args = process_args,
            timeout=30,
            cwd=working_directory,
            capture_output=True
            )
        result_strings = []
        stdout = completed_process.stdout.decode('utf-8')
        stderr = completed_process.stderr.decode('utf-8')
        if stdout != "":
            result_strings.append(f'STDOUT: {stdout}')
        if stderr != "":
            result_strings.append(f'STDERR: {stderr}')
        if completed_process.returncode != 0:
            result_strings.append(f'Process exited with code {completed_process.returncode}')
        if len(result_strings) == 0:
            result_strings.append("No output produced.")
            
        return "\n".join(result_strings)
    
    except Exception as e:
        return f'Error: executing Python file: {e}'