import unittest
import sys
import os

# Add scripts directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from changelog_generator import generate_changelog_entry, parse_changelog  # Import the functions you need to test

class TestChangelogGenerator(unittest.TestCase):
    
    def test_generate_changelog_entry(self):
        # Example test for generate_changelog_entry function
        entry = generate_changelog_entry("author", "message")
        self.assertIn("author", entry)
        self.assertIn("message", entry)

    def test_parse_changelog(self):
        # Example test for parse_changelog function
        # Use a mock path or test data here
        changelog = parse_changelog("path/to/changelog")
        self.assertIsInstance(changelog, list)

if __name__ == '__main__':
    unittest.main()
