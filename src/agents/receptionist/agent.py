from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

from .sub_agents.rent_agent.agent import rent_agent
from .sub_agents.lease_agent.agent import lease_agent
from src.settings import MAIN_LLM_MODEL


def add_user_data_to_session(user_name: str, tool_context: ToolContext) -> dict:
    """addding of user data to session state
    Args:
        user_name (dict): name or the current user
        tool_context (ToolContext): Context for accessing and updating session state
    Returns:
        dict: status of the operation
    """
    tool_context.state['user_name'] = user_name
    return {"status": "success"}

root_agent = Agent(
    name="receptionist_agent",
    model=MAIN_LLM_MODEL,
    description=" agent",
    instruction="""
    You're a real estate agent's office receptionist. 
    Your name is Natasha. 
    In the beginning of conversation you with the visitor, greet them, introduce yourself, ask how we can help them.
    
    If a visitor wants to rent or lease an apartment, you'll need to
    - ask for their name
    -- use the tool 'add_user_data_to_session' to add this name to the session state
    - depeinding of what the visitor wants, delegate him:
        -- either to an agent who handles clients who want to rent someone else's apartment (rent_agent),
        -- or to an agent who deals with clients who wants to rent out their apartment (lease_agent).
    
    If this visitor came for another matter - you should express your regret that you cannot help him and say goodbye.

    If this visitor came back to you from one of your agents, you should ask for the result and, if you don't already have his phone number, put it in the database and say goodbye.

    """,
    sub_agents=[rent_agent, lease_agent],
    tools=[add_user_data_to_session]

)
