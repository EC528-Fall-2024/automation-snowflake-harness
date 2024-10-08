import logging
import subprocess
import os
import yaml
from config.settings import SNOWFLAKE_CREDENTIALS

class MigrationManager:
    def __init__(self):
        self.snowflake_url = self._construct_snowflake_url()
        self._log_snowflake_url()

    def _construct_snowflake_url(self):
        return (
            f"jdbc:snowflake://{SNOWFLAKE_CREDENTIALS['account']}.snowflakecomputing.com/?"
            f"user={SNOWFLAKE_CREDENTIALS['user']}&"
            f"password={SNOWFLAKE_CREDENTIALS['password']}&"
            f"warehouse={SNOWFLAKE_CREDENTIALS['warehouse']}&"
            f"database={SNOWFLAKE_CREDENTIALS['database']}&"
            f"schema={SNOWFLAKE_CREDENTIALS['schema']}"
        )

    def _log_snowflake_url(self):
        masked_url = self.snowflake_url.replace(SNOWFLAKE_CREDENTIALS['password'], '********')
        logging.info(f"Constructed Snowflake URL: {masked_url}")

    def _add_preconditions(self, changelog_file):
        with open(changelog_file, 'r') as file:
            changelog = yaml.safe_load(file)

        for changeset in changelog['databaseChangeLog']:
            if 'createTable' in changeset['changeSet']['changes'][0]:
                table = changeset['changeSet']['changes'][0]['createTable']
                changeset['changeSet']['preConditions'] = [
                    {'not': {'tableExists': {'schemaName': table['schemaName'], 'tableName': table['tableName']}}}
                ]
            elif 'createView' in changeset['changeSet']['changes'][0]:
                view = changeset['changeSet']['changes'][0]['createView']
                changeset['changeSet']['preConditions'] = [
                    {'not': {'viewExists': {'schemaName': view['schemaName'], 'viewName': view['viewName']}}}
                ]
            elif 'createSequence' in changeset['changeSet']['changes'][0]:
                sequence = changeset['changeSet']['changes'][0]['createSequence']
                changeset['changeSet']['preConditions'] = [
                    {'not': {'sequenceExists': {'schemaName': sequence['schemaName'], 'sequenceName': sequence['sequenceName']}}}
                ]

        with open(changelog_file, 'w') as file:
            yaml.dump(changelog, file, sort_keys=False)

    def run_migration(self, changelog_file):
        
        try:
            logging.info(f"Starting Liquibase migration using changelog: {changelog_file}")

            if not os.path.exists(changelog_file):
                raise FileNotFoundError(f"Changelog file not found: {changelog_file}")

            # Add preconditions to the changelog
            self._add_preconditions(changelog_file)

            # Check if Liquibase changelog table exists
            check_command = [
                'liquibase',
                f'--url={self.snowflake_url}',
                f'--defaultSchemaName={SNOWFLAKE_CREDENTIALS["schema"]}',
                'status'
            ]

            result = subprocess.run(check_command, capture_output=True, text=True)
            if "does not exist" in result.stderr:
                logging.info("Liquibase changelog table does not exist. Running initial setup.")
                init_command = [
                    'liquibase',
                    f'--url={self.snowflake_url}',
                    f'--defaultSchemaName={SNOWFLAKE_CREDENTIALS["schema"]}',
                    'changelogSync'
                ]
                subprocess.run(init_command, check=True)

            update_command = [
                'liquibase',
                f'--changeLogFile={changelog_file}',
                f'--url={self.snowflake_url}',
                f'--defaultSchemaName={SNOWFLAKE_CREDENTIALS["schema"]}',
                'update'
            ]

            logging.info(f"Running migration with command: {' '.join(update_command)}")
            
            result = subprocess.run(update_command, check=True, capture_output=True, text=True)
            
            logging.info("Migration Output:\n%s", result.stdout)
            if result.stderr:
                logging.warning("Migration Warnings/Errors:\n%s", result.stderr)

            self.verify_migration(changelog_file)

            logging.info("Liquibase migration completed successfully.")

        except subprocess.CalledProcessError as e:
            logging.error("Error running Liquibase migration:\nCommand: %s\nReturn Code: %d\nSTDOUT: %s\nSTDERR: %s", 
                          e.cmd, e.returncode, e.stdout, e.stderr)
            raise
        except Exception as e:
            logging.error("Unexpected error during migration: %s", str(e), exc_info=True)
            raise

    def verify_migration(self, changelog_file):
        try:
            logging.info("Verifying migration...")

            status_command = [
                'liquibase',
                f'--changeLogFile={changelog_file}',
                f'--url={self.snowflake_url}',
                f'--defaultSchemaName={SNOWFLAKE_CREDENTIALS["schema"]}',
                'status'
            ]

            result = subprocess.run(status_command, check=True, capture_output=True, text=True)
            logging.info("Migration Verification Output:\n%s", result.stdout)

            if "is up to date" in result.stdout:
                logging.info("Migration verification successful. Database is up to date.")
            else:
                logging.warning("Migration verification shows pending changes. Please review the status output.")

        except subprocess.CalledProcessError as e:
            logging.error("Error verifying migration:\nSTDOUT: %s\nSTDERR: %s", e.stdout, e.stderr)
            raise
        except Exception as e:
            logging.error("Unexpected error during migration verification: %s", str(e), exc_info=True)
            raise
    # Rollback the last n changes
    def rollback_last_changes(self, changelog_file,count=1):
        try:
            logging.info(f"Rolling back the last {count} changes.")

            rollback_command = [
                'liquibase',
                f'--changeLogFile={changelog_file}',
                f'--url={self.snowflake_url}',
                f'--defaultSchemaName={SNOWFLAKE_CREDENTIALS["schema"]}',
                'rollbackCount',
                str(count)
            ]

            result = subprocess.run(rollback_command, check=True, capture_output=True, text=True)
            logging.info("Rollback Output:\n%s", result.stdout)
            if result.stderr:
                logging.warning("Rollback Warnings/Errors:\n%s", result.stderr)

        except subprocess.CalledProcessError as e:
            logging.error("Error executing rollback:\nCommand: %s\nReturn Code: %d\nSTDOUT: %s\nSTDERR: %s",
                        e.cmd, e.returncode, e.stdout, e.stderr)
            raise
        except Exception as e:
            logging.error("Unexpected error during rollback: %s", str(e), exc_info=True)
            raise

    # Rollback to a specific tag        
    def rollback_to_tag(self, changelog_file,tag):
        try:
            logging.info(f"Rolling back to tag {tag}.")

            rollback_command = [
                'liquibase',
                f'--changeLogFile={changelog_file}',
                f'--url={self.snowflake_url}',
                f'--defaultSchemaName={SNOWFLAKE_CREDENTIALS["schema"]}',
                'rollback',
                tag
            ]

            result = subprocess.run(rollback_command, check=True, capture_output=True, text=True)
            logging.info("Rollback Output:\n%s", result.stdout)
            if result.stderr:
                logging.warning("Rollback Warnings/Errors:\n%s", result.stderr)

        except subprocess.CalledProcessError as e:
            logging.error("Error executing rollback:\nCommand: %s\nReturn Code: %d\nSTDOUT: %s\nSTDERR: %s", 
                        e.cmd, e.returncode, e.stdout, e.stderr)
            raise
        except Exception as e:
            logging.error("Unexpected error during rollback: %s", str(e), exc_info=True)
            raise