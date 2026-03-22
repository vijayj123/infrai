import os
import json
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
import subprocess
import ast
import base64

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

# Validate the Open AI subscription.
if not api_key:
    raise ValueError("API key not found!")

# Get path of file standardspec.txt.
FILEPATH = os.path.join(os.path.dirname(__file__), "standardspec.txt")

# Return a base64 encoded value for the standardspec.txt file.
def file_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# This is the AWS CLI command validator agent.  It will validated if the generated AWS CLI command is valid or not.
validator_agent = Agent(
    name = 'AWS CLI Validator',
    instructions = (
        'You are a strict.. AWS CLI validator.'
        'Check if the provided command is valid AWS CLI syntax.'
        'Respond ONLY in JSON format:'
        '{"cmd_valid": true/false, "reason": "explanation}'
    ),
    model = 'gpt-5-nano-2025-08-07'
)

# This is agent to classify if the given user input is to create EC2 or S3 resource.
# Currently we will only create these two resouces.
classifier_agent = Agent(
    name = 'AWS Intent Classifier',
    instructions = (
        'Classify the AWS service from user input.'
        'Supported services: ec2, s3'
        'Return ONLY JSON:'
        '{"service: "ec2|s3|unknown"}'
    ),
    model = 'gpt-5-nano-2025-08-07'
)

# This agent will actually create the AWS CLI command.  Based on the user input it will return the 
# correct command.  It will also refer the standardspec.txt file for help create the command.
async def extract_command(service, user_input):
    extractor_agent = Agent(
        name = f"{service.upper()} Parameter Extractor",
        instructions=(
            f"You are an AWS {service} assistant.\n\n"

            "Follow STRICT priority order:\n"
            "1. ALWAYS use user-provided values if present\n"
            "2. ONLY use file values when user has NOT provided that parameter\n"
            "3. NEVER override a user-provided value with file defaults\n\n"

            "Rules:\n"
            "- Extract parameters from user input\n"
            "- Fill missing parameters from the file\n"
            "- Generate a single AWS CLI command\n"
            "- Output ONLY python list format like:\n"
            '  ["aws","ec2","run-instances",...]\n'
            "- No explanations, no extra text\n"),

        model = 'gpt-5-nano-2025-08-07'
    )

    b64_file = file_to_base64(FILEPATH)
    result = await Runner.run(
        extractor_agent,
        [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "file_data": f"data:text/plain;base64,{b64_file}",
                        "filename": "standardspec.txt",
                    }
                ],
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
    )
    return result.final_output

# This function will run the AWS CLI command to create the actual AWS resouces.
def runCommand(cmmnd):
    try:
        process = subprocess.Popen(cmmnd, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE, 
                                   text=True) # Use text=True for string output
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print(f"Error executing command: {' '.join(cmmnd)}")
            print(f"Stderr: {stderr}")
            return None, stderr
        else:
            return stdout, None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, str(e)


async def main():
    # Get the user input, example: "create ec2 with t2.large instance type"
    user_input = input('Enter the details: ')

    # Classify the user_input as ec2 or s3
    classifier_result = await Runner.run(classifier_agent,f'{user_input}')
    print(classifier_result.final_output)
    service = json.loads(classifier_result.final_output)

    # Keep generating the command until it is valicated true
    while True:
        # Generate the command
        print('Generating command: ')
        command_str = await extract_command(service['service'], user_input)
        print(command_str)

        # Validate the command
        val_result = await Runner.run(validator_agent,f'Validate this AWS CLI command: {command_str}')
        print('Validation Result:')
        print(val_result.final_output)
        data = json.loads(val_result.final_output)
        # print(data['cmd_valid'])
        if data['cmd_valid']:
            break
    
    # Run the AWS CLI command to create the resource
    if data['cmd_valid']:
        # convert the command to list using ast and then pass to function
        stdout, stderr = runCommand(ast.literal_eval(command_str)) 
        if stdout:
            print(stdout)
    else:
        print('Command not valid, cannot create resource')

# Entry point
if __name__ == "__main__":
    asyncio.run(main())