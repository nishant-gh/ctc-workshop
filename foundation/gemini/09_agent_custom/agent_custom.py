"""
Agent C: Build Your Own Agent (using Google ADK)

This is a scaffold for you to build your own agent.
Fill in the three sections marked with TODO:
  1. instruction — who is your agent?
  2. tool functions — what can it do?
  3. Agent(...) assembly — wire it together

Ideas:
  - A travel assistant (search flights, check visa requirements, convert currency)
  - A recipe helper (search recipes, convert units, set timers)
  - A study buddy (create flashcards, quiz the user, explain concepts)
  - A fitness coach (log workouts, calculate calories, suggest exercises)
  - A movie recommender (search movies, get ratings, check streaming availability)
"""

import asyncio

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

# ============================================================
# TODO 1: Define your tools as plain functions
# ADK infers the schema from type hints and docstrings.
# ============================================================


def example_tool(param1: str) -> str:
    """Describe what this tool does so the model knows when to use it."""
    return f"You called example_tool with: {param1}"


# Add more tool functions here...


# ============================================================
# TODO 2: Define your agent
# ============================================================

agent = Agent(
    model="gemini-3-flash-preview",
    name="my_custom_agent",
    # TODO: Replace with your agent's persona and guidelines
    instruction="""You are a helpful assistant.

Replace this with your agent's persona and guidelines.
""",
    tools=[example_tool],  # TODO: Add your tools here
)


# ============================================================
# Agent loop (this part is already done for you!)
# ============================================================


runner = InMemoryRunner(agent=agent, app_name="my_custom_agent")
runner.auto_create_session = True


async def run(user_message: str, session_id: str = "session1"):
    user_content = types.Content(role="user", parts=[types.Part.from_text(text=user_message)])
    final_text = ""
    async for event in runner.run_async(user_id="user1", session_id=session_id, new_message=user_content):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    final_text = part.text
    return final_text


if __name__ == "__main__":
    print("Your Custom Agent (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = asyncio.run(run(user_input))
        print(f"\nAgent: {result}\n")
