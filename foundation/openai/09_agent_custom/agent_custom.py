"""
Agent C: Build Your Own Agent (using OpenAI Agents SDK)

This is a scaffold for you to build your own agent.
Fill in the three sections marked with TODO:
  1. instructions — who is your agent?
  2. @function_tool functions — what can it do?
  3. Agent(...) assembly — wire it together

Ideas:
  - A travel assistant (search flights, check visa requirements, convert currency)
  - A recipe helper (search recipes, convert units, set timers)
  - A study buddy (create flashcards, quiz the user, explain concepts)
  - A fitness coach (log workouts, calculate calories, suggest exercises)
  - A movie recommender (search movies, get ratings, check streaming availability)
"""

from agents import Agent, Runner, function_tool

# ============================================================
# TODO 1: Define your tools as decorated functions
# The SDK infers the schema from type hints and docstrings.
# ============================================================


@function_tool
def example_tool(param1: str) -> str:
    """Describe what this tool does so the model knows when to use it."""
    return f"You called example_tool with: {param1}"


# Add more @function_tool functions here...


# ============================================================
# TODO 2: Define your agent
# ============================================================

agent = Agent(
    name="My Custom Agent",
    # TODO: Replace with your agent's persona and guidelines
    instructions="""You are a helpful assistant.

Replace this with your agent's persona and guidelines.
""",
    tools=[example_tool],  # TODO: Add your tools here
    model="gpt-4.1-mini",
)


# ============================================================
# Agent loop (this part is already done for you!)
# ============================================================
if __name__ == "__main__":
    print("Your Custom Agent (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = Runner.run_sync(agent, user_input)
        print(f"\nAgent: {result.final_output}\n")
