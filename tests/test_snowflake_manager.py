import unittest
import sys
import os

# Add scripts directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from snowflake_manager import connect_to_snowflake, create_schema  # Import the functions you need to test

class TestSnowflakeManager(unittest.TestCase):
    
    def test_connect_to_snowflake(self):
        # Example test for connect_to_snowflake function
        connection = connect_to_snowflake()
        self.assertIsNotNone(connection)

    def test_create_schema(self):
        # Example test for create_schema function
        result = create_schema("TEST_SCHEMA")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
