from scripts.snowflake_manager import connect_to_snowflake

def execute_query(query):
    """
    Executes a given SQL query in Snowflake.
    """
    conn = connect_to_snowflake()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            print("Query executed successfully.")
    except Exception as e:
        print(f"Error executing query: {str(e)}")
    finally:
        conn.close()
