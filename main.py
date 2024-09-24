from scripts.migration_manager import run_liquibase_migration
from scripts.snowflake_manager import create_schema
import logging
import os
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

def main():
    """
    Main function to run the schema creation and migration.
    """
    logging.info('Starting the migration process.')
    create_schema("demo_schema")  # Create the demo schema
    run_liquibase_migration()      # Run Liquibase migrations
    logging.info('Migration process completed.')

if __name__ == '__main__':
    main()
