"""
Website Builder Agent (using Google ADK)

An agent that generates websites from descriptions with page generation, sections, and themes.
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


def generate_page(page_type: str, description: str) -> dict:
    """Generate a complete HTML page based on a page type and description.

    Args:
        page_type: The type of page to generate (e.g. "landing", "portfolio", "blog").
        description: A description of what the page should contain.

    Returns:
        dict: status and the generated HTML or error message.
    """
    html = (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"  <title>{page_type.title()} Page</title>\n"
        "  <style>\n"
        "    * { margin: 0; padding: 0; box-sizing: border-box; }\n"
        "    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }\n"
        "    .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }\n"
        "    header { background: #2c3e50; color: white; padding: 1rem 0; }\n"
        "    main { padding: 2rem 0; }\n"
        "    footer { background: #34495e; color: white; padding: 1rem 0; text-align: center; }\n"
        "  </style>\n"
        "</head>\n"
        "<body>\n"
        '  <header><div class="container"><h1>' + page_type.title() + " Page</h1></div></header>\n"
        '  <main><div class="container">\n'
        f"    <p>{description}</p>\n"
        "  </div></main>\n"
        '  <footer><div class="container"><p>&copy; 2025</p></div></footer>\n'
        "</body>\n"
        "</html>"
    )
    return {
        "status": "success",
        "report": f"Generated a {page_type} page. Here is the HTML:\n\n{html}",
    }


def add_section(section_type: str, content: str) -> dict:
    """Generate an HTML section to add to a page.

    Args:
        section_type: The type of section (e.g. "hero", "features", "testimonials", "contact").
        content: The text content for the section.

    Returns:
        dict: status and the generated HTML section or error message.
    """
    # TODO: implement — return a dict with "status" and "report" keys
    # Hint: return a hardcoded HTML snippet for the section_type, incorporating content
    # Example: a "hero" section might be a <section> with a heading, paragraph, and a CTA button
    pass


def apply_theme(html: str, theme: str) -> dict:
    """Apply a visual theme to an HTML page by injecting CSS styles.

    Args:
        html: The HTML string to apply the theme to.
        theme: The theme name (e.g. "modern", "minimal", "bold").

    Returns:
        dict: status and the themed HTML or error message.
    """
    # TODO: implement — return a dict with "status" and "report" keys
    # Hint: define a CSS string for each theme and inject it into the <head> of the HTML
    # Example: "modern" might use a gradient background and rounded corners
    pass


# ============================================================
# TODO 2: Define your agent
# ============================================================

agent = Agent(
    model="gemini-3-flash-preview",
    name="website_builder",
    # TODO: Write an instruction that gives the agent a web-developer persona.
    # Hint: describe what the agent can help with, its tone, and any guidelines.
    instruction="""You are a helpful website builder assistant.

Replace this with your agent's persona and guidelines.
""",
    tools=[generate_page, add_section, apply_theme],
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
