from google import genai
from google.genai import types

client = genai.Client()

# Without a system prompt
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What should I cook for dinner?",
)
print("Without system prompt:")
print(response.text)

print("\n" + "=" * 50 + "\n")

# With a system prompt
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What should I cook for dinner?",
    config=types.GenerateContentConfig(
        system_instruction="You are a grumpy Italian chef. You are passionate about authentic Italian cuisine and get annoyed when people suggest non-Italian food. Keep responses short and funny."
    ),
)
print("With system prompt:")
print(response.text)
