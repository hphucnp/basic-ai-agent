# Basic AI Agent

A small Python agent that answers questions in English and can call a local `check_stock` function to look up sample inventory. It supports DeepSeek and OpenAI through the same Python SDK.

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then clone the repo and install the locked dependencies. The project requires Python 3.10 or later.

```sh
git clone https://github.com/hphucnp/basic-ai-agent.git
cd basic-ai-agent
uv sync --locked
```

Get an API key for the provider you want to use. Create a `.env` file in the project directory and add the matching line below with your actual key. Git ignores this file.

```dotenv
DEEPSEEK_API_KEY=your_deepseek_key_here
OPENAI_API_KEY=your_openai_key_here
```

| Provider | Model | API key variable |
| --- | --- | --- |
| DeepSeek (default) | `deepseek-flash` | `DEEPSEEK_API_KEY` |
| OpenAI | `gpt-5.4-mini` | `OPENAI_API_KEY` |

## Run the agent

Run one of these commands from the project directory.

```sh
uv run --env-file .env basic_ai_agent.py --provider deepseek
uv run --env-file .env basic_ai_agent.py --provider openai
```

If you already exported your API key in the shell, omit `--env-file .env`. Use `uv run basic_ai_agent.py --help` to list the CLI options.

At the prompt, enter `How many units of A101 are in stock?` The sample data contains 17 units of `A101` and zero units of `B202`. An unknown product code returns a null quantity.

## How it works

1. The agent sends your question and the `check_stock` tool definition to the selected model.
2. If the model requests a lookup, Python runs `check_stock` against the sample inventory and sends the result back to the model.
3. The model uses the result to answer. The script handles one question per run and allows up to four model calls.

The agent code is in [`basic_ai_agent.py`](basic_ai_agent.py). You can edit the sample inventory in `check_stock` and the model and endpoint for each provider in `PROVIDERS`.
