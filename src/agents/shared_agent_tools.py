from src.utils.sql_communicator import execute_select_query
from src.utils.utils import make_json_serializable
from src.settings import MAX_NUMBER_OF_ROWS

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
        if len(rows) > MAX_NUMBER_OF_ROWS:
            rows= rows[:MAX_NUMBER_OF_ROWS]
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
