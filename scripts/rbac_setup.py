import logging
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import snowflake.connector

# Load Snowflake credentials from environment variables
SNOWFLAKE_CREDENTIALS = {
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA")
}

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

def setup_rbac():
    """
    Sets up Role-Based Access Control (RBAC) in Snowflake.
    """
    conn = connect_to_snowflake()
    try:
        with conn.cursor() as cur:
            # Step 1: Create Roles
            roles = ['devops_engineer', 'database_administrator', 'data_engineer', 'security_engineer', 'admin_role']
            for role in roles:
                cur.execute(f"CREATE ROLE IF NOT EXISTS {role};")
                logging.info(f"Role {role} created.")

            # Step 2: Grant Privileges to Roles
            # Granting privileges to DevOps Engineer
            cur.execute("GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE devops_engineer;")
            cur.execute("GRANT CREATE SCHEMA ON DATABASE TEST TO ROLE devops_engineer;")
            
            # Granting privileges to Database Administrator
            cur.execute("GRANT ALL PRIVILEGES ON DATABASE TEST TO ROLE database_administrator;")
            cur.execute("GRANT ALL PRIVILEGES ON ALL SCHEMAS IN DATABASE TEST TO ROLE database_administrator;")
            
            # Granting privileges to Data Engineer
            cur.execute("GRANT USAGE ON DATABASE TEST TO ROLE data_engineer;")
            cur.execute("GRANT USAGE ON ALL SCHEMAS IN DATABASE TEST TO ROLE data_engineer;")
            cur.execute("GRANT SELECT ON ALL TABLES IN SCHEMA PUBLIC TO ROLE data_engineer;")
            
            # Granting privileges to Security Engineer
            cur.execute("GRANT ROLE devops_engineer TO ROLE security_engineer;")
            cur.execute("GRANT ROLE database_administrator TO ROLE security_engineer;")
            
            # Granting privileges to the Admin role
            cur.execute("GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE admin_role;")
            cur.execute("GRANT ALL PRIVILEGES ON DATABASE TEST TO ROLE admin_role;")
            cur.execute("GRANT ALL PRIVILEGES ON ALL SCHEMAS IN DATABASE TEST TO ROLE admin_role;")

            # Step 3: Create Users and Assign Roles
            users = {
                'amruth': 'data_engineer',
                'hrishav': 'devops_engineer',
                'krish': 'admin_role',  # Assigning admin role
                'yuzhe': 'data_engineer',
                'rithvik': 'data_engineer'
            }

            for user, role in users.items():
                cur.execute(f"CREATE USER IF NOT EXISTS {user} PASSWORD='your_password';")  # Update this for strong password management
                cur.execute(f"GRANT ROLE {role} TO USER {user};")  # Associate the user with the role
                logging.info(f"User {user} created and assigned role {role}.")

    except Exception as e:
        logging.error("An error occurred during RBAC setup: %s", str(e))
    finally:
        conn.close()

# Call the setup_rbac function where appropriate in your project
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # Set logging level
    setup_rbac()
