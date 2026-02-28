"""
Recipe Helper Agent (using Google ADK)

An agent that helps users cook — find recipes, convert units, and suggest substitutions.
One tool is complete as an example — implement the remaining two TODOs.

Run:  uv run python custom_agents_adk/recipe_helper.py
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


def search_recipes(ingredients: str) -> dict:
    """Search for recipes that can be made with the given ingredients.

    Args:
        ingredients: Comma-separated list of ingredients (e.g. "chicken, rice, garlic").

    Returns:
        dict: status and matching recipes or error message.
    """
    return {
        "status": "success",
        "report": (
            f"Found 3 recipes using {ingredients}: "
            f"1) Garlic Chicken Stir-Fry (30 min, easy). "
            f"2) Chicken Fried Rice (25 min, easy). "
            f"3) One-Pot Chicken & Rice (45 min, medium)."
        ),
    }


def convert_units(amount: float, from_unit: str, to_unit: str) -> dict:
    """Convert between cooking measurement units.

    Args:
        amount: The quantity to convert.
        from_unit: Source unit (e.g. "cups", "tablespoons", "grams").
        to_unit: Target unit (e.g. "ml", "teaspoons", "ounces").

    Returns:
        dict: status and converted measurement or error message.
    """
    # TODO: implement — return a dict with "status" and "report" keys
    # Hint: use hardcoded conversion factors (e.g. 1 cup = 236.6 ml)
    pass


def suggest_substitution(ingredient: str, reason: str) -> dict:
    """Suggest a substitution for an ingredient.

    Args:
        ingredient: The ingredient to replace (e.g. "butter").
        reason: Why a substitution is needed (e.g. "vegan", "allergy", "out of stock").

    Returns:
        dict: status and substitution suggestions or error message.
    """
    # TODO: implement — return a dict with "status" and "report" keys
    # Hint: return 1-2 substitution options with usage notes
    pass


# ============================================================
# TODO 2: Define your agent
# ============================================================

agent = Agent(
    model="gemini-3-flash-preview",
    name="recipe_helper",
    # TODO: Write an instruction that gives the agent a friendly chef persona.
    # Hint: describe what the agent can help with, dietary awareness, tone, etc.
    instruction="""You are a helpful recipe assistant.

Replace this with your agent's persona and guidelines.
""",
    tools=[search_recipes, convert_units, suggest_substitution],
)


# ============================================================
# Agent loop (this part is already done for you!)
# ============================================================

runner = InMemoryRunner(agent=agent, app_name="recipe_helper")
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
    print("Recipe Helper (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = asyncio.run(run(user_input))
        print(f"\nAgent: {result}\n")
