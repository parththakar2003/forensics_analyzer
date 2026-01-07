import unittest
from src.file_carver import FileCarver

class TestFileCarver(unittest.TestCase):
    def setUp(self):
        self.carver = FileCarver()

    def test_carve_files(self):
        # Assuming we have a test disk image and a directory to carve files into
        test_image_path = 'path/to/test_image.dd'
        output_directory = 'path/to/output_directory'
        
        # Call the carve_files method
        carved_files = self.carver.carve_files(test_image_path, output_directory)
        
        # Check if the carved files are as expected
        self.assertTrue(len(carved_files) > 0)
        for file in carved_files:
            self.assertTrue(os.path.exists(os.path.join(output_directory, file)))

if __name__ == '__main__':
    unittest.main()