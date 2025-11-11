import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, message):
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.join(abs_working, file_path)
    allowed = abs_target.startswith(abs_working + os.sep) or (abs_target == abs_working)

    if not allowed:
        return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')

    try:
        parent = os.path.dirname(abs_target)
        os.makedirs(parent, exist_ok=True)

        with open(abs_target, "w") as f:
            f.write(message)
        
        return(f'Successfully wrote to "{file_path}" ({len(message)} characters written)')

    except Exception as e:
        return(f'Error: {e}')

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the included message to the specified file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that will be written to, relative to the working directory.",
            ),
            "message": types.Schema(
                type=types.Type.STRING,
                description="The string to that will be written.",
            )
        },
        required =["file_path","message"]
    ),
)
