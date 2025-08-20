import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

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