import os
import subprocess
import pytest
from scripts.migration_manager import MigrationManager
from scripts.snowflake_manager import connect_to_snowflake

# Fixture to create and clean up the changelog file
@pytest.fixture
def changelog_file():
    filename = 'test_changelog.yaml'
    content = '''
databaseChangeLog:
  - changeSet:
      id: create-test-table
      author: test-author
      changes:
        - createTable:
            schemaName: TEST_SCHEMA
            tableName: test_table
            columns:
              - column:
                  name: id
                  type: INT
                  constraints:
                    primaryKey: true
              - column:
                  name: name
                  type: VARCHAR(255)
      rollback:
        - dropTable:
            schemaName: TEST_SCHEMA
            tableName: test_table
    '''
    # Write the content to the file
    with open(filename, 'w') as file:
        file.write(content)
    
    yield filename  # Provide the filename to the test

    # Clean up: remove the file after the test
    if os.path.exists(filename):
        os.remove(filename)

@pytest.fixture(scope='module')
def migration_manager():
    """Create an instance of MigrationManager with test credentials."""
    return MigrationManager()

def test_rollback_last_changes_integration(migration_manager, changelog_file):
    """Integration test for rolling back the last change."""
    # Run migration
    migration_manager.run_migration(changelog_file)

    # Verify table exists
    conn = connect_to_snowflake()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM TEST_SCHEMA.test_table")
            data = cursor.fetchall()
            assert data == []
    finally:
        conn.close()

    # Perform rollback
    migration_manager.rollback_last_changes(changelog_file,count=1)

    # Verify table no longer exists
    conn = connect_to_snowflake()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM TEST_SCHEMA.test_table")
            pytest.fail("Table 'test_table' should not exist after rollback.")
    except Exception as e:
        # Expecting an exception since the table should not exist
        assert 'does not exist' in str(e)
    finally:
        conn.close()
