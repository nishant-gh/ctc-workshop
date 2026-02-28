"""
Agent A: Personal Assistant

A simple agent with two real tools: a calculator and a clock.
Ask it things like:
  - "What is 234 * 567?"
  - "What time is it?"
  - "If I have 3 meetings of 45 minutes each, how many hours is that? And what time will it be when they're done?"
"""

import anthropic
from datetime import datetime

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a helpful personal assistant. You have access to a calculator and a clock.
Use the calculator for any math — never do arithmetic in your head.
Be concise and friendly."""

tools = [
    {
        "name": "calculator",
        "description": "Evaluate a mathematical expression. Supports +, -, *, /, **, parentheses, and common math.",
        "input_schema": {
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
    {
        "name": "get_time",
        "description": "Get the current date, day of week, and time",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
]


def call_tool(name, input):
    if name == "calculator":
        try:
            # Only allow safe math operations
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
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages,
            tools=tools,
        )

        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = call_tool(block.name, block.input)
                print(f"  [{block.name}] {block.input} → {result}")
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    }
                )
            elif block.type == "text" and response.stop_reason == "end_turn":
                print(f"Assistant: {block.text}")

        if tool_results:
            messages.append({"role": "user", "content": tool_results})
        else:
            break


if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            break
        messages = [{"role": "user", "content": user_input}]

        while True:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=messages,
                tools=tools,
            )

            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = call_tool(block.name, block.input)
                    print(f"  [{block.name}] {block.input} → {result}")
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        }
                    )
                elif block.type == "text" and response.stop_reason == "end_turn":
                    print(f"Assistant: {block.text}")

            if tool_results:
                messages.append({"role": "user", "content": tool_results})
            else:
                break
