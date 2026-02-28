"""
Website Builder Agent (using Google ADK)

An agent that helps plan websites with layout, color schemes, and content suggestions.
One tool is complete as an example — implement the remaining two TODOs.

Run:  uv run python custom_agents_adk/website_builder.py
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


def generate_layout(page_type: str, description: str) -> dict:
    """Plan the layout and sections for a website page.

    Args:
        page_type: The type of page (e.g. "landing", "portfolio", "blog", "restaurant").
        description: What the page is for and any specific requirements.

    Returns:
        dict: status and a layout plan describing the page sections.
    """
    return {
        "status": "success",
        "report": (
            f"Layout plan for a {page_type} page:\n"
            f"1. Navigation bar — logo on the left, menu links on the right\n"
            f"2. Hero section — large headline, subtitle, and a call-to-action button\n"
            f"3. Features/services section — 3-column grid highlighting key offerings\n"
            f"4. Testimonials section — customer quotes in a carousel\n"
            f"5. Contact section — address, phone, email, and a simple form\n"
            f"6. Footer — social media links, copyright notice\n\n"
            f"Design notes based on description: {description}"
        ),
    }


def suggest_color_scheme(style: str, industry: str) -> dict:
    """Suggest a color palette for a website based on the desired style and industry.

    Args:
        style: The visual style (e.g. "professional", "playful", "dark", "minimal", "bold").
        industry: The business type (e.g. "restaurant", "tech startup", "law firm", "photography").

    Returns:
        dict: status and a recommended color palette.
    """
    # TODO: implement — return a dict with "status" and "report" keys
    # Hint: return a hardcoded color palette as plain text, e.g.:
    #   "Primary: deep navy (#1a2b4a), Accent: warm gold (#d4a843),
    #    Background: off-white (#f9f6f0), Text: charcoal (#2d2d2d)"
    # You can vary the palette based on style or industry if you want!
    pass


def suggest_content(section_type: str, business_name: str) -> dict:
    """Generate suggested copywriting text for a website section.

    Args:
        section_type: The section to write for (e.g. "hero", "about", "testimonials", "call_to_action").
        business_name: The name of the business the website is for.

    Returns:
        dict: status and suggested text content for the section.
    """
    # TODO: implement — return a dict with "status" and "report" keys
    # Hint: return hardcoded marketing copy, e.g. for a "hero" section:
    #   "Headline: Welcome to {business_name}
    #    Subtitle: We bring your ideas to life.
    #    Button text: Get Started"
    pass


# ============================================================
# TODO 2: Define your agent
# ============================================================

agent = Agent(
    model="gemini-3-flash-preview",
    name="website_builder",
    # TODO: Write an instruction that gives the agent a web-designer persona.
    # Hint: describe what the agent can help with, its tone, and any guidelines.
    instruction="""You are a helpful website planning assistant.

Replace this with your agent's persona and guidelines.
""",
    tools=[generate_layout, suggest_color_scheme, suggest_content],
)


# ============================================================
# Agent loop (this part is already done for you!)
# ============================================================

runner = InMemoryRunner(agent=agent, app_name="website_builder")
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
    print("Website Builder (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = asyncio.run(run(user_input))
        print(f"\nAgent: {result}\n")
