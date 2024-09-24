import subprocess
import os

def run_liquibase_migration():
    """
    Executes Liquibase migration scripts from the specified changelog file.
    """
    try:
        print("Starting Liquibase migration...")

        # Command to run Liquibase migration
        command = [
            'liquibase',
            '--changeLogFile=migrations/changelog.xml',
            '--url=jdbc:snowflake://euwmcnr-mhb16871.snowflakecomputing.com/?user=EC528AUTOMATION&password=Chesterfield4396@&warehouse=COMPUTE_WH&db=TEST&schema=PUBLIC',
            'update'
        ]

        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Migration Output:\n", result.stdout)

    except subprocess.CalledProcessError as e:
        print("Error during migration:", e.stderr)
        raise
