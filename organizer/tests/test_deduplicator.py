import os
import unittest
from ..deduplicator import compute_file_hash

class TestDeduplicator(unittest.TestCase):
    def setUp(self):
        # Create two test files
        self.test_file1 = "test_file1.txt"
        self.test_file2 = "test_file2.txt"
        with open(self.test_file1, "w") as f:
            f.write("test content")
        with open(self.test_file2, "w") as f:
            f.write("test content")

    def tearDown(self):
        # Clean up test files
        for file in [self.test_file1, self.test_file2]:
            if os.path.exists(file):
                os.remove(file)

    def test_hash_computation(self):
        hash1 = compute_file_hash(self.test_file1)
        hash2 = compute_file_hash(self.test_file2)
        self.assertIsNotNone(hash1)
        self.assertIsNotNone(hash2)
        self.assertEqual(hash1, hash2)  # Should be equal for identical content

