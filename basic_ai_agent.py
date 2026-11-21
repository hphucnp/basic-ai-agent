"""Ví dụ AI agent có một công cụ tra tồn kho giả lập."""

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
    """Tra số lượng trong dữ liệu mẫu."""
    stock = {"A101": 17, "B202": 0}
    return {"quantity": stock.get(product_code.strip().upper())}


# Schema cho model biết công cụ làm gì và cần tham số nào.
STOCK_TOOL = {
    "type": "function",
    "name": "check_stock",
    "description": "Tra tồn kho theo mã sản phẩm. null nghĩa là mã không tồn tại.",
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
        raise RuntimeError(f"Hãy đặt biến môi trường {key_env}.")

    client = OpenAI(api_key=api_key, base_url=config["base_url"])
    history = [{"role": "user", "content": question}]

    for _ in range(4):
        # 1. Model chọn trả lời hoặc gọi công cụ.
        response = client.responses.create(
            model=config["model"],
            instructions=(
                "Trả lời ngắn gọn bằng tiếng Việt. Nếu người dùng hỏi tồn kho "
                "và có mã sản phẩm, hãy tra bằng check_stock. Nếu thiếu mã, hãy hỏi lại."
            ),
            input=history,
            tools=[STOCK_TOOL],
            **config["request_options"],
        )
        history.extend(response.output)
        tool_calls = [item for item in response.output if item.type == "function_call"]
        if not tool_calls:
            return response.output_text or "Model chưa trả về câu trả lời."

        for tool_call in tool_calls:
            # 2. Python thực thi công cụ mà model yêu cầu.
            arguments = json.loads(tool_call.arguments)
            print(f"[Tool] {tool_call.name} {arguments}")
            result = check_stock(arguments["product_code"])
            print(f"[Kết quả tool] {result}")

            # 3. Gắn kết quả với đúng lần gọi tool và gửi lại ở vòng kế tiếp.
            history.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps(result),
            })

    return "Agent đã đạt giới hạn 4 lượt gọi model."


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--provider",
        choices=PROVIDERS,
        default=DEFAULT_PROVIDER,
        help="Nhà cung cấp model (mặc định: %(default)s).",
    )
    args = parser.parse_args()

    question = input("Bạn hỏi gì? ").strip()
    if question:
        print(run_agent(question, provider=args.provider))
