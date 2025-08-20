from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

function_dict = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file
}

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
        schema_get_file_content
    ]
)

default_working_directory = "./calculator"

def call_function(function_call_part: types.FunctionCall, verbose: bool = False):
    try:
        function_name = function_call_part.name
        function_args = function_call_part.args
        if verbose:
            print(f"Calling function: {function_name}({function_args})")
        else:
            print(f" - Calling function: {function_name}")
    
        func = function_dict[function_name]
        
        function_args.update({"working_directory": default_working_directory})
        
        function_result = func(**function_args)
        
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
)
        
    except KeyError:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],)
    except Exception as e:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"{e}"},
            )
        ],)