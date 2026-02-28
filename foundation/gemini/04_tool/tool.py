from google import genai
from google.genai import types

client = genai.Client()


def get_weather(location: str) -> str:
    """Get the current weather in a given location."""
    pass


response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What is the weather in Tokyo?",
    config=types.GenerateContentConfig(
        tools=[get_weather],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    ),
)

for part in response.candidates[0].content.parts:
    if part.function_call:
        fc = part.function_call
        print(f"Tool: {fc.name}")
        print(f"  Arguments: {fc.args}")
