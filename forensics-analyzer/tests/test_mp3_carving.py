import unittest
import sys
import os
from pathlib import Path
import tempfile
import shutil

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from file_carver import FileCarver
from disk_image_generator import DiskImageGenerator

class TestMP3Carving(unittest.TestCase):
    """Test MP3 file carving functionality"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.carver = FileCarver()
        self.generator = DiskImageGenerator()
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_mp3_file_generation(self):
        """Test that MP3 files are generated with correct ID3 structure"""
        mp3_data = self.generator._generate_mp3(5000)
        
        # Check minimum size
        self.assertGreater(len(mp3_data), 1000)
        
        # Check ID3 header
        self.assertEqual(mp3_data[:3], b'ID3')
        
        # Check version (should be 2.3 or 2.4)
        version = mp3_data[3]
        self.assertIn(version, [3, 4])
        
        # Check for MP3 frame sync after ID3 tag
        tag_size = ((mp3_data[6] & 0x7F) << 21) | \
                   ((mp3_data[7] & 0x7F) << 14) | \
                   ((mp3_data[8] & 0x7F) << 7) | \
                   (mp3_data[9] & 0x7F)
        audio_start = 10 + tag_size
        
        if audio_start < len(mp3_data):
            # Check for MP3 frame sync (0xFF 0xFB or similar)
            self.assertEqual(mp3_data[audio_start], 0xFF)
            self.assertEqual(mp3_data[audio_start + 1] & 0xE0, 0xE0)
    
    def test_mp3_file_carving(self):
        """Test that MP3 files can be carved from disk image"""
        # Generate disk image with MP3 file
        self.generator.add_file({"type": "mp3", "size": 5000})
        image_path = Path(self.temp_dir) / 'test_mp3.dd'
        self.generator.generate(image_path, size_mb=1)
        
        # Carve files
        output_dir = Path(self.temp_dir) / 'carved'
        carved_files = self.carver.carve(image_path, output_dir)
        
        # Verify at least one MP3 file was carved
        mp3_files = [f for f in carved_files if f['type'] == 'mp3']
        self.assertGreater(len(mp3_files), 0, "No MP3 files were carved")
        
        # Verify carved MP3 file has correct structure
        mp3_file_path = Path(mp3_files[0]['path'])
        with open(mp3_file_path, 'rb') as f:
            header = f.read(10)
            self.assertEqual(header[:3], b'ID3')
    
    def test_mp3_size_optimization(self):
        """Test that MP3 files are carved with optimized size (not too much garbage)"""
        # Generate disk image with MP3 file
        self.generator.add_file({"type": "mp3", "size": 5000})
        image_path = Path(self.temp_dir) / 'test_mp3.dd'
        self.generator.generate(image_path, size_mb=1)
        
        # Carve files
        output_dir = Path(self.temp_dir) / 'carved'
        carved_files = self.carver.carve(image_path, output_dir)
        
        # Verify MP3 file was carved with reasonable size
        mp3_files = [f for f in carved_files if f['type'] == 'mp3']
        self.assertGreater(len(mp3_files), 0, "No MP3 files were carved")
        
        mp3_size = mp3_files[0]['size']
        # Should be less than 12KB (allowing some overhead for ID3 tags and audio)
        # Original issue was 20KB, now should be around 10KB or less
        self.assertLessEqual(mp3_size, 12 * 1024, 
                            f"MP3 file too large: {mp3_size} bytes (expected <= 12KB)")
        
        # Should be at least the minimum size
        self.assertGreaterEqual(mp3_size, 100, 
                               f"MP3 file too small: {mp3_size} bytes")
    
    def test_multiple_mp3_files(self):
        """Test carving multiple MP3 files from a single disk image"""
        # Generate disk image with multiple MP3 files
        self.generator.add_file({"type": "mp3", "size": 3000})
        self.generator.add_file({"type": "mp3", "size": 4000})
        self.generator.add_file({"type": "mp3", "size": 5000})
        
        image_path = Path(self.temp_dir) / 'test_multi_mp3.dd'
        self.generator.generate(image_path, size_mb=2)
        
        # Carve files
        output_dir = Path(self.temp_dir) / 'carved'
        carved_files = self.carver.carve(image_path, output_dir)
        
        # Verify all MP3 files were carved
        mp3_files = [f for f in carved_files if f['type'] == 'mp3']
        self.assertEqual(len(mp3_files), 3, "Expected 3 MP3 files to be carved")
        
        # Verify all files are valid
        for mp3_file in mp3_files:
            mp3_path = Path(mp3_file['path'])
            with open(mp3_path, 'rb') as f:
                header = f.read(3)
                self.assertEqual(header, b'ID3', f"Invalid MP3 header in {mp3_file['name']}")

if __name__ == '__main__':
    unittest.main()
