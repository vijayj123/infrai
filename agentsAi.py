import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key not found!")

ec2_specs = {
    "instance_type": "t2.micro",
    "ami_id": "ami-01b6d88af12965bb6"
}

agent = Agent(
    name = 'Basic Agent',
    instructions = 'You are an expert AWS assistant who will give provide commands to create all types of services in AWS account',
    model = 'gpt-5-nano-2025-08-07'
)

async def main():
    instance_type = ec2_specs["instance_type"]
    ami_id = ec2_specs["ami_id"]

    result = await Runner.run(agent,f'give single and correct command without any notes or suggestions to create EC2 with these configuration. Instance type is {instance_type}, AMI is {ami_id}')
    print(result.final_output)

# Entry point
if __name__ == "__main__":
    asyncio.run(main())