# File location: scripts/migration_manager.py

import logging
import subprocess

def run_liquibase_migration():
    """
    Execute the Liquibase migration script to update the Snowflake database.
    """
    logging.info("Starting Liquibase migration.")
    try:
        subprocess.run([
            "liquibase",
            "--changeLogFile=migrations/V1__create_database.sql",
            "update"
        ], check=True)
        logging.info("Liquibase migration executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Liquibase migration failed: {str(e)}")

def rollback_liquibase_migration():
    """
    Rollback the last Liquibase migration.
    """
    logging.info("Rolling back the last Liquibase migration.")
    try:
        subprocess.run([
            "liquibase",
            "rollback",
            "tag", "latest"
        ], check=True)
        logging.info("Liquibase rollback executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Liquibase rollback failed: {str(e)}")
