from google import genai

client = genai.Client()

chat = client.chats.create(model="gemini-3-flash-preview")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = chat.send_message(user_input)
    print(f"\nAssistant: {response.text}")
