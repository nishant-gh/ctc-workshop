"""
Agent A: Personal Assistant

A simple agent with two real tools: a calculator and a clock.
Ask it things like:
  - "What is 234 * 567?"
  - "What time is it?"
  - "If I have 3 meetings of 45 minutes each, how many hours is that? And what time will it be when they're done?"
"""

import json
import openai
from datetime import datetime

client = openai.OpenAI()

SYSTEM_PROMPT = """You are a helpful personal assistant. You have access to a calculator and a clock.
Use the calculator for any math — never do arithmetic in your head.
Be concise and friendly."""

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a mathematical expression. Supports +, -, *, /, **, parentheses, and common math.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate, e.g. '(12 + 34) * 5'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the current date, day of week, and time",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
]


def call_tool(name, input):
    if name == "calculator":
        try:
            allowed = set("0123456789+-*/.() ")
            expr = input["expression"]
            if all(c in allowed for c in expr):
                return str(eval(expr))
            else:
                return "Error: expression contains invalid characters"
        except Exception as e:
            return f"Error: {e}"
    elif name == "get_time":
        return datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S")
    return "Unknown tool"


def run_agent(user_message):
    print(f"\nYou: {user_message}")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

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
                result = call_tool(tool_call.function.name, args)
                print(f"  [{tool_call.function.name}] {args} → {result}")
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )
        else:
            print(f"Assistant: {message.content}")
            break


if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            break
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ]

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
                    result = call_tool(tool_call.function.name, args)
                    print(f"  [{tool_call.function.name}] {args} → {result}")
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result,
                        }
                    )
            else:
                print(f"Assistant: {message.content}")
                break
