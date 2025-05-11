from typing import List
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

from src.settings import MAIN_LLM_MODEL


def calculate_price(object_ids: List[int], tool_context: ToolContext) -> dict:
    """
    Calculate the total price based on the object IDs provided.

    Args:
        object_ids (List[int]): A list of integers representing object IDs.
        tool_context (ToolContext): A context object containing state information.

    Returns:
        dict: A dictionary containing:
            - "total_price" (int): The calculated total price.
            - "explanation" (str): A textual explanation of the price calculation.
    """

    item_price = 100
    total_price = item_price * len(object_ids)
    tool_context.state["total_price"] = total_price
    explanation = f"The total price is calculated as {item_price} * {len(object_ids)} = {total_price}"
    return {"total_price": total_price, "explanation": explanation}

sales_agent = Agent(
    name="sales_agent",
    model=MAIN_LLM_MODEL,
    description="realty agency agent, who deals with payments for agency services",
    instruction="""
    You're a real estate agency agent,  who deals with payments for agency services".
    Your name is Monika, the name of you client is {user_name}.
    The client migh have choosen one of the appartments from the list of apartments you have access to.
    The IDs of chosen objects are {user_choise}.
    You should calculate the total price, using 'calculate_price' tool for the client and explain how you calculated it.
    """,
    tools=[calculate_price],
)
