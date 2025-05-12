from typing import Optional

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext
from google.genai import types

from src.agents.session_schema import SK_USER_CHOISE, SK_USER_NAME
from src.settings import MAIN_LLM_MODEL

from .sub_agents.rent_agent.agent import rent_agent
from .sub_agents.sales_agent.agent import sales_agent


def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Init session state and log the request.
    """
    state = callback_context.state
    if  SK_USER_NAME not in state:
        state[SK_USER_NAME] = "not defined yet"
    if  SK_USER_CHOISE not in state:
        state[SK_USER_NAME] = []

def add_user_data_to_session(user_name: str, tool_context: ToolContext) -> dict:
    """addding of user data to session state
    Args:
        user_name (str): name or the current user
        tool_context (ToolContext): Context for accessing and updating session state
    Returns:
        dict: status of the operation
    """
    tool_context.state[SK_USER_NAME] = user_name
    return {"status": "success"}

root_agent = Agent(
    name="receptionist_agent",
    model=MAIN_LLM_MODEL,
    description=" agent",
    instruction="""
    You're a real estate agent's office receptionist. 
    The service you are providing works like this:
    - The client goes to the rent agent, who will help them choose an apartment.
    - The client goes to the sales agent, who will help them calculate the price.
    You are the first point of contact for clients.
    Your name is Natasha. 
    The name of your client is {user_name}.
    At the beginning of the conversation with the visitor:
     - Greet them, introduce yourself, and ask how you can help them.
    
    If a visitor wants to rent an apartment, you'll need to:
    - Explain how the service you are providing works.
    - If the user's name is not defined yet, ask for their name, and use the tool 'add_user_data_to_session' to add this name to the session state.
    - Delegate first to the agent who deals with renting apartments (rent_agent).
    - If the user came from the sales agent and has already chosen an apartment, pass it to the sales agent.
    If this visitor came for another matter, you should express your regret that you cannot help them and say goodbye.
    """,
    sub_agents=[rent_agent, sales_agent],
    tools=[add_user_data_to_session],
    before_agent_callback=before_agent_callback,
)
