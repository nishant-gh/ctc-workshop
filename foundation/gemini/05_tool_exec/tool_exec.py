from google import genai
from google.genai import types

client = genai.Client()


def get_weather(location: str) -> str:
    """Get the current weather in a given location."""
    pass


config = types.GenerateContentConfig(
    tools=[get_weather],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

contents = [types.Content(role="user", parts=[types.Part.from_text(text="What is the weather in Tokyo?")])]

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=contents,
    config=config,
)

# Append the model's response (preserves the function_call)
contents.append(response.candidates[0].content)

for part in response.candidates[0].content.parts:
    if part.function_call:
        fc = part.function_call
        print(f"Tool: {fc.name}({fc.args})")

        # "Execute" the tool (hardcoded for now)
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_function_response(name=fc.name, response={"output": "65 degrees"})],
            )
        )

# Send the tool result back to the model
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=contents,
    config=config,
)
print(response.text)
