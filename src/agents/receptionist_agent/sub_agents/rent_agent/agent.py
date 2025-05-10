from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from src.settings import MAIN_LLM_MODEL
from src.agents.text_2_SQL_agent.agent import root_agent as text2SQL

def text2SQL_test_stub(human_query: str) -> dict:
    """translates human query to SQL query"""
    # This is a placeholder function for test
    return {
        'sql_query': f"SELECT * FROM v_emlak_data_mart WHERE description LIKE '%{human_query}%' LIMIT 10;",

    }

def execute_sql_query(sql_query: str) -> dict:
    """
    Execute a SQL SELECT query and return the result as dictionary.
    Args:
        query (str): The SQL SELECT query to execute.
    Returns:
        dict: Query results 

    example of returned dictionary:
        {
            'rows_from_db': [
                {'id': 1, 'description': 'Apartment kepez '},
                {'id': 2, 'description': 'Apartment liman'},
            ],
            'errors': '',
        }
        each row of the rows_from_db is a dictionary that represents row from SQL dataset with column names as keys.
        value of 'errors' key is empty string if there are no errors, otherwise it contains error message.
        """
    # This is a placeholder function. In a real implementation, this would
    # execute the SQL query against the database and return the result.
    return {
        'rows_from_db': [
            {'id': 1, 'description': 'Apartment kepez '},
            {'id': 2, 'description': 'Apartment liman'},
        ],
        'errors': '',
    }

# Create the root agent
rent_agent = Agent(
    name="rent_agent",
    model=MAIN_LLM_MODEL,
    description="An agency working with the clients who want to rent an apartment.",
    instruction="""
    You are an employee at a real estate agency working with the clients who want to rent an apartment.

    You have to:
    - find out from the client what kind of accommodation they're looking for.
    - answer, using access to the agency's database, their questions about the state of the realty estate rental market.
    - when  what client wants become clear, you should formulate them it a set of criteria for the search and ask the client if they have understood it correctly.
    - If the set of criteria is clear, query the database based on those criteria. Provide the resulting list to the client.
    - In the course of your communication, the client can adjust his wishes and supplement new  criteria for search.
    - When the client chooses one or more of the proposed options, you should ask him whether these options are enough for him. If so, refer him to a top-level agent. 
        If not, ask if he wants to continue the search. If not, pass control to the higher-level agent.

    You have access to the following tools, that are supposed to be used in chain, 'text2SQL'->'execute_sql_query'.
    Use 'text2SQL' tool to convert the client's request into a SQL query. 
    Take the output result of text2SQL tool and pass it to the execute_sql_query tool as valid sql, striping all formatting if exists.
    Once you get the result from the execute_sql_query tool, check if there are any errors in the result.
    If there are errors, inform the client about them and ask him to clarify his request.
    If there are no errors, check if the 'rows_from_db' key in the result is not empty.
    If this list is not empty, format it as a table and present it to the client
    If the list is empty, inform the client that there are no options that meet his criteria.
    After you present the table to the client, ask him if he wants to continue the search or if he is satisfied with the options presented.
    If the client is satisfied with the options presented or don't want to continue, say goodbye and pass control to the parent agent.
    """,
    tools=[AgentTool(agent=text2SQL), execute_sql_query],
)

