import unittest
import sys
import os
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from file_carver import FileCarver
from disk_image_generator import DiskImageGenerator

class TestFileCarver(unittest.TestCase):
    def setUp(self):
        self.carver = FileCarver()
        self.temp_dir = tempfile.mkdtemp()
        self.test_image_path = Path(self.temp_dir) / 'test_image.dd'
        self.output_directory = Path(self.temp_dir) / 'carved_output'
        
        # Generate a test disk image with some files
        generator = DiskImageGenerator()
        generator.add_file({"type": "jpg", "size": 5000})
        generator.add_file({"type": "txt", "content": "This is a test file."})
        generator.generate(self.test_image_path, size_mb=1)

    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_carve_files(self):
        # Call the carve method (not carve_files)
        carved_files = self.carver.carve(self.test_image_path, self.output_directory)
        
        # Check if files were carved
        self.assertIsInstance(carved_files, list)
        self.assertGreater(len(carved_files), 0)
        
        # Verify output directory exists
        self.assertTrue(self.output_directory.exists())

if __name__ == '__main__':
    unittest.main()