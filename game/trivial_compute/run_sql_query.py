import os
import pymysql
from dotenv import load_dotenv


def run_sql_query(categoryName):
    """
    Executes an SQL query on a given MySQL database and returns the results.

    Parameters:
    - category: str: the category of guestion for the SQL query

    Returns:
    - List[Tuple[Any]]: List of tuples containing the query results.
    """
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
            cursor.execute("SELECT Questions.questionID, Questions.questionContent, Questions.answerContent, Categories.categoryName FROM Questions LEFT JOIN Categories ON Questions.categoryID = Categories.categoryID WHERE Categories.categoryName=%s", categoryName)

            # Fetch all the results
            results = cursor.fetchall()

            return results
    finally:
        connection.close()
