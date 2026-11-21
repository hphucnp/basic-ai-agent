"""Example AI agent with a mock stock lookup tool."""

import argparse
import json
import os

from openai import OpenAI


DEFAULT_PROVIDER = "deepseek"
PROVIDERS = {
    "deepseek": {
        "base_url": "https://api.deepseek.com",
        "key_env": "DEEPSEEK_API_KEY",
        "model": "deepseek-flash",
        "request_options": {"reasoning": {"effort": "none"}},
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "key_env": "OPENAI_API_KEY",
        "model": "gpt-5.4-mini",
        "request_options": {"parallel_tool_calls": False},
    },
}


def check_stock(product_code):
    """Look up the quantity in the sample data."""
    stock = {"A101": 17, "B202": 0}
    return {"quantity": stock.get(product_code.strip().upper())}


# The tool schema tells the model what the tool does and which arguments it needs.
STOCK_TOOL = {
    "type": "function",
    "name": "check_stock",
    "description": "Look up stock by product code. A null quantity means the code was not found.",
    "parameters": {
        "type": "object",
        "properties": {"product_code": {"type": "string"}},
        "required": ["product_code"],
        "additionalProperties": False,
    },
    "strict": True,
}


def run_agent(question, provider=DEFAULT_PROVIDER):
    config = PROVIDERS[provider]
    key_env = config["key_env"]
    api_key = os.getenv(key_env)
    if not api_key:
        raise RuntimeError(f"Set the {key_env} environment variable.")

    client = OpenAI(api_key=api_key, base_url=config["base_url"])
    history = [{"role": "user", "content": question}]

    for _ in range(4):
        # 1. The model decides whether to answer or call the tool.
        response = client.responses.create(
            model=config["model"],
            instructions=(
                "Answer briefly in English. If the user asks about stock "
                "and provides a product code, use check_stock. If the code is missing, ask for it."
            ),
            input=history,
            tools=[STOCK_TOOL],
            **config["request_options"],
        )
        history.extend(response.output)
        tool_calls = [item for item in response.output if item.type == "function_call"]
        if not tool_calls:
            return response.output_text or "The model returned no answer."

        for tool_call in tool_calls:
            # 2. Python runs the tool requested by the model.
            arguments = json.loads(tool_call.arguments)
            print(f"[Tool] {tool_call.name} {arguments}")
            result = check_stock(arguments["product_code"])
            print(f"[Tool result] {result}")

            # 3. Match the result to its tool call and send it back on the next turn.
            history.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps(result),
            })

    return "The agent reached its limit of four model calls."


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--provider",
        choices=PROVIDERS,
        default=DEFAULT_PROVIDER,
        help="Model provider (default is %(default)s).",
    )
    args = parser.parse_args()

    question = input("What would you like to ask? ").strip()
    if question:
        print(run_agent(question, provider=args.provider))
