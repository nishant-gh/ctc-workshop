import anthropic

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
    }
]

messages = [{"role": "user", "content": "What is the weather in Tokyo?"}]

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

for content in message.content:
    if content.type == "tool_use":
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": content.id,  # from the API response
                        "content": "65 degrees",  # from running your tool
                    }
                ],
            }
        )
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=messages,
            tools=tools,
        )
        print(message.content[0].text)
    elif content.type == "text":
        print(content.text)
