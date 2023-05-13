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

    def divideIntoGrid(self, n = 4, m = 4):
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

    def mergeGrid(self):
        def merge(img_divided):
            n = len(img_divided)
            m = len(img_divided[0])

            height, width, layers = img_divided[0][0].shape # type: ignore

            merged_img = np.zeros_like(self.img1)

            for i in range(n):
                for j in range(m):
                    merged_img[i * height : (i + 1) * height, j * width : (j + 1) * width, :] = img_divided[i][j]
            
            return merged_img
        
        return merge(self.img1_divided), merge(self.img2_divided) 




def debug(diff):
    diff.divideIntoGrid()
    pic1, pic2 = diff.mergeGrid()
    PictureComparator.showImage(pic1)
    PictureComparator.showImage(pic2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        diff = GridDiff('examples/01_bird_norm.png', 'examples/01_bird_edit.png')
    else:
        diff = GridDiff(sys.argv[1], sys.argv[2])
    debug(diff)