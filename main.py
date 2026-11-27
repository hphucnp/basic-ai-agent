import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import check_inventory, tools

load_dotenv()

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

# response = client.responses.create(
#     model="deepseek-flash",
#     input="What is an AI agent?",
#     reasoning={"effort": "none"},
# )

response = client.responses.create(
    model="deepseek-flash",
    instructions="You are an e-commerce customer support agent.",
    input="Is the iPhone 16 Pro in stock?",
    tools=tools,
    reasoning={"effort": "none"},
)


for item in response.output:
    if item.type == "function_call":
        arguments = json.loads(item.arguments)

        if item.name == "check_inventory":
            result = check_inventory(**arguments)

            print(result)