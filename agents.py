import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key not found!")

agent = Agent(
    name = 'Basic Agent',
    instructions = 'You are an expert AWS assistant who will give provide commands to create all types of services in AWS account',
    model = 'gpt-5-nano-2025-08-07'
)

result = await Runner.run(agent, 'give command to create EC2')
result.final_output