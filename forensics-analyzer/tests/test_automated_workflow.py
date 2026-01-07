import unittest
import sys
from pathlib import Path
import tempfile
import shutil
import os

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from automated_workflow import AutomatedForensicsWorkflow

class TestAutomatedWorkflow(unittest.TestCase):
    def setUp(self):
        self.workflow = AutomatedForensicsWorkflow()
        self.temp_dir = tempfile.mkdtemp()
        self.source_dir = Path(self.temp_dir) / 'source'
        self.output_dir = Path(self.temp_dir) / 'output'
        self.source_dir.mkdir()
        
        # Create test files with proper signatures
        # Create a minimal JPEG
        jpg_data = (
            b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
            b'\xff\xc0\x00\x11\x08\x00\x10\x00\x10\x03\x01\x22\x00\x02\x11\x01\x03\x11\x01'
            b'\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00'
            + b'\x00' * 100 +
            b'\xff\xd9'
        )
        with open(self.source_dir / 'test.jpg', 'wb') as f:
            f.write(jpg_data)
        
        # Create a minimal PDF
        pdf_data = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>
endobj
xref
0 4
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
trailer
<< /Size 4 /Root 1 0 R >>
startxref
194
%%EOF
"""
        with open(self.source_dir / 'test.pdf', 'wb') as f:
            f.write(pdf_data)

    def test_run_complete_workflow(self):
        # Run the workflow
        results = self.workflow.run_complete_workflow(
            self.source_dir,
            self.output_dir,
            recursive=False
        )
        
        # Check results
        self.assertEqual(results['status'], 'completed')
        self.assertGreater(results['statistics']['total_original_files'], 0)
        self.assertGreater(results['statistics']['total_carved_files'], 0)
        
        # Check that disk image was created
        disk_image = Path(results['disk_image_path'])
        self.assertTrue(disk_image.exists())
        
        # Check that carved files directory exists
        carved_dir = self.output_dir / 'carved_files'
        self.assertTrue(carved_dir.exists())

    def test_calculate_required_size(self):
        # This is tested as part of the workflow
        results = self.workflow.run_complete_workflow(
            self.source_dir,
            self.output_dir,
            recursive=False
        )
        
        # Check that size was calculated
        self.assertIn('required_image_size_mb', results['statistics'])
        self.assertGreater(results['statistics']['required_image_size_mb'], 0)

    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()
