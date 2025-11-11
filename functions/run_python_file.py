import os
import subprocess
import sys
from google import genai
from google.genai import types

#!###############################################################################################!#
#! Do not give this program to others for them to use!                                           !#
#! It does not have all the security and safety features that a production AI agent would have.  !#
#! It is for learning purposes only.                                                             !#
#!###############################################################################################!#
def run_python_file(working_directory, file_path, args=[]):
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(abs_working, file_path))
    allowed = abs_target.startswith(abs_working + os.sep) or (abs_target == abs_working)

    if not allowed:
        return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not os.path.exists(abs_target):
        return(f'Error: File "{file_path}" not found.')
    if not file_path.endswith('.py'):
        return(f'Error: "{file_path}" is not a Python file.')
    try:
        cmd = [sys.executable, abs_target] + list(args)
        completed = subprocess.run(cmd, cwd=abs_working, capture_output=True, text=True, timeout=30)
        out = []
        if completed.stdout:
            out.append(f"STDOUT:{completed.stdout}")
        if completed.stderr:
            out.append(f"STDERR:{completed.stderr}")
        if completed.returncode != 0:
            out.append(f"Process exited with code {completed.returncode}")
        if not out:
            return "No output produced."
        return "\n".join(out).rstrip()

    except Exception as e:
        return(f"Error: executing Python file: {e}")

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python file listed within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path that will be used to locate the file.",
            ),
            "optional_args": types.Schema(
                type=types.Type.ARRAY,
                description="Execute Python files with optional arguments.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single argument to be passed to the Python script."
                ),
            ),
        },
        required=["file_path"]
    ),
)
