import os
import json
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
import subprocess
import ast

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key not found!")

ec2_specs = {
    "instance_type": "t2.micro",
    "ami_id": "ami-01b6d88af12965bb6",
    "aws_region": "ap-south-1"
}

generator_agent = Agent(
    name = 'AWS CLI Generator',
    instructions = 'You are an expert AWS assistant who will provide commands to create all types of services in AWS account',
    model = 'gpt-5-nano-2025-08-07'
)

validator_agent = Agent(
    name = 'AWS CLI Validator',
    instructions = (
        'You are a stric AWS CLI validator.'
        'Check if the provided command:'
        '1. Is valid AWS CLI syntax'
        '2. Matches EC2 run-instances use case'
        '3. Contains correct region, AMI format, instance type'
        '4. Is safe (no delete/terminate/modify commands)'
        'Respond ONLY in JSON format:'
        '{"cmd_valid": true/false, "reason": "explanation}'
    ),
    model = 'gpt-5-nano-2025-08-07'
)

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
    instance_type = ec2_specs["instance_type"]
    ami_id = ec2_specs["ami_id"]
    aws_region = ec2_specs["aws_region"]

    result = await Runner.run(generator_agent,f'give single and correct command without any notes or suggestions to create EC2 with these configuration. Instance type is {instance_type}, AMI is {ami_id}, Region is {aws_region}. Also, breakup the command in python list format ["aws","ec2",..]')
    command_str = result.final_output
    print('AWS CLI Command: ')
    print(command_str)

    val_result = await Runner.run(validator_agent,f'Validate this AWS CLI command: {command_str}')
    print('Validation Result:')
    print(val_result.final_output)
    data = json.loads(val_result.final_output)
    print(data['cmd_valid'])

    if data['cmd_valid']:
        # convert the command to list using ast and then pass to function
        stdout, stderr = runCommand(ast.literal_eval(result.final_output)) 
        if stdout:
            print("\nEC2 Instances:")
            print(stdout)
    else:
        print('Command not valid, cannot create resource')

# Entry point
if __name__ == "__main__":
    asyncio.run(main())