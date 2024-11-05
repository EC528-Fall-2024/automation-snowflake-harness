import unittest
import sys
import os

# Add scripts directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from rbac_setup import create_role, assign_role_to_user  # Import the functions you need to test

class TestRBACSetup(unittest.TestCase):
    
    def test_create_role(self):
        # Example test for create_role function
        result = create_role("TEST_ROLE")
        self.assertTrue(result)

    def test_assign_role_to_user(self):
        # Example test for assign_role_to_user function
        result = assign_role_to_user("TEST_USER", "TEST_ROLE")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
