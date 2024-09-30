# File location: utils/db_utils.py

import snowflake.connector
from config.settings import *

def get_connection():
    """
    Establish a connection to the Snowflake database.
    
    Returns:
        snowflake.connector.connection: A connection object to the Snowflake database.
    """
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
