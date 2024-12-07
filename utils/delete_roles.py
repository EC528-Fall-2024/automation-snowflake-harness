import logging
import snowflake.connector
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import SNOWFLAKE_CREDENTIALS

def connect_to_snowflake():
    """
    Establish a connection to Snowflake.
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

def delete_roles():
    """
    Deletes all roles except ACCOUNTADMIN and system-defined roles.
    """
    conn = connect_to_snowflake()
    try:
        with conn.cursor() as cur:
            # Get a list of all roles
            cur.execute("SHOW ROLES;")
            non_deletable_roles = ["ACCOUNTADMIN", "ORGADMIN", "PUBLIC", "SECURITYADMIN", "SYSADMIN", "USERADMIN"]
            roles = [row[1] for row in cur.fetchall() if row[1] not in non_deletable_roles]

            # Drop each role
            for role in roles:
                try:
                    cur.execute(f"DROP ROLE IF EXISTS {role};")
                    logging.info(f"Role {role} deleted successfully.")
                except Exception as e:
                    logging.error(f"Failed to delete role {role}: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    delete_roles()
