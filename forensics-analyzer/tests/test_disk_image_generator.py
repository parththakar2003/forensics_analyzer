import unittest
import sys
from pathlib import Path
import tempfile
import shutil
import os

# Add src directory to path for imports (required for unittest discover)
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from disk_image_generator import DiskImageGenerator

class TestDiskImageGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = DiskImageGenerator()
        self.temp_dir = tempfile.mkdtemp()
        self.image_path = Path(self.temp_dir) / 'test_evidence.dd'

    def test_generate_image(self):
        # Add some files to embed
        self.generator.add_file({"type": "jpg", "size": 5000})
        self.generator.add_file({"type": "txt", "content": "Test content"})
        
        # Generate the image
        self.generator.generate(self.image_path, size_mb=1)
        
        # Check if image was created
        self.assertTrue(self.image_path.exists())
        self.assertGreater(self.image_path.stat().st_size, 0)

    def test_add_file(self):
        # Test adding files
        initial_count = len(self.generator.files_to_embed)
        self.generator.add_file({"type": "pdf", "size": 3000})
        
        # Check if file was added
        self.assertEqual(len(self.generator.files_to_embed), initial_count + 1)

    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()