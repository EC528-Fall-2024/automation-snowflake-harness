import snowflake.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Snowflake connection parameters
user = os.getenv('SNOWFLAKE_USER')
password = os.getenv('SNOWFLAKE_PASSWORD')
account = os.getenv('SNOWFLAKE_ACCOUNT')
warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
database = os.getenv('SNOWFLAKE_DATABASE')
schema = os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')  # Default to PUBLIC if not specified

def test_snowflake_connection():
    try:
        # Establish the connection
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema
        )

        # Create a cursor object
        cursor = conn.cursor()

        # Execute a simple query
        cursor.execute("SELECT CURRENT_VERSION()")

        # Fetch the result
        version = cursor.fetchone()
        print("Connected to Snowflake successfully, version:", version[0])

    except Exception as e:
        print("Failed to connect to Snowflake:", str(e))
    
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

if __name__ == "__main__":
    test_snowflake_connection()
