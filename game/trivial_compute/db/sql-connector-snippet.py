import os
import pymysql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='db/database.env')

# Get database credentials from environment variables
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Connect to the database
connection = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

try:
    with connection.cursor() as cursor:
        # Execute the query
        cursor.execute("SELECT * FROM Questions")
        
        # Fetch all the results
        results = cursor.fetchall()
        
        # Print the results
        for row in results:
            print(row)
finally:
    connection.close()
