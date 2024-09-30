import logging
import os
from datetime import datetime
from scripts.snowflake_manager import create_schema
from scripts.changelog_generator import create_dynamic_changelog
from scripts.migration_manager import MigrationManager
from config.settings import SNOWFLAKE_CREDENTIALS
import yaml

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(
    filename=f'logs/migration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def validate_changelog(changelog_file):
    with open(changelog_file, 'r') as file:
        changelog = yaml.safe_load(file)
    
    ids = {}
    for changeset in changelog['databaseChangeLog']:
        changeset_id = changeset['changeSet']['id']
        if changeset_id in ids:
            raise ValueError(f"Duplicate changeset ID found: {changeset_id}\nOriginal: {ids[changeset_id]}\nDuplicate: {changeset}")
        ids[changeset_id] = changeset
    
    logging.info(f"Changelog validation successful. Total changesets: {len(ids)}")
    logging.info("Changeset IDs:")
    for changeset_id in ids:
        logging.info(f"  {changeset_id}")

def main():
    try:
        logging.info('Starting the migration process.')
        
        # Log Snowflake credentials (with password masked)
        masked_credentials = SNOWFLAKE_CREDENTIALS.copy()
        masked_credentials['password'] = '********'
        logging.info(f"Snowflake Credentials: {masked_credentials}")
        
        # Create the schema
        create_schema(SNOWFLAKE_CREDENTIALS['schema'])
        
        # Generate dynamic changelog
        changelog_file = f'migrations/generated_changelog_{datetime.now().strftime("%Y%m%d_%H%M%S")}.yaml'
        
        # Delete existing changelog file if it exists
        if os.path.exists(changelog_file):
            os.remove(changelog_file)
            logging.info(f"Deleted existing changelog file: {changelog_file}")
        
        create_dynamic_changelog(changelog_file)
        
        # Validate the generated changelog
        validate_changelog(changelog_file)
        
        # Initialize MigrationManager and run migration
        migration_manager = MigrationManager()
        migration_manager.run_migration(changelog_file)
        
        logging.info('Migration process completed successfully.')
    except ValueError as ve:
        logging.error(f'Validation error: {str(ve)}')
    except Exception as e:
        logging.error(f'Migration process failed: {str(e)}', exc_info=True)

if __name__ == '__main__':
    main()