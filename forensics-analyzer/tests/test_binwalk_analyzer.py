import unittest
from src.binwalk_analyzer import BinwalkAnalyzer

class TestBinwalkAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = BinwalkAnalyzer()

    def test_run_binwalk(self):
        # Assuming we have a test file to analyze
        test_file = 'path/to/test/file'
        results = self.analyzer.run_binwalk(test_file)
        self.assertIsNotNone(results)
        self.assertIn('expected_output', results)

if __name__ == '__main__':
    unittest.main()