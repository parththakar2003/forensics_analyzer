import unittest
import sys
import os
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from file_parser import FileParser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = FileParser()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_parse_file(self):
        # Create a test file
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("This is a test file")
        
        # Parse the file
        result = self.parser.parse_file(test_file)
        
        # Check the result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['name'], 'test.txt')
        self.assertIn('size', result)
        self.assertEqual(result['extension'], '.txt')

    def test_parse_directory(self):
        # Create test files
        test_dir = Path(self.temp_dir) / "test_files"
        test_dir.mkdir()
        
        (test_dir / "file1.txt").write_text("Test 1")
        (test_dir / "file2.txt").write_text("Test 2")
        
        # Parse directory
        results = self.parser.parse_directory(test_dir)
        
        # Check results
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)

    def test_get_statistics(self):
        # Create and parse test files
        test_dir = Path(self.temp_dir) / "test_files"
        test_dir.mkdir()
        
        (test_dir / "file1.txt").write_text("Test 1")
        (test_dir / "file2.txt").write_text("Test 2")
        
        self.parser.parse_directory(test_dir)
        
        # Get statistics
        stats = self.parser.get_statistics()
        
        # Check statistics
        self.assertIsInstance(stats, dict)
        self.assertIn('total_files', stats)
        self.assertEqual(stats['total_files'], 2)

if __name__ == '__main__':
    unittest.main()