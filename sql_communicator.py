
import psycopg2

from settings import SQLConfig

def get_connection():
    connection_params = {
            'dbname': SQLConfig.DB,
            'user': SQLConfig.USER,
            'password': SQLConfig.PASSWORD,
            'host':     SQLConfig.HOST,
            'port': SQLConfig.PORT
        }
    return  psycopg2.connect(**connection_params)
    

