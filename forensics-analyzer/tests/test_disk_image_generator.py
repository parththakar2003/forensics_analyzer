import unittest
from src.disk_image_generator import DiskImageGenerator
import os

class TestDiskImageGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = DiskImageGenerator()
        self.image_path = 'evidence.dd'

    def test_create_image(self):
        self.generator.create_image()
        self.assertTrue(os.path.exists(self.image_path))

    def tearDown(self):
        if os.path.exists(self.image_path):
            os.remove(self.image_path)

if __name__ == '__main__':
    unittest.main()