import os
from subprocess import run

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