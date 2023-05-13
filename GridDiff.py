import sys
import cv2
import numpy as np

from PictureComparator import PictureComparator

class GridDiff:
    RED = (0, 0, 255)
    LINE_THICKNESS = 3

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

    def compareTiles(self):
        n = len(self.img1_divided)
        m = len(self.img1_divided[0])
        self.comparedTiles = [[None for _ in range(m)] for _ in range(n)]

        for i in range(n):
            for j in range(m):
                comparator = PictureComparator(img1 = self.img1_divided[i][j], img2 = self.img2_divided[i][j])
                diff_img = comparator.getDiffImg()
                diff_img = diff_img[:,:,0:3]
                self.comparedTiles[i][j] = diff_img

        return self.comparedTiles

    def mergeGrid(self, img_divided, red_lines : bool = True):
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
        
    



def debug(diff):
    diff.divideIntoGrid(4, 4)
    compared = diff.compareTiles()
    merged = diff.mergeGrid(compared)
    PictureComparator.showImage(merged)
    # TODO: make font size adjust automatically

if __name__ == "__main__":
    if len(sys.argv) != 3:
        diff = GridDiff('examples/01_bird_norm.png', 'examples/01_bird_edit.png')
    else:
        diff = GridDiff(sys.argv[1], sys.argv[2])
    debug(diff)