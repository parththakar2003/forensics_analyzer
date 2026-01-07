import unittest
from src.parser import Parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse_results(self):
        # Sample data to parse
        carved_files = [
            "file1.txt",
            "file2.jpg",
            "file3.pdf"
        ]
        expected_output = {
            "text_files": ["file1.txt"],
            "image_files": ["file2.jpg"],
            "pdf_files": ["file3.pdf"]
        }
        
        # Assuming parse_results method categorizes files
        result = self.parser.parse_results(carved_files)
        self.assertEqual(result, expected_output)

    def test_empty_results(self):
        # Test parsing with no files
        carved_files = []
        expected_output = {
            "text_files": [],
            "image_files": [],
            "pdf_files": []
        }
        
        result = self.parser.parse_results(carved_files)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()