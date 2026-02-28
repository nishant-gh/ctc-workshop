"""
Agent B: Customer Support Bot

A more complex agent with a persona (system prompt) and multiple tools
that query a fake database. Shows how tools can be data lookups, not just computation.

Try:
  - "Where is my order 1?"
  - "I want to return order 2, is it eligible?"
  - "What's the status of order 99?"
"""

import anthropic

client = anthropic.Anthropic()

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

# --- System prompt ---

SYSTEM_PROMPT = """You are a friendly customer support agent for TechShop, an online electronics store.

Guidelines:
- Be empathetic and helpful
- Always look up order details before answering order questions — never guess
- If an order is not found, apologize and ask the customer to double-check
- When discussing returns, always check the return policy first
- Keep responses concise but warm"""

# --- Tools ---

tools = [
    {
        "name": "lookup_order",
        "description": "Look up an order by its order ID. Returns order details including item, status, tracking, and price.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID to look up",
                }
            },
            "required": ["order_id"],
        },
    },
    {
        "name": "get_return_policy",
        "description": "Get the store's return and refund policy",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "check_return_eligibility",
        "description": "Check if a specific order is eligible for return based on delivery date and status",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID to check return eligibility for",
                }
            },
            "required": ["order_id"],
        },
    },
]


def call_tool(name, input):
    if name == "lookup_order":
        order = ORDERS.get(input["order_id"])
        if order:
            return str(order)
        return f"No order found with ID {input['order_id']}"

    elif name == "get_return_policy":
        return RETURN_POLICY

    elif name == "check_return_eligibility":
        order = ORDERS.get(input["order_id"])
        if not order:
            return f"No order found with ID {input['order_id']}"
        if order["status"] != "delivered":
            return f"Order {input['order_id']} is not yet delivered (status: {order['status']}). Returns can only be initiated for delivered orders."
        return f"Order {input['order_id']} ({order['item']}) was delivered on {order['date']}. It IS eligible for return within 30 days."

    return "Unknown tool"


# --- Agent loop ---

if __name__ == "__main__":
    messages = []
    print("TechShop Support Bot (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})

        while True:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=messages,
                tools=tools,
            )

            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = call_tool(block.name, block.input)
                    print(f"  [{block.name}] → {result[:80]}...")
                    tool_results.append(
                        {"type": "tool_result", "tool_use_id": block.id, "content": result}
                    )
                elif block.type == "text" and response.stop_reason == "end_turn":
                    print(f"\nSupport: {block.text}\n")

            if tool_results:
                messages.append({"role": "user", "content": tool_results})
            else:
                break
