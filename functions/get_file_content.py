from config import MAX_CHARS
import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns up to 10000 characters of textual file content from a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath and name of the file to read from, relative to the working directory.",
            ),
        },
    ),
)

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

