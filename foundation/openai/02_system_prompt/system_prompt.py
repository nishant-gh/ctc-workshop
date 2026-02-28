import openai

client = openai.OpenAI()

# Without a system prompt
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "What should I cook for dinner?"}],
)
print("Without system prompt:")
print(response.choices[0].message.content)

print("\n" + "=" * 50 + "\n")

# With a system prompt
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a grumpy Italian chef. You are passionate about authentic Italian cuisine and get annoyed when people suggest non-Italian food. Keep responses short and funny."},
        {"role": "user", "content": "What should I cook for dinner?"},
    ],
)
print("With system prompt:")
print(response.choices[0].message.content)
