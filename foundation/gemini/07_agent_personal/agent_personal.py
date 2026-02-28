"""
Agent A: Personal Assistant

A simple agent with two real tools: a calculator and a clock.
Ask it things like:
  - "What is 234 * 567?"
  - "What time is it?"
  - "If I have 3 meetings of 45 minutes each, how many hours is that? And what time will it be when they're done?"
"""

from google import genai
from google.genai import types
from datetime import datetime

client = genai.Client()

SYSTEM_PROMPT = """You are a helpful personal assistant. You have access to a calculator and a clock.
Use the calculator for any math — never do arithmetic in your head.
Be concise and friendly."""


def calculator(expression: str) -> str:
    """Evaluate a mathematical expression. Supports +, -, *, /, **, parentheses, and common math."""
    pass


def get_time() -> str:
    """Get the current date, day of week, and time."""
    pass


def call_tool(name, args):
    if name == "calculator":
        try:
            allowed = set("0123456789+-*/.() ")
            expr = args["expression"]
            if all(c in allowed for c in expr):
                return str(eval(expr))
            else:
                return "Error: expression contains invalid characters"
        except Exception as e:
            return f"Error: {e}"
    elif name == "get_time":
        return datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S")
    return "Unknown tool"


config = types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT,
    tools=[calculator, get_time],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)


if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            break

        contents = [types.Content(role="user", parts=[types.Part.from_text(text=user_input)])]

        while True:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=contents,
                config=config,
            )

            model_content = response.candidates[0].content
            contents.append(model_content)

            function_calls = [part.function_call for part in model_content.parts if part.function_call]

            if function_calls:
                tool_response_parts = []
                for fc in function_calls:
                    result = call_tool(fc.name, dict(fc.args))
                    print(f"  [{fc.name}] {dict(fc.args)} → {result}")
                    tool_response_parts.append(
                        types.Part.from_function_response(name=fc.name, response={"output": result})
                    )
                contents.append(types.Content(role="user", parts=tool_response_parts))
            else:
                print(f"Assistant: {response.text}")
                break
