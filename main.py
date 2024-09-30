from scripts.migration_manager import run_liquibase_migration, generate_changelog
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
    
    # Create the demo schema
    create_schema("demo_schema")
    
    # Generate changelog before running migration
    reference_db_url = 'jdbc:snowflake://euwmcnr-mhb16871.snowflakecomputing.com/?user=EC528AUTOMATION&password=Chesterfield4396@&warehouse=COMPUTE_WH&db=TEST&schema=PUBLIC'
    generate_changelog(reference_db_url)  # Generate changelog

    # Run Liquibase migrations
    run_liquibase_migration()
    
    logging.info('Migration process completed.')

if __name__ == '__main__':
    main()
