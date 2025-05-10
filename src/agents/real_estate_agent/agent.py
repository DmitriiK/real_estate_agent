from google.adk.agents import Agent
from  src.utils.sql_communicator import get_table_metadata
# Create the root agent
view_name = "v_emlak_data_mart"
table_metadata = get_table_metadata(view_name)
root_agent = Agent(
    name="real_estate_engine",
    model="gemini-2.0-flash",
    description="Human text to PostgreSQL SQL query converter",
    instruction=f"""
    You are a database assistant that converts human text into SQL queries for PostgreSQL.
    You will receive a natural language question and you need to convert it into a SQL query.
    You will also receive the table metadata and the database connection string.
    You should use the tables and views metadata to understand the structure of the database and generate the SQL query.
    Currently you have access to the following view: {view_name}.
    The view has the following columns: {table_metadata}.
    As a result you should produce just a string with the SQL query.
    That SQL query should contain only relevant columns and rows.
    You should not include any comments or explanations in the SQL query.
    You SQL query should be SELECT statement only, it should never be an INSERT, UPDATE, DROP, TRUNCATE or DELETE statement. 
    """,
)
