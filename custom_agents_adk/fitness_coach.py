"""
Fitness Coach Agent (using Google ADK)

An agent that helps users stay fit — log workouts, estimate calories, and suggest exercises.
One tool is complete as an example — implement the remaining two TODOs.

Run:  uv run python custom_agents_adk/fitness_coach.py
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


def log_workout(exercise: str, duration_minutes: int, sets: int, reps: int) -> dict:
    """Log a completed workout session.

    Args:
        exercise: Name of the exercise (e.g. "bench press", "running").
        duration_minutes: How long the workout lasted in minutes.
        sets: Number of sets completed.
        reps: Number of reps per set.

    Returns:
        dict: status and workout summary or error message.
    """
    return {
        "status": "success",
        "report": (
            f"Workout logged: {exercise} — {sets}x{reps} for {duration_minutes} min. "
            f"Great job! You've completed 3 workouts this week."
        ),
    }


def calculate_calories(exercise: str, duration_minutes: int, weight_kg: float) -> dict:
    """Estimate calories burned for a given exercise.

    Args:
        exercise: Name of the exercise (e.g. "running", "cycling", "swimming").
        duration_minutes: Duration of the exercise in minutes.
        weight_kg: User's body weight in kilograms.

    Returns:
        dict: status and calorie estimate or error message.
    """
    # TODO: implement — return a dict with "status" and "report" keys
    # Hint: use a simple formula like calories = duration * weight * factor
    pass


def suggest_exercise(muscle_group: str, equipment: str) -> dict:
    """Suggest exercises for a target muscle group and available equipment.

    Args:
        muscle_group: Target area (e.g. "chest", "legs", "back", "core").
        equipment: Available equipment (e.g. "dumbbells", "barbell", "bodyweight", "none").

    Returns:
        dict: status and exercise suggestions or error message.
    """
    # TODO: implement — return a dict with "status" and "report" keys
    # Hint: return 2-3 exercise suggestions with sets/reps recommendations
    pass


# ============================================================
# TODO 2: Define your agent
# ============================================================

agent = Agent(
    model="gemini-3-flash-preview",
    name="fitness_coach",
    # TODO: Write an instruction that gives the agent a motivating coach persona.
    # Hint: describe its coaching style, safety reminders, encouragement approach, etc.
    instruction="""You are a helpful fitness coach.

Replace this with your agent's persona and guidelines.
""",
    tools=[log_workout, calculate_calories, suggest_exercise],
)


# ============================================================
# Agent loop (this part is already done for you!)
# ============================================================

runner = InMemoryRunner(agent=agent, app_name="fitness_coach")
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
    print("Fitness Coach (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = asyncio.run(run(user_input))
        print(f"\nAgent: {result}\n")
