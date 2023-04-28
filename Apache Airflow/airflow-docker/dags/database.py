import csv
import json
import psycopg2
from airflow.models import Variable

# Define the filename for the CSV file.
FILENAME = './dags/data.csv'

class Database():
    def __init__(self):
        pass
    
    # Create a function that'll establish a connection to the database.
    def create_connection(self):
        # Get the connection details from Airflow variable.
        connection_id = 'lilbaby'
        
        # From Airflow variable, intialize varaibles.
        db_host = 'postgres'
        db_port = '5432'
        db_name = 'airflow'
        db_user = 'airflow'
        db_password = 'airflow'
        
        conn = None
        try:
            # Connect to the database.
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_password
            )
            print("[+] Connection to PostgreSQL database successful")
        except(Exception, psycopg2.Error) as error:
            print("[-] Error while connecting to PostgreSQL database", error)
            
        return(conn)
