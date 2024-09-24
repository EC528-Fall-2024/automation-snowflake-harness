import snowflake.connector
from config.settings import SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT, SNOWFLAKE_DATABASE

def connect_to_snowflake():
    """
    Establishes a connection to Snowflake.
    """
    try:
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            database=SNOWFLAKE_DATABASE
        )
        return conn
    except Exception as e:
        print("Failed to connect to Snowflake:", str(e))
        raise

def create_schema(schema_name):
    """
    Creates a schema in the specified Snowflake database.
    """
    conn = connect_to_snowflake()
    try:
        with conn.cursor() as cur:
            cur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
            print(f"Schema {schema_name} created successfully.")
    finally:
        conn.close()

if __name__ == "__main__":
    create_schema("demo_schema")
