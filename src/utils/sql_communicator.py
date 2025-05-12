from sqlalchemy import create_engine, inspect, text

from src.settings import SQLConfig
engine = create_engine(SQLConfig.get_connection_string())



def get_table_metadata(table_name: str, schema='public') -> list[dict]:
    """
    Get column metadata for a specific table or view in PostgreSQL.
    
    Args:
        connection_string (str): SQLAlchemy connection string
        table_name (str): Name of the table or view
        schema (str): Schema name (default: 'public')
        
    Returns:
        list: List of dictionaries containing column metadata
    """

    inspector = inspect(engine)
    print("table_name", table_name)
    columns = inspector.get_columns(table_name, schema=schema) 
    # Get column comments from PostgreSQL's information_schema
    with engine.connect() as connection:
        comment_query = text("""
            SELECT
                a.attname as column_name,
                d.description as column_description
            FROM
                pg_catalog.pg_class c
                JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                JOIN pg_catalog.pg_attribute a ON a.attrelid = c.oid
                LEFT JOIN pg_catalog.pg_description d ON d.objoid = c.oid AND d.objsubid = a.attnum
            WHERE
                c.relname = :table_name
                AND n.nspname = :schema 
                AND a.attnum > 0
                AND NOT a.attisdropped         
        """)
        
        comment_results = connection.execute(comment_query, 
                                           {"schema": schema, "table_name": table_name}).fetchall()
        
        # Create a dictionary of column comments
        comments_dict = {row[0]: row[1] for row in comment_results}
    
    # Combine column info with comments
    result = [
        {
            'name': col['name'],
            'type': str(col['type']),
            'column_description': comments_dict.get(col['name'], None)
        }
        for col in columns
    ]
    
    return result

def execute_select_query(query: str, params: dict = None) -> list[dict]:
    """
    Execute a SQL SELECT query and return the result as a list of dictionaries.

    Args:
        query (str): The SQL SELECT query to execute.
        params (dict, optional): Parameters to bind to the query. Defaults to None.

    Returns:
        list[dict]: Query results as a list of dictionaries.
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), params or {})
        return [row._asdict() for row in result]  # Use _asdict() to convert row to dictionary

def get_records_by_ids(table_name: str, ids: list[int], id_column_name: str ='id', columns_to_fetch: str = '*') -> list[dict]:
    """
    Fetch records from a table where the ID is in the provided list of IDs.

    Args:
        table_name (str): The name of the table to query.
        ids (list[int]): A list of integer IDs to filter the query.

    Returns:
        list[dict]: Query results as a list of dictionaries.
    """
    if not ids:
        return []  # Return an empty list if no IDs are provided

    # Create a parameterized query
    query = f"SELECT {columns_to_fetch} FROM {table_name} WHERE {id_column_name} IN :ids"
    params = {"ids": tuple(ids)}  # Use a tuple for SQLAlchemy parameter binding

    return execute_select_query(query, params)
