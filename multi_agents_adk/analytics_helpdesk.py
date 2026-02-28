"""
Multi-Agent Exercise: Build an Analytics Helpdesk (Coordinator + Specialists)

A coordinator agent routes user queries to specialist sub-agents:
  - SQL Agent: queries data tables
  - Data Quality Agent: checks for data issues

Fill in the TODOs below, then run:
  uv run python multi_agents_adk/analytics_helpdesk.py

Test queries:
  - "Show me all enterprise customers" → SQL agent
  - "Are there data quality issues in the events table?" → Data quality agent
  - "What metrics should I track for churn?" → Coordinator answers directly
"""

import asyncio

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

# --- Fake database ---

TABLES = {
    "customers": [
        {"id": 1, "name": "Acme Corp", "segment": "Enterprise", "mrr": 12000},
        {"id": 2, "name": "StartupXYZ", "segment": "SMB", "mrr": 500},
        {"id": 3, "name": "MegaRetail", "segment": "Enterprise", "mrr": 25000},
        {"id": 4, "name": "LocalShop", "segment": "SMB", "mrr": 200},
        {"id": 5, "name": "TechGiant", "segment": "Enterprise", "mrr": 45000},
    ],
    "events": [
        {"customer_id": 1, "event": "login", "count": 340, "month": "2024-12"},
        {"customer_id": 1, "event": "export", "count": 45, "month": "2024-12"},
        {"customer_id": 2, "event": "login", "count": 12, "month": "2024-12"},
        {"customer_id": 3, "event": "login", "count": 580, "month": "2024-12"},
        {"customer_id": 3, "event": "export", "count": 120, "month": "2024-12"},
        {"customer_id": 4, "event": "login", "count": 3, "month": "2024-12"},
        {"customer_id": 5, "event": "login", "count": 890, "month": "2024-12"},
        {"customer_id": 5, "event": "export", "count": 200, "month": "2024-12"},
    ],
}

# --- TODO 1: Define tools for the SQL Agent ---
# list_tables() — returns available table names
# run_query(table, filter_field, filter_value) — filters a table and returns matching rows


def list_tables() -> str:
    """List all available database tables."""
    # TODO: Return the table names from TABLES
    pass


def run_query(table: str, filter_field: str, filter_value: str) -> str:
    """Query a table with an optional filter. Returns matching rows.

    Args:
        table: Name of the table to query (e.g. 'customers')
        filter_field: Column to filter on (e.g. 'segment')
        filter_value: Value to match (e.g. 'Enterprise')
    """
    # TODO: Look up the table in TABLES, filter rows where row[filter_field] matches filter_value,
    #       and return the matching rows as a string. Handle missing tables gracefully.
    pass


# --- TODO 2: Define tools for the Data Quality Agent ---
# check_missing_values(table) — checks for None/empty values
# check_duplicates(table, field) — checks for repeated values in a field


def check_missing_values(table: str) -> str:
    """Check a table for missing or None values in any field. Returns a report of findings."""
    # TODO: Iterate through rows in TABLES[table], check each field for None or empty string,
    #       and return a summary (e.g. "No missing values" or "Row 2: field 'name' is missing")
    pass


def check_duplicates(table: str, field: str) -> str:
    """Check if any values in a specific field are duplicated.

    Args:
        table: Name of the table to check
        field: Column name to check for duplicates
    """
    # TODO: Collect all values for the given field, find duplicates, and return a report
    pass


# --- TODO 3: Create specialist sub-agents ---

sql_agent = Agent(
    model="gemini-3-flash-preview",
    name="sql_agent",
    # TODO: Write an instruction telling this agent it's a SQL specialist that helps
    #       analysts query data. It should list tables first, then run queries.
    instruction="""
    """,
    tools=[],  # TODO: Add your SQL tools here
)

data_quality_agent = Agent(
    model="gemini-3-flash-preview",
    name="data_quality_agent",
    # TODO: Write an instruction telling this agent it's a data quality specialist
    #       that checks for missing values and duplicates.
    instruction="""
    """,
    tools=[],  # TODO: Add your data quality tools here
)

# --- TODO 4: Create the coordinator agent ---

coordinator = Agent(
    model="gemini-3-flash-preview",
    name="analytics_helpdesk",
    # TODO: Write an instruction that tells the coordinator to:
    #       - Route data/query questions to sql_agent
    #       - Route quality/validation questions to data_quality_agent
    #       - Answer general analytics questions itself
    instruction="""
    """,
    sub_agents=[],  # TODO: Add your specialist agents here
)

# --- Runner (provided — no TODO) ---

runner = InMemoryRunner(agent=coordinator, app_name="analytics_helpdesk")
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
    print("Analytics Helpdesk (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = asyncio.run(run(user_input))
        print(f"\nHelpdesk: {result}\n")
