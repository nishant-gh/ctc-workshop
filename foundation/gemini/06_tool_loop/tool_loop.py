from google import genai
from google.genai import types
from datetime import datetime

client = genai.Client()


def get_weather(location: str) -> str:
    """Get the current weather in a given location."""
    pass


def get_time() -> str:
    """Get the current date and time."""
    pass


def call_tool(tool_name, tool_input):
    if tool_name == "get_weather":
        return f"72°F and sunny in {tool_input['location']}"
    elif tool_name == "get_time":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        return "Tool not found."


config = types.GenerateContentConfig(
    tools=[get_weather, get_time],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

contents = [types.Content(role="user", parts=[types.Part.from_text(text="What's the weather and current time in Tokyo?")])]

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
            tool_result = call_tool(fc.name, dict(fc.args))
            print(f"  Tool: {fc.name}({dict(fc.args)}) → {tool_result}")
            tool_response_parts.append(
                types.Part.from_function_response(name=fc.name, response={"output": tool_result})
            )
        contents.append(types.Content(role="user", parts=tool_response_parts))
    else:
        print(response.text)
        break
