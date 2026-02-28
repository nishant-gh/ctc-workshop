"""
Agent C: Build Your Own Agent

This is a scaffold for you to build your own agent.
Fill in the three sections marked with TODO:
  1. SYSTEM_PROMPT — who is your agent?
  2. tools — what can it do?
  3. call_tool — how does each tool work?

Ideas:
  - A travel assistant (search flights, check visa requirements, convert currency)
  - A recipe helper (search recipes, convert units, set timers)
  - A study buddy (create flashcards, quiz the user, explain concepts)
  - A fitness coach (log workouts, calculate calories, suggest exercises)
  - A movie recommender (search movies, get ratings, check streaming availability)
"""

import anthropic

client = anthropic.Anthropic()

# ============================================================
# TODO 1: Define your agent's persona
# ============================================================
SYSTEM_PROMPT = """You are a helpful assistant.

Replace this with your agent's persona and guidelines.
"""

# ============================================================
# TODO 2: Define your tools
# ============================================================
tools = [
    # Example tool — replace with your own:
    {
        "name": "example_tool",
        "description": "Describe what this tool does so Claude knows when to use it",
        "input_schema": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Describe this parameter",
                }
            },
            "required": ["param1"],
        },
    },
    # Add more tools here...
]


# ============================================================
# TODO 3: Implement your tools
# ============================================================
def call_tool(name, input):
    if name == "example_tool":
        return f"You called example_tool with: {input}"
    # Add more tool implementations here...
    return "Unknown tool"


# ============================================================
# Agent loop (this part is already done for you!)
# ============================================================
if __name__ == "__main__":
    messages = []
    print("Your Custom Agent (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})

        while True:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=messages,
                tools=tools,
            )

            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = call_tool(block.name, block.input)
                    print(f"  [{block.name}] → {result}")
                    tool_results.append(
                        {"type": "tool_result", "tool_use_id": block.id, "content": result}
                    )
                elif block.type == "text" and response.stop_reason == "end_turn":
                    print(f"\nAgent: {block.text}\n")

            if tool_results:
                messages.append({"role": "user", "content": tool_results})
            else:
                break
