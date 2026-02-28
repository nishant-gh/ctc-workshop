"""
Multi-Agent Example: Analytics Report Generator (Sequential Pipeline)

A 3-stage pipeline using SequentialAgent:
  DataFetcher → Analyzer → ReportWriter

Each agent writes to shared state via output_key, and the next agent reads it.

Try:
  - "Generate a quarterly analytics report"
  - "What were Q4 results?"
"""

import asyncio

from google.adk.agents import Agent, SequentialAgent
from google.adk.runners import InMemoryRunner
from google.genai import types

# --- Fake sales data ---

SALES_DATA = {
    "2024-Q3": [
        {"product": "Widget A", "units": 1200, "revenue": 36000},
        {"product": "Widget B", "units": 800, "revenue": 48000},
        {"product": "Gadget X", "units": 450, "revenue": 67500},
        {"product": "Gadget Y", "units": 300, "revenue": 27000},
    ],
    "2024-Q4": [
        {"product": "Widget A", "units": 1400, "revenue": 42000},
        {"product": "Widget B", "units": 950, "revenue": 57000},
        {"product": "Gadget X", "units": 520, "revenue": 78000},
        {"product": "Gadget Y", "units": 280, "revenue": 25200},
    ],
}

# --- DataFetcher tools ---


def get_sales_data(quarter: str) -> str:
    """Fetch sales data for a given quarter (e.g. '2024-Q3'). Returns a list of product sales records."""
    data = SALES_DATA.get(quarter)
    if data:
        return str(data)
    return f"No data found for {quarter}. Available quarters: {list(SALES_DATA.keys())}"


def list_available_quarters() -> str:
    """List all quarters that have sales data available."""
    return str(list(SALES_DATA.keys()))


# --- Analyzer tools ---


def compute_growth(current_quarter: str, previous_quarter: str) -> str:
    """Compute revenue growth rate between two quarters. Returns per-product and total growth."""
    curr = SALES_DATA.get(current_quarter)
    prev = SALES_DATA.get(previous_quarter)
    if not curr or not prev:
        return "One or both quarters not found."
    prev_map = {r["product"]: r["revenue"] for r in prev}
    results = []
    for r in curr:
        old = prev_map.get(r["product"], 0)
        growth = ((r["revenue"] - old) / old * 100) if old else 0
        results.append(f"{r['product']}: ${old:,} → ${r['revenue']:,} ({growth:+.1f}%)")
    total_prev = sum(r["revenue"] for r in prev)
    total_curr = sum(r["revenue"] for r in curr)
    total_growth = (total_curr - total_prev) / total_prev * 100
    results.append(f"TOTAL: ${total_prev:,} → ${total_curr:,} ({total_growth:+.1f}%)")
    return "\n".join(results)


def find_top_products(quarter: str, metric: str) -> str:
    """Find top products for a quarter ranked by a metric ('revenue' or 'units'). Returns ranked list."""
    data = SALES_DATA.get(quarter)
    if not data:
        return f"No data for {quarter}"
    if metric not in ("revenue", "units"):
        return "Metric must be 'revenue' or 'units'"
    ranked = sorted(data, key=lambda r: r[metric], reverse=True)
    return "\n".join(f"{i+1}. {r['product']}: {r[metric]:,} {metric}" for i, r in enumerate(ranked))


# --- Sub-agents ---

data_fetcher = Agent(
    model="gemini-3-flash-preview",
    name="data_fetcher",
    instruction="""You are a data fetcher. Your job is to retrieve sales data.

1. First list available quarters.
2. Then fetch sales data for ALL available quarters.
3. Compile everything you retrieved into your response.""",
    tools=[get_sales_data, list_available_quarters],
    output_key="fetched_data",
)

analyzer = Agent(
    model="gemini-3-flash-preview",
    name="analyzer",
    instruction="""You are a data analyst. The fetched sales data is here:
{fetched_data}

Analyze it:
1. Compute growth between the two quarters using the compute_growth tool.
2. Find top products by revenue for the latest quarter.
3. Summarize your findings.""",
    tools=[compute_growth, find_top_products],
    output_key="analysis",
)

report_writer = Agent(
    model="gemini-3-flash-preview",
    name="report_writer",
    instruction="""You are a report writer. Using the analysis below, write a concise executive summary.

Analysis:
{analysis}

Format the report with:
- A headline with the quarter
- Key metrics (total revenue, growth rate)
- Top performing products
- One actionable recommendation

Keep it under 200 words.""",
    output_key="report",
)

# --- Pipeline ---

pipeline = SequentialAgent(
    name="analytics_pipeline",
    sub_agents=[data_fetcher, analyzer, report_writer],
)

# --- Runner ---

runner = InMemoryRunner(agent=pipeline, app_name="analytics_pipeline")
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
    print("Analytics Report Generator (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = asyncio.run(run(user_input))
        print(f"\nReport:\n{result}\n")
