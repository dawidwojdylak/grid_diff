import sys
import cv2
import numpy as np

class PictureComparator:
    TITLE = "Image grid difference app"
    
    def __init__(self, path1 : str, path2 : str):
        self.img1 = cv2.imread(path1)
        self.img2 = cv2.imread(path2)

    def showImage(self, img, title):
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def calculateAbsDifference(self):
        self.diff = cv2.absdiff(self.img1, self.img2)
        nonzeros = np.count_nonzero(self.diff)
        total = np.prod(self.diff.shape)
        self.percentage_diff = nonzeros / total * 100.
        print("Difference: {:.2f}%".format(round(self.percentage_diff, 2)))

    def calculateDiffPixels(self):
        pass
        # comp_arr = np.all(self.img1, self.img2, axis=-1)
        # count_true = np.count_nonzero(comp_arr)
        # diff = count_true / comp_arr.size * 100
        # diff = 100 - diff
        # print(diff)
        
    
    def showDifference(self):
        try:
            self.showImage(self.diff, "Difference image")
        except AttributeError:
            print("Calculate the difference!")

def debug(comp):
    comp.calculateAbsDifference()
    comp.showDifference()
    comp.calculateDiffPixels()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        comp = PictureComparator('examples/01_bird_norm.png', 'examples/01_bird_edit.png')
    else:
        comp = PictureComparator(sys.argv[1], sys.argv[2])
    debug(comp)

