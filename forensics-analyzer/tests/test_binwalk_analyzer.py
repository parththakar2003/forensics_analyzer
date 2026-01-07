import unittest
import sys
from pathlib import Path
import tempfile
import shutil
import os

# Add src directory to path for imports (required for unittest discover)
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from binwalk_analyzer import BinwalkAnalyzer
from disk_image_generator import DiskImageGenerator

class TestBinwalkAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = BinwalkAnalyzer()
        self.temp_dir = tempfile.mkdtemp()
        self.test_image = Path(self.temp_dir) / 'test_image.dd'
        self.output_dir = Path(self.temp_dir) / 'binwalk_output'

    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_is_binwalk_available(self):
        # Test if binwalk availability check works
        result = self.analyzer.is_binwalk_available()
        self.assertIsInstance(result, bool)

    def test_analyze_without_binwalk(self):
        # Generate a test image
        generator = DiskImageGenerator()
        generator.add_file({"type": "jpg", "size": 5000})
        generator.generate(self.test_image, size_mb=1)
        
        # Try to analyze (should work even if binwalk is not installed)
        results = self.analyzer.analyze(self.test_image, self.output_dir)
        
        # Results should be a list (empty if binwalk not available)
        self.assertIsInstance(results, list)

    def test_analyze_nonexistent_file(self):
        # Test with non-existent file
        nonexistent = Path(self.temp_dir) / 'nonexistent.dd'
        results = self.analyzer.analyze(nonexistent, self.output_dir)
        
        # Should return empty list
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()