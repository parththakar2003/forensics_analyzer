import unittest
import sys
import os
from pathlib import Path
import tempfile
import shutil
import zipfile
import io

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from file_carver import FileCarver
from disk_image_generator import DiskImageGenerator
from file_parser import FileParser

class TestWavDocxSupport(unittest.TestCase):
    """Test WAV and DOCX/XLSX file handling"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.carver = FileCarver()
        self.generator = DiskImageGenerator()
        self.parser = FileParser()
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_wav_file_generation(self):
        """Test that WAV files are generated with correct structure"""
        wav_data = self.generator._generate_wav(5000)
        
        # Check minimum size
        self.assertGreater(len(wav_data), 44)  # Minimum WAV header size
        
        # Check RIFF header
        self.assertEqual(wav_data[:4], b'RIFF')
        
        # Check WAVE identifier
        self.assertEqual(wav_data[8:12], b'WAVE')
        
        # Check fmt chunk
        self.assertIn(b'fmt ', wav_data)
        
        # Check data chunk
        self.assertIn(b'data', wav_data)
    
    def test_wav_file_carving(self):
        """Test that WAV files can be carved from disk image"""
        # Generate disk image with WAV file
        self.generator.add_file({"type": "wav", "size": 5000})
        image_path = Path(self.temp_dir) / 'test_wav.dd'
        self.generator.generate(image_path, size_mb=1)
        
        # Carve files
        output_dir = Path(self.temp_dir) / 'carved'
        carved_files = self.carver.carve(image_path, output_dir)
        
        # Verify at least one WAV file was carved
        wav_files = [f for f in carved_files if f['type'] == 'wav']
        self.assertGreater(len(wav_files), 0, "No WAV files were carved")
        
        # Verify carved WAV file has correct structure
        wav_file_path = Path(wav_files[0]['path'])
        with open(wav_file_path, 'rb') as f:
            header = f.read(12)
            self.assertEqual(header[:4], b'RIFF')
            self.assertEqual(header[8:12], b'WAVE')
    
    def test_docx_file_generation(self):
        """Test that DOCX files are generated with proper Office structure"""
        docx_data = self.generator._generate_docx(3000)
        
        # Check ZIP header
        self.assertEqual(docx_data[:4], b'PK\x03\x04')
        
        # Verify it's a valid ZIP with Office structure
        zip_buffer = io.BytesIO(docx_data)
        with zipfile.ZipFile(zip_buffer, 'r') as zf:
            filenames = zf.namelist()
            
            # Check required Office files
            self.assertIn('[Content_Types].xml', filenames)
            self.assertIn('_rels/.rels', filenames)
            
            # Check for Word-specific structure
            word_files = [f for f in filenames if f.startswith('word/')]
            self.assertGreater(len(word_files), 0, "No word/ directory found")
    
    def test_xlsx_file_generation(self):
        """Test that XLSX files are generated with proper Office structure"""
        xlsx_data = self.generator._generate_xlsx(3000)
        
        # Check ZIP header
        self.assertEqual(xlsx_data[:4], b'PK\x03\x04')
        
        # Verify it's a valid ZIP with Office structure
        zip_buffer = io.BytesIO(xlsx_data)
        with zipfile.ZipFile(zip_buffer, 'r') as zf:
            filenames = zf.namelist()
            
            # Check required Office files
            self.assertIn('[Content_Types].xml', filenames)
            self.assertIn('_rels/.rels', filenames)
            
            # Check for Excel-specific structure
            xl_files = [f for f in filenames if f.startswith('xl/')]
            self.assertGreater(len(xl_files), 0, "No xl/ directory found")
    
    def test_docx_detection(self):
        """Test that DOCX files are correctly detected and carved as DOCX"""
        # Generate disk image with DOCX file
        self.generator.add_file({"type": "docx", "size": 3000})
        image_path = Path(self.temp_dir) / 'test_docx.dd'
        self.generator.generate(image_path, size_mb=1)
        
        # Carve files
        output_dir = Path(self.temp_dir) / 'carved'
        carved_files = self.carver.carve(image_path, output_dir)
        
        # Verify DOCX file was carved and detected as DOCX
        docx_files = [f for f in carved_files if f['type'] == 'docx']
        self.assertGreater(len(docx_files), 0, "No DOCX files were detected")
    
    def test_xlsx_detection(self):
        """Test that XLSX files are correctly detected and carved as XLSX"""
        # Generate disk image with XLSX file
        self.generator.add_file({"type": "xlsx", "size": 3000})
        image_path = Path(self.temp_dir) / 'test_xlsx.dd'
        self.generator.generate(image_path, size_mb=1)
        
        # Carve files
        output_dir = Path(self.temp_dir) / 'carved'
        carved_files = self.carver.carve(image_path, output_dir)
        
        # Verify XLSX file was carved and detected as XLSX
        xlsx_files = [f for f in carved_files if f['type'] == 'xlsx']
        self.assertGreater(len(xlsx_files), 0, "No XLSX files were detected")
    
    def test_mixed_file_types(self):
        """Test carving multiple file types including WAV and DOCX"""
        # Generate disk image with various file types
        self.generator.add_file({"type": "wav", "size": 5000})
        self.generator.add_file({"type": "docx", "size": 3000})
        self.generator.add_file({"type": "xlsx", "size": 3000})
        self.generator.add_file({"type": "zip", "size": 2000})
        self.generator.add_file({"type": "jpg", "size": 2000})
        
        image_path = Path(self.temp_dir) / 'test_mixed.dd'
        self.generator.generate(image_path, size_mb=2)
        
        # Carve files
        output_dir = Path(self.temp_dir) / 'carved'
        carved_files = self.carver.carve(image_path, output_dir)
        
        # Count file types
        type_counts = {}
        for f in carved_files:
            type_counts[f['type']] = type_counts.get(f['type'], 0) + 1
        
        # Verify we found each type
        self.assertIn('wav', type_counts, "WAV file not found")
        self.assertIn('docx', type_counts, "DOCX file not found")
        self.assertIn('xlsx', type_counts, "XLSX file not found")
        self.assertIn('zip', type_counts, "ZIP file not found")
        self.assertIn('jpg', type_counts, "JPG file not found")
    
    def test_wav_validation(self):
        """Test that WAV files are validated correctly by FileParser"""
        # Generate a WAV file
        wav_data = self.generator._generate_wav(5000)
        wav_path = Path(self.temp_dir) / 'test.wav'
        with open(wav_path, 'wb') as f:
            f.write(wav_data)
        
        # Parse the file
        file_info = self.parser.parse_file(wav_path)
        
        # Verify validation
        self.assertTrue(file_info.get('is_valid'), "WAV file not validated")
        self.assertEqual(file_info.get('extension'), '.wav')

if __name__ == '__main__':
    unittest.main()
