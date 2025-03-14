import os
import unittest
from ..metadata import extract_basic_metadata, extract_extended_metadata

class TestMetadata(unittest.TestCase):
    def setUp(self):
        # Create a temporary test file
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as f:
            f.write("test content")

    def tearDown(self):
        # Clean up the test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_basic_metadata(self):
        metadata = extract_basic_metadata(self.test_file)
        self.assertEqual(metadata['file_name'], "test_file.txt")
        self.assertEqual(metadata['file_extension'], ".txt")
        self.assertTrue('file_size' in metadata)
        self.assertTrue('created_time' in metadata)
        self.assertTrue('modified_time' in metadata)
        self.assertTrue('accessed_time' in metadata)

    def test_extended_metadata(self):
        metadata = extract_extended_metadata(self.test_file)
        self.assertTrue('extended' in metadata)
        self.assertEqual(metadata['file_name'], "test_file.txt")

