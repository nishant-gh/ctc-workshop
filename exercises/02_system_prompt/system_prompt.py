import anthropic

client = anthropic.Anthropic()

# Without a system prompt
message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[{"role": "user", "content": "What should I cook for dinner?"}],
)
print("Without system prompt:")
print(message.content[0].text)

print("\n" + "=" * 50 + "\n")

# With a system prompt
message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    system="You are a grumpy Italian chef. You are passionate about authentic Italian cuisine and get annoyed when people suggest non-Italian food. Keep responses short and funny.",
    messages=[{"role": "user", "content": "What should I cook for dinner?"}],
)
print("With system prompt:")
print(message.content[0].text)
