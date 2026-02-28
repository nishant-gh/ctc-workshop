"""
Agent B: Customer Support Bot (using OpenAI Agents SDK)

This exercise rewrites the customer support agent using the OpenAI Agents SDK.
Compare this with exercise 07 — notice how much boilerplate disappears:
  - No manual message history
  - No tool schema JSON
  - No agentic loop
  - No dispatcher function

Try:
  - "Where is my order 1?"
  - "I want to return order 2, is it eligible?"
  - "What's the status of order 99?"
"""

from agents import Agent, Runner, function_tool

# --- Fake database ---

ORDERS = {
    "1": {"item": "Wireless Headphones", "status": "shipped", "tracking": "TRK-98765", "date": "2025-02-20", "price": 79.99},
    "2": {"item": "USB-C Hub", "status": "delivered", "tracking": "TRK-11223", "date": "2025-02-10", "price": 34.99},
    "3": {"item": "Mechanical Keyboard", "status": "processing", "tracking": None, "date": "2025-02-27", "price": 149.99},
}

RETURN_POLICY = """
Items can be returned within 30 days of delivery for a full refund.
Items must be in original packaging and unused condition.
Electronics with opened packaging can only be exchanged, not refunded.
Shipping costs for returns are covered by the customer unless the item is defective.
"""

# --- Tools (just decorated functions — the SDK infers the schema) ---


@function_tool
def lookup_order(order_id: str) -> str:
    """Look up an order by its order ID. Returns order details including item, status, tracking, and price."""
    order = ORDERS.get(order_id)
    if order:
        return str(order)
    return f"No order found with ID {order_id}"


@function_tool
def get_return_policy() -> str:
    """Get the store's return and refund policy."""
    return RETURN_POLICY


@function_tool
def check_return_eligibility(order_id: str) -> str:
    """Check if a specific order is eligible for return based on delivery date and status."""
    order = ORDERS.get(order_id)
    if not order:
        return f"No order found with ID {order_id}"
    if order["status"] != "delivered":
        return f"Order {order_id} is not yet delivered (status: {order['status']}). Returns can only be initiated for delivered orders."
    return f"Order {order_id} ({order['item']}) was delivered on {order['date']}. It IS eligible for return within 30 days."


# --- Agent definition (replaces system prompt + tools + loop) ---

agent = Agent(
    name="TechShop Support",
    instructions="""You are a friendly customer support agent for TechShop, an online electronics store.

Guidelines:
- Be empathetic and helpful
- Always look up order details before answering order questions — never guess
- If an order is not found, apologize and ask the customer to double-check
- When discussing returns, always check the return policy first
- Keep responses concise but warm""",
    tools=[lookup_order, get_return_policy, check_return_eligibility],
    model="gpt-4.1-mini",
)

# --- Run the agent ---

if __name__ == "__main__":
    print("TechShop Support Bot (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = Runner.run_sync(agent, user_input)
        print(f"\nSupport: {result.final_output}\n")
