import anthropic

client = anthropic.Anthropic()

messages = []

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append({"role": "user", "content": user_input})

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=messages,
    )

    messages.append({"role": "assistant", "content": message.content})
    print(f"\nAssistant: {message.content[0].text}")
