import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import tools, tool_registry

load_dotenv()

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

MAX_STEPS = 10

SYSTEM_PROMPT = """
You are an e-commerce customer support agent.
Use available tools to retrieve accurate information.
Never invent order, inventory, or shipment information.
"""

def run_agent(question: str) -> str:
    history = [
        {"role": "user", "content": question}
    ]
    
    for step in range(MAX_STEPS):
        response = client.responses.create(
            model="deepseek-flash",
            instructions=SYSTEM_PROMPT,
            input=history,
            tools=tools,
            reasoning={"effort": "none"},
        )

        history.extend(response.output)

        function_calls = [item for item in response.output if item.type == "function_call"]
        if not function_calls:
            return response.output_text
        
        for call in function_calls:
            arguments = json.loads(call.arguments)
            tool_function = tool_registry.get(call.name)
            if tool_function is None:
                result = {"error": f"Tool {call.name} not found"}
            else:
                print(
                    f"Step {step + 1}: "
                    f"{call.name}({arguments})"
                )
                result = tool_function(**arguments)
                history.append({
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(result)
                })
    return "Please contact a customer support specialist."