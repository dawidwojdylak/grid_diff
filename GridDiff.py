import sys
import cv2
import numpy as np

from PictureComparator import PictureComparator

class GridDiff:
    def __init__(self, path1 : str, path2 : str):
        self.img1 = cv2.imread(path1)
        self.img2 = cv2.imread(path2)

        if self.img1 is None: 
            raise FileNotFoundError(f"Failed to read image {path1}")
        elif self.img2 is None:
            raise FileNotFoundError(f"Failed to read image {path2}")
        
        if self.img1.shape != self.img2.shape:
            if self.img1.shape[0] * self.img1.shape[1] > self.img2.shape[0] * self.img2.shape[1]:
                self.img1 = cv2.resize(self.img1, (self.img2.shape[1], self.img2.shape[0]))
            else:
                self.img2 = cv2.resize(self.img2, (self.img1.shape[1], self.img1.shape[0]))


def debug(diff):
    pass

if __name__ == "__main__":
    if len(sys.argv) != 3:
        diff = GridDiff('examples/01_bird_norm.png', 'examples/01_bird_edit.png')
    else:
        diff = GridDiff(sys.argv[1], sys.argv[2])
    debug(diff)