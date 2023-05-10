import sys
import cv2
import numpy as np

class PictureComparator:
    TITLE = "Image grid difference app"
    
    def __init__(self, path1 : str, path2 : str):
        self.img1 = cv2.imread(path1)
        self.img2 = cv2.imread(path2)
        if self.img1 is None: 
            raise FileNotFoundError(f"Failed to read image {path1}")
        elif self.img2 is None:
            raise FileNotFoundError(f"Failed to read image {path2}")

    def showImage(self, img, title):
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def calculateDiffPixels(self):
        if self.img1.shape != self.img2.shape:
            raise ValueError("Images are different size")
        self.diff = cv2.absdiff(self.img1, self.img2)
        avg = np.mean(self.diff, axis=2)
        diff_pix = np.count_nonzero(avg)
        total = avg.shape[0] * avg.shape[1]
        self.percentage_diff = diff_pix / total * 100.
        print("Difference: {:.2f}%".format(round(self.percentage_diff, 2)))

    def showDifference(self):
        try:
            self.showImage(self.diff, "Difference image")
        except AttributeError:
            print("Calculate the difference!")

def debug(comp):
    comp.calculateDiffPixels()
    comp.showDifference()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        comp = PictureComparator('examples/01_bird_norm.png', 'examples/01_bird_edit.png')
    else:
        comp = PictureComparator(sys.argv[1], sys.argv[2])
    debug(comp)

