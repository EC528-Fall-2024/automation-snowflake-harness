# File location: main.py

import logging
from datetime import datetime
from scripts.snowflake_manager import create_database, create_schema
from scripts.migration_manager import run_liquibase_migration

# Generate a unique log filename based on the current timestamp
log_filename = f'logs/app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

# Configure logging
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """
    Main function to run the Snowflake resource deployment process.
    """
    logging.info("Starting Snowflake resource deployment process.")
    create_database("demo_database")
    create_schema("demo_schema")
    run_liquibase_migration()
    logging.info("Snowflake resource deployment process completed.")

if __name__ == "__main__":
    main()
