import unittest
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import encode_depth_to_bytes, create_gdepth_xmp

class TestUtils(unittest.TestCase):
    def test_encode_depth_to_bytes(self):
        depth = np.array([[0, 1], [0.5, 0.2]])
        encoded = encode_depth_to_bytes(depth)
        self.assertIsInstance(encoded, bytes)
        self.assertEqual(len(encoded), 4 * 2) # 4 pixels * 2 bytes (uint16)

    def test_create_gdepth_xmp(self):
        depth = np.zeros((10, 10))
        xmp = create_gdepth_xmp(depth, 10, 10)
        self.assertIn(b"GDepth:Mime", xmp)
        self.assertIn(b"x:xmpmeta", xmp)

if __name__ == '__main__':
    unittest.main()
