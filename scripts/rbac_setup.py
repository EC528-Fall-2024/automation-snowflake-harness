import logging
import sys
import os
from dotenv import load_dotenv
import argparse
import snowflake.connector

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env file
load_dotenv()

SNOWFLAKE_CREDENTIALS = {
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA")
}

def connect_to_snowflake():
    try:
        logging.info("Connecting to Snowflake...")
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_CREDENTIALS["user"],
            password=SNOWFLAKE_CREDENTIALS["password"],
            account="orhmmra-ypb57008",
            warehouse=SNOWFLAKE_CREDENTIALS["warehouse"],
            database=SNOWFLAKE_CREDENTIALS["database"],
            schema=SNOWFLAKE_CREDENTIALS["schema"]
        )
        logging.info("Connection to Snowflake established successfully.")
        return conn
    except Exception as e:
        logging.error("Failed to connect to Snowflake: %s", str(e))
        raise

def create_role(conn, role_name):
    try:
        with conn.cursor() as cur:
            cur.execute(f"CREATE ROLE IF NOT EXISTS {role_name};")
            logging.info(f"Role {role_name} created.")
    except Exception as e:
        logging.error("Error creating role %s: %s", role_name, str(e))

def grant_privileges(conn, role_name, privileges):
    try:
        with conn.cursor() as cur:
            for privilege in privileges:
                cur.execute(privilege)
                logging.info(f"Privilege granted to role {role_name}: {privilege}")
    except Exception as e:
        logging.error("Error granting privileges to role %s: %s", role_name, str(e))

def create_user(conn, username, role_name):
    try:
        with conn.cursor() as cur:
            cur.execute(f"CREATE USER IF NOT EXISTS {username} PASSWORD='DemoPassword123!';")
            cur.execute(f"GRANT ROLE {role_name} TO USER {username};")
            logging.info(f"User {username} created and assigned role {role_name}.")
    except Exception as e:
        logging.error("Error creating user %s: %s", username, str(e))

def main():
    parser = argparse.ArgumentParser(description="Snowflake RBAC CLI Tool")
    parser.add_argument("--action", choices=["create_role", "grant_privileges", "create_user"], required=True, help="Action to perform")
    parser.add_argument("--role", type=str, help="Role name (for create_role or grant_privileges)")
    parser.add_argument("--privileges", nargs="+", help="List of privileges to grant (SQL statements for grant_privileges)")
    parser.add_argument("--user", type=str, help="Username (for create_user)")
    parser.add_argument("--assign_role", type=str, help="Role to assign to user (for create_user)")

    args = parser.parse_args()
    conn = connect_to_snowflake()

    try:
        if args.action == "create_role":
            if not args.role:
                logging.error("Role name is required for creating a role.")
                sys.exit(1)
            create_role(conn, args.role)

        elif args.action == "grant_privileges":
            if not args.role or not args.privileges:
                logging.error("Role name and privileges are required for granting privileges.")
                sys.exit(1)
            grant_privileges(conn, args.role, args.privileges)

        elif args.action == "create_user":
            if not args.user or not args.assign_role:
                logging.error("Username and role are required for creating a user.")
                sys.exit(1)
            create_user(conn, args.user, args.assign_role)

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
    finally:
        conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
