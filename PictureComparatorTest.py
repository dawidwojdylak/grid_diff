import unittest
import numpy as np
from PictureComparator import PictureComparator

class PictureComparatorTest(unittest.TestCase):
    def setUp(self):
        self.img1 = np.array([[[128, 0, 0  ], [0, 255, 255]],
                              [[0  , 255, 0], [0,   0, 255]]], dtype=np.uint8)

        self.img2 = np.array([[[128,   0, 0], [0,   0, 255]],
                              [[0  , 250, 0], [0,   0, 255]]], dtype=np.uint8)

    def testGetDiffImg(self):
        comparator = PictureComparator(self.img1, self.img2)

        expected = np.array([ [[128, 0, 0  , 255], [0,   0, 255, 255]],
                              [[0  , 0, 255, 255], [0,   0, 255, 255]]])


        result = comparator.getDiffImg()
        np.testing.assert_array_equal(result, expected)

if __name__ == '__main__':
    unittest.main()