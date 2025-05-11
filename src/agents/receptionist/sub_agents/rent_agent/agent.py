from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from src.settings import MAIN_LLM_MODEL
from src.agents.text2SQL.agent import root_agent as text2SQL
from src.utils.sql_communicator import execute_select_query
from src.utils.utils import make_json_serializable

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
        sql_query (str): The SQL SELECT query to execute.
    Returns:
        dict: Query results 

    Example of returned dictionary:
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
    try:
        rows = execute_select_query(sql_query)
        if len(rows) > 100:
            rows= rows[:100]
            print("Warning: The result set is too large, only the first 100 rows are returned.")
            # otherwise in will cause error in ADK WEB for datetime and decimal types
        make_json_serializable(rows)
        return {
            'rows_from_db': rows,
            'errors': '',
        }
    except Exception as e:
        return {
            'rows_from_db': [],
            'errors': str(e),
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
    - Tools usage:
       - You have access to the following tools, that are supposed to be used in chain, 'text2SQL'->'execute_sql_query'.
       - Use 'text2SQL' tool to convert the client's request into a SQL query. 
       - Take the output result of text2SQL tool and pass it to the execute_sql_query tool as valid sql, striping all formatting if exists.
       - Once you get the result from the execute_sql_query tool, check if there are any errors in the result.
       - If there are errors, inform the client about them and ask him to clarify his request.
       - If there are no errors, check if the 'rows_from_db' key in the result is not empty.
       - If this list is not empty, format it as a table, using pseudografic and present it to the client
       - If the list is empty, inform the client that there are no options that meet his criteria.
    - After you present the results from DB to the client, ask him if he wants to continue the search or if he is satisfied with the options presented.
    - If the client is satisfied with the options presented or don't want to continue, say goodbye and pass control to the parent agen, receptionist.
    - Otherwise, ask the client to clarify his request and continue the search.
    """,
    tools=[AgentTool(agent=text2SQL), execute_sql_query],
)

