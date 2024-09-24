import logging
import snowflake.connector
import os
from config.settings import SNOWFLAKE_CREDENTIALS  # Import the credentials dictionary
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging with a unique filename based on the current timestamp
logging.basicConfig(
    filename=f'logs/migration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    filemode='a',                   # Append mode
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO              # Set logging level
)

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
            database=SNOWFLAKE_CREDENTIALS["database"],
            warehouse=SNOWFLAKE_CREDENTIALS["warehouse"],
            schema=SNOWFLAKE_CREDENTIALS["schema"]  # Use the schema if specified
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
