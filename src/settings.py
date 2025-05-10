MAIN_LLM_MODEL = "gemini-2.0-flash"


class SQLConfig:
    HOST = 'localhost'
    DB = 'emlak'
    PORT = 5432
    USER="postgres"
    PASSWORD="123" 
    def get_connection_string():
        return f"postgresql://{SQLConfig.USER}:{SQLConfig.PASSWORD}@{SQLConfig.HOST}:{SQLConfig.PORT}/{SQLConfig.DB}"
    
