import os

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