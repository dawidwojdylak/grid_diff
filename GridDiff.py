import sys
import cv2
import numpy as np

from PictureComparator import PictureComparator

class GridDiff:
    """
    A class for slicing two images into grid and comparing them with PictureComparator class. 
    """
    RED = (0, 0, 255)
    LINE_THICKNESS = 3

    def __init__(self, img1, img2):
        """
        Initializes a class instance with images to be sliced and compared.

        Args:
            img1 (numpy.ndarray) : first image
            img2 (numpy.ndarray) : second image
        """
        self.img1 = img1
        self.img2 = img2

    def divideIntoGrid(self, n = 4, m = 4):
        """
        Slices images into (n x m) size grid.

        Args:
            n (int) : number of rows
            m (int) : number of columns
        """
        def divide(img, n, m):
            height = img.shape[0] // n
            width = img.shape[1] // m

            container = [[None for _ in range(m)] for _ in range(n)]

            for i in range(n):
                for j in range(m):
                    container[i][j] = img[i * height : (i+1) * height, j * width : (j+1) * width]

            return container
        
        self.img1_divided = divide(self.img1, n, m)
        self.img2_divided = divide(self.img2, n, m)

    def compareTiles(self, tolerance = None):
        """
        Compares slices using PictureComparator.

        Args:
            tolerance (int) : tolerance of calculating a difference between pixels

        Returns:
            A list of compared images.
        """
        n = len(self.img1_divided)
        m = len(self.img1_divided[0])
        self.comparedTiles = [[None for _ in range(m)] for _ in range(n)]

        for i in range(n):
            for j in range(m):
                comparator = PictureComparator(img1 = self.img1_divided[i][j], img2 = self.img2_divided[i][j])
                comparator.setTolerance(tolerance)
                diff_img = comparator.getDiffImg()
                diff_img = diff_img[:,:,0:3]
                self.comparedTiles[i][j] = diff_img

        return self.comparedTiles

    def mergeGrid(self, img_divided, red_lines : bool = True):
        """
        Merges sliced image into image of original size.

        Args:
            img_divided (list) : List of compared images
            red_lines (bool) : Check value if red grid lines should be drawn

        Returns:
            A merged image 
        """
        n = len(img_divided)
        m = len(img_divided[0])

        height, width, layers = img_divided[0][0].shape # type: ignore

        merged_img = np.zeros_like(self.img1)

        for i in range(n):
            for j in range(m):
                merged_img[i * height : (i + 1) * height, j * width : (j + 1) * width, :] = img_divided[i][j]
                if red_lines:
                    # horizontal
                    if i < n - 1:
                        cv2.line(merged_img, (j * width,      (i + 1) * height), 
                                            ((j + 1) * width, (i + 1) * height),
                                            self.RED, thickness=self.LINE_THICKNESS)
                    # vertical
                    if j < m - 1:
                        cv2.line(merged_img,((j + 1) * width, i * height), 
                                            ((j + 1) * width, (i + 1) * height),
                                            self.RED, thickness=self.LINE_THICKNESS)

        return merged_img
        
    