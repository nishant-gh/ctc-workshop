"""
Travel Assistant Agent (using Google ADK)

An agent that helps users plan trips with flights, visa info, and currency conversion.
One tool is complete as an example — implement the remaining two TODOs.

Run:  uv run python custom_agents_adk/travel_assistant.py
"""

import asyncio

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

# ============================================================
# TODO 1: Define your tools
# ADK infers the schema from type hints and docstrings.
# The first tool is done for you — implement the other two.
# ============================================================


def search_flights(origin: str, destination: str, date: str) -> dict:
    """Search for available flights between two cities on a given date.

    Args:
        origin: Departure city (e.g. "New York").
        destination: Arrival city (e.g. "London").
        date: Travel date in YYYY-MM-DD format.

    Returns:
        dict: status and flight options or error message.
    """
    return {
        "status": "success",
        "report": (
            f"Found 3 flights from {origin} to {destination} on {date}: "
            f"1) Departure 08:00, Arrival 20:00, $450 economy. "
            f"2) Departure 14:30, Arrival 02:30+1, $380 economy. "
            f"3) Departure 22:00, Arrival 10:00+1, $820 business."
        ),
    }


def check_visa_requirements(passport_country: str, destination_country: str) -> dict:
    """Check visa requirements for traveling to a destination country.

    Args:
        passport_country: The traveler's passport country (e.g. "United States").
        destination_country: The country they want to visit (e.g. "Japan").

    Returns:
        dict: status and visa requirement details or error message.
    """
    # TODO: implement — return a dict with "status" and "report" keys
    # Hint: return hardcoded info like visa-free duration, visa type needed, etc.
    pass


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convert an amount from one currency to another.

    Args:
        amount: The amount of money to convert.
        from_currency: Source currency code (e.g. "USD").
        to_currency: Target currency code (e.g. "EUR").

    Returns:
        dict: status and conversion result or error message.
    """
    # TODO: implement — return a dict with "status" and "report" keys
    # Hint: use a hardcoded exchange rate and calculate the converted amount
    pass


# ============================================================
# TODO 2: Define your agent
# ============================================================

agent = Agent(
    model="gemini-3-flash-preview",
    name="travel_assistant",
    # TODO: Write an instruction that gives the agent a travel-advisor persona.
    # Hint: describe what the agent can help with, its tone, and any guidelines.
    instruction="""You are a helpful travel assistant.

Replace this with your agent's persona and guidelines.
""",
    tools=[search_flights, check_visa_requirements, convert_currency],
)


# ============================================================
# Agent loop (this part is already done for you!)
# ============================================================

runner = InMemoryRunner(agent=agent, app_name="travel_assistant")
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
    print("Travel Assistant (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = asyncio.run(run(user_input))
        print(f"\nAgent: {result}\n")
