
from sqlalchemy import create_engine, inspect, text

from settings import SQLConfig
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

