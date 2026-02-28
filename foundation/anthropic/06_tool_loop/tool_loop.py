import anthropic
from datetime import datetime

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
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
    {
        "name": "get_time",
        "description": "Get the current date and time",
        "input_schema": {
            "type": "object",
            "properties": {},
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
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=messages,
        tools=tools,
    )

    messages.append(
        {
            "role": "assistant",
            "content": message.content,
        }
    )

    user_message = {"role": "user", "content": []}

    has_tool_use = False

    for content in message.content:
        if content.type == "tool_use":
            has_tool_use = True
            tool_result = call_tool(content.name, content.input)
            print(f"  Tool: {content.name}({content.input}) → {tool_result}")
            user_message["content"].append(
                {
                    "type": "tool_result",
                    "tool_use_id": content.id,
                    "content": tool_result,
                }
            )
        elif content.type == "text":
            print(content.text)

    if has_tool_use:
        messages.append(user_message)
    else:
        break
