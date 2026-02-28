"""
Study Buddy Agent (using Google ADK)

An agent that helps students learn — flashcards, quizzes, and concept explanations.
One tool is complete as an example — implement the remaining two TODOs.

Run:  uv run python custom_agents_adk/study_buddy.py
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


def create_flashcard(topic: str, question: str, answer: str) -> dict:
    """Create a flashcard for studying.

    Args:
        topic: The subject area (e.g. "Biology", "History").
        question: The front of the flashcard.
        answer: The back of the flashcard.

    Returns:
        dict: status and confirmation or error message.
    """
    return {
        "status": "success",
        "report": (
            f"Flashcard created for {topic}! "
            f"Q: {question} | A: {answer}"
        ),
    }


def quiz_me(topic: str, difficulty: str) -> dict:
    """Generate a quiz question on a topic.

    Args:
        topic: The subject to quiz on (e.g. "Photosynthesis", "World War II").
        difficulty: Question difficulty — "easy", "medium", or "hard".

    Returns:
        dict: status and a quiz question with answer or error message.
    """
    # TODO: implement — return a dict with "status" and "report" keys
    # Hint: return a hardcoded question and answer for the given topic/difficulty
    pass


def explain_concept(concept: str, level: str) -> dict:
    """Explain a concept at a specified comprehension level.

    Args:
        concept: The concept to explain (e.g. "mitosis", "supply and demand").
        level: Target level — "beginner", "intermediate", or "advanced".

    Returns:
        dict: status and explanation or error message.
    """
    # TODO: implement — return a dict with "status" and "report" keys
    # Hint: return a short explanation tailored to the requested level
    pass


# ============================================================
# TODO 2: Define your agent
# ============================================================

agent = Agent(
    model="gemini-3-flash-preview",
    name="study_buddy",
    # TODO: Write an instruction that gives the agent an encouraging tutor persona.
    # Hint: describe how it should quiz students, when to give hints vs answers, etc.
    instruction="""You are a helpful study buddy.

Replace this with your agent's persona and guidelines.
""",
    tools=[create_flashcard, quiz_me, explain_concept],
)


# ============================================================
# Agent loop (this part is already done for you!)
# ============================================================

runner = InMemoryRunner(agent=agent, app_name="study_buddy")
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
    print("Study Buddy (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = asyncio.run(run(user_input))
        print(f"\nAgent: {result}\n")
