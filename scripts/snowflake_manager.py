import logging
import snowflake.connector
from config.settings import SNOWFLAKE_CREDENTIALS

def connect_to_snowflake():
    """
    Establishes a connection to Snowflake.
    """
    try:
        logging.info("Connecting to Snowflake...")
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_CREDENTIALS["user"],
            password=SNOWFLAKE_CREDENTIALS["password"],
            account=SNOWFLAKE_CREDENTIALS["account"],
            warehouse=SNOWFLAKE_CREDENTIALS["warehouse"],
            database=SNOWFLAKE_CREDENTIALS["database"],
            schema=SNOWFLAKE_CREDENTIALS["schema"]
        )
        logging.info("Connection to Snowflake established successfully.")
        return conn
    except Exception as e:
        logging.error("Failed to connect to Snowflake: %s", str(e))
        raise

def create_schema(schema_name):
    """
    Creates a schema in the specified Snowflake database.
    """
    conn = connect_to_snowflake()
    try:
        with conn.cursor() as cur:
            cur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
            logging.info("Schema %s created successfully.", schema_name)
    finally:
        conn.close()

def execute_query(query):
    """
    Executes a given SQL query in Snowflake.
    """
    conn = connect_to_snowflake()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            logging.info("Query executed successfully.")
    except Exception as e:
        logging.error(f"Error executing query: {str(e)}")
    finally:
        conn.close()