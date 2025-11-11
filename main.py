import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []

    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("ERROR: No prompt provided")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

    generate_content(client, messages, verbose)

    
def generate_content(client, messages, verbose):
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )
    
    if verbose:
        print(f"Prompt tokens:", response.usage_metadata.prompt_token_count)
        print(f"Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    calls = response.function_calls
    if calls:
        for fc in calls:
            #print(f"Calling function: {fc.name}({fc.args})")
            function_call_result = call_function(fc, verbose)

            try:
                response = function_call_result.parts[0].function_response.response
                if verbose:
                    print(f"-> {response}")
            except AttributeError:
                raise Exception("Function call result does not contain expected response structure")
    else:
        print(response.text)

def call_function(function_call_part, verbose=False):

    function_name = function_call_part.name
    function_args = function_call_part.args

    copied_args = function_args.copy()
    copied_args["working_directory"] = "./calculator"

    func_dict = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if verbose is True:
        print(f"Calling function: {function_name}({copied_args})")
    else:
        print(f" - Calling function: {function_name}")


    try:
        my_function = func_dict[function_name]
        function_result = my_function(**copied_args)

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
            ],
        )



if __name__ == "__main__":
    main()
