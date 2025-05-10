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
            SELECT col.column_name, pgd.description
            FROM pg_catalog.pg_statio_all_tables AS st
            INNER JOIN pg_catalog.pg_description pgd ON pgd.objoid = st.relid
            INNER JOIN information_schema.columns col 
                ON col.table_schema = st.schemaname AND col.table_name = st.relname 
                AND col.ordinal_position = pgd.objsubid
            WHERE col.table_schema = :schema AND col.table_name = :table_name;
        """)
        
        comment_results = connection.execute(comment_query, 
                                           {"schema": schema, "table_name": table_name}).fetchall()
        
        # Create a dictionary of column comments
        comments_dict = {row[0]: row[1] for row in comment_results}
    
    # Combine column info with comments
    result = []
    for col in columns:
        column_info = {
            'name': col['name'],
            'type': str(col['type']),
            'comment': comments_dict.get(col['name'], None)
        }
        result.append(column_info)
    
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

