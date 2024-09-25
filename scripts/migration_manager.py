import logging
import subprocess
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

def run_liquibase_migration():
    """
    Executes Liquibase migration scripts from the specified changelog file.
    """
    try:
        logging.info("Starting Liquibase migration...")

        # Command to run Liquibase migration
        command = [
            'liquibase',
            '--changeLogFile=migrations/changelog.yaml',  # Updated to YAML
            '--url=jdbc:snowflake://euwmcnr-mhb16871.snowflakecomputing.com/?user=EC528AUTOMATION&password=Chesterfield4396@&warehouse=COMPUTE_WH&db=TEST&schema=PUBLIC',
            'update'
        ]

        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info("Migration Output:\n%s", result.stdout)

    except subprocess.CalledProcessError as e:
        logging.error("Error during migration: %s", e.stderr)
        raise
    except Exception as e:
        logging.error("Unexpected error: %s", str(e))
        raise
