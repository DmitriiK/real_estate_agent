from typing import List
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

from src.settings import MAIN_LLM_MODEL, VIEW_NAME
from src.utils.sql_communicator import get_records_by_ids

def request_user_choise_tool(object_ids: List[int]) -> dict:
    """
    Retrieve the records from the database based on the provided object IDs.

    Args:
        object_ids (List[int]): A list of integers representing object IDs.

    Returns:
        dict: A dictionary containing:
            - "records" (list): The retrieved records from the database.
    """

    records = get_records_by_ids(VIEW_NAME, object_ids, 'id', 'id, url, description')
    return {"records": records}
#

def calculate_price_tool(object_ids: List[int], tool_context: ToolContext) -> dict:
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
    After you said the price to client, as his confirmation, you should ask him to confirm the payment.
    If the client agrees, you should use 'request_user_choise_tool' to fetch additional information about the chosen apartments and 
    present it to the client in table format.
    After that you communication is completed. Say thank you to the client for using your service and say goodbye.
    """,
    tools=[calculate_price_tool, request_user_choise_tool],
)
