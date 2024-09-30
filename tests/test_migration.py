import unittest
import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.snowflake_manager import connect_to_snowflake
from scripts.changelog_generator import create_dynamic_changelog
from scripts.migration_manager import MigrationManager
from config.settings import SNOWFLAKE_CREDENTIALS

class TestMigration(unittest.TestCase):
    def setUp(self):
        self.changelog_file = 'test_changelog.yaml'
        self.migration_manager = MigrationManager()

    def tearDown(self):
        if os.path.exists(self.changelog_file):
            os.remove(self.changelog_file)

    def test_changelog_generation(self):
        create_dynamic_changelog(self.changelog_file)
        self.assertTrue(os.path.exists(self.changelog_file))
        
        with open(self.changelog_file, 'r') as file:
            content = file.read()
        self.assertIn('databaseChangeLog', content)

    def test_migration_process(self):
        create_dynamic_changelog(self.changelog_file)
        try:
            self.migration_manager.run_migration(self.changelog_file)
        except Exception as e:
            self.fail(f"Migration process raised an exception: {str(e)}")

    def test_database_state(self):
        conn = connect_to_snowflake()
        try:
            with conn.cursor() as cursor:
                # Check if DATABASECHANGELOG table exists
                cursor.execute("SHOW TABLES LIKE 'DATABASECHANGELOG'")
                result = cursor.fetchone()
                self.assertIsNotNone(result, "DATABASECHANGELOG table should exist")

                # You can add more checks here, e.g., for specific tables or objects
                # that you expect to exist in your database
        finally:
            conn.close()

if __name__ == '__main__':
    unittest.main()