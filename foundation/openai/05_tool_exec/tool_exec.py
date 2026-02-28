import json
import openai

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
    }
]

messages = [{"role": "user", "content": "What is the weather in Tokyo?"}]

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages,
    tools=tools,
)

# Append the full assistant message (preserves tool_calls field)
messages.append(response.choices[0].message)

for tool_call in response.choices[0].message.tool_calls:
    args = json.loads(tool_call.function.arguments)
    print(f"Tool: {tool_call.function.name}({args})")

    # "Execute" the tool (hardcoded for now)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": "65 degrees",
        }
    )

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages,
    tools=tools,
)
print(response.choices[0].message.content)
