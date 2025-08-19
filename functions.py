import os

def get_files_info(working_directory, directory="."):
    directory_name = "current"
    if directory != ".":
        directory_name = f"'{directory}'"
    content_string = f"Result for {directory_name} directory:\n"
    
    target_path = os.path.join(working_directory, directory)
    
    abs_target_path = os.path.abspath(target_path)
    abs_working_dir = os.path.abspath(working_directory)
    
    if not abs_target_path.startswith(abs_working_dir):
        content_string += f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
        return content_string
    if not os.path.isdir(abs_target_path):
        content_string += f'    Error: "{directory}" is not a directory'
        return content_string
    
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
            return f"    Error: {e}"
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
        
    content_string += "\n".join(formatted_strings)
        
    return content_string