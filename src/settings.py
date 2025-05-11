MAIN_LLM_MODEL = "gemini-2.0-flash"
MAX_NUMBER_OF_ROWS = 10 # max number or rows we can give from the results of SQL to LLM model
VIEW_NAME = "v_emlak_data_mart" # name of the view we are using in the SQL queries
class SQLConfig:
    HOST = 'localhost'
    DB = 'emlak'
    PORT = 5432
    USER="postgres"
    PASSWORD="123" 
    def get_connection_string():
        return f"postgresql://{SQLConfig.USER}:{SQLConfig.PASSWORD}@{SQLConfig.HOST}:{SQLConfig.PORT}/{SQLConfig.DB}"
    
