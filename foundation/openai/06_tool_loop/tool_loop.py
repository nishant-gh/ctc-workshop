import json
import openai
from datetime import datetime

client = openai.OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the current date and time",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
]

messages = [{"role": "user", "content": "What's the weather and current time in Tokyo?"}]


def call_tool(tool_name, tool_input):
    if tool_name == "get_weather":
        return f"72°F and sunny in {tool_input['location']}"
    elif tool_name == "get_time":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        return "Tool not found."


while True:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools=tools,
    )

    message = response.choices[0].message
    messages.append(message)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            tool_result = call_tool(tool_call.function.name, args)
            print(f"  Tool: {tool_call.function.name}({args}) → {tool_result}")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )
    else:
        print(message.content)
        break
