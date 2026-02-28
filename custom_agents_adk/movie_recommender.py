"""
Movie Recommender Agent (using Google ADK)

An agent that helps users find movies — search, ratings, and streaming availability.
One tool is complete as an example — implement the remaining two TODOs.

Run:  uv run python custom_agents_adk/movie_recommender.py
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


def search_movies(query: str, genre: str) -> dict:
    """Search for movies matching a query and genre.

    Args:
        query: Search keywords (e.g. "space adventure", "romantic comedy").
        genre: Movie genre filter (e.g. "sci-fi", "comedy", "drama", "horror").

    Returns:
        dict: status and matching movies or error message.
    """
    return {
        "status": "success",
        "report": (
            f"Found 3 {genre} movies matching '{query}': "
            f"1) Interstellar (2014) — 8.7/10. "
            f"2) The Martian (2015) — 8.0/10. "
            f"3) Arrival (2016) — 7.9/10."
        ),
    }


def get_movie_rating(title: str) -> dict:
    """Get ratings and review summary for a specific movie.

    Args:
        title: The movie title (e.g. "Inception").

    Returns:
        dict: status and rating details or error message.
    """
    # TODO: implement — return a dict with "status" and "report" keys
    # Hint: return hardcoded ratings from multiple sources (IMDb, Rotten Tomatoes, etc.)
    pass


def check_streaming(title: str, country: str) -> dict:
    """Check which streaming platforms have a movie available.

    Args:
        title: The movie title (e.g. "Inception").
        country: Country code for regional availability (e.g. "US", "UK").

    Returns:
        dict: status and streaming availability or error message.
    """
    # TODO: implement — return a dict with "status" and "report" keys
    # Hint: return a list of platforms where the movie is available (Netflix, Prime, etc.)
    pass


# ============================================================
# TODO 2: Define your agent
# ============================================================

agent = Agent(
    model="gemini-3-flash-preview",
    name="movie_recommender",
    # TODO: Write an instruction that gives the agent a film-enthusiast persona.
    # Hint: describe how it should recommend movies, handle preferences, spoiler policy, etc.
    instruction="""You are a helpful movie recommender.

Replace this with your agent's persona and guidelines.
""",
    tools=[search_movies, get_movie_rating, check_streaming],
)


# ============================================================
# Agent loop (this part is already done for you!)
# ============================================================

runner = InMemoryRunner(agent=agent, app_name="movie_recommender")
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
    print("Movie Recommender (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = asyncio.run(run(user_input))
        print(f"\nAgent: {result}\n")
