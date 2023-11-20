import os

import openai

client = openai.Client(
    api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE_URL")
)

MODEL = os.getenv("MODEL") or "gpt-3.5-turbo"


functions = [
    {
        "name": "",
        "description": "",
        "parameters": {
            "type": "object",
            "properties": {
                "pandas_python_commend": {
                    "type": "string",
                    "description": "The python code of execute from dataframe by use pandas framework",
                },
            },
            "required": ["pandas_python_commend"],
        },
    }
]


messages = [{"role": "user", "content": ""}]

response = client.chat.completions.create(
    model=MODEL,
    tools={
        "type": "function",  # Tools can be of types code_interpreter, retrieval, or function.
        "function": {
            "name": "",
            "description": "",
            "parameters": {
                "type": "object",
                "properties": {
                    "pandas_python_commend": {
                        "type": "string",
                        "description": "The python code of execute from dataframe by use pandas framework",
                    },
                },
                "required": ["pandas_python_commend"],
            },
        },
    },
    tool_choice="auto",
)
