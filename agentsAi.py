import os
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

agent = Agent(
    name = 'Basic Agent',
    instructions = 'You are an expert AWS assistant who will give provide commands to create all types of services in AWS account',
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

    result = await Runner.run(agent,f'give single and correct command without any notes or suggestions to create EC2 with these configuration. Instance type is {instance_type}, AMI is {ami_id}, Region is {aws_region}. Also, breakup the command in python list format ["aws","ec2",..]')
    print(result.final_output)

    # convert the command to list using ast and then pass to function
    stdout, stderr = runCommand(ast.literal_eval(result.final_output)) 
    if stdout:
        print("\nEC2 Instances:")
        print(stdout)

# Entry point
if __name__ == "__main__":
    asyncio.run(main())