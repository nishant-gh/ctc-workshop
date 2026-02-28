import openai

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "Hello!"}],
)

print(response.choices[0].message.content)
