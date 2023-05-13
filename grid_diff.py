import sys
import cv2
import numpy as np

class PictureComparator:
    TITLE = "Image grid difference app"
    
    def __init__(self, path1 : str, path2 : str):
        self.img1 = cv2.imread(path1)
        self.img2 = cv2.imread(path2)

        self.diff_avg = None

        if self.img1 is None: 
            raise FileNotFoundError(f"Failed to read image {path1}")
        elif self.img2 is None:
            raise FileNotFoundError(f"Failed to read image {path2}")
        if self.img1.shape != self.img2.shape:
            raise ValueError("Images are different size")

    @staticmethod
    def showImage(img, title):
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def calculateDiffPixels(self):
        self.diff = cv2.absdiff(self.img1, self.img2)
        self.diff_avg = np.mean(self.diff, axis=2)
        diff_pix = np.count_nonzero(self.diff_avg)
        total = self.diff_avg.shape[0] * self.diff_avg.shape[1]
        self.percentage_diff = diff_pix / total * 100.
        print("Difference: {:.2f}%".format(round(self.percentage_diff, 2)))

    def getTranspDiffImage(self):
        if self.diff_avg is None:
            self.calculateDiffPixels()

        matching_pixels = np.where(self.diff_avg == 0., 255., 0.).astype(np.uint8)
        different_pixels = np.where(self.diff_avg != 0., 255., 0.).astype(np.uint8)

        diff_mask = np.zeros((self.img1.shape[0], self.img1.shape[1], 4), dtype=np.uint8)
        diff_mask[:,:,2] = different_pixels
        diff_mask[:,:,3] = matching_pixels

        return diff_mask
    
    def mergeDiffImage(self):
        diff_mask = self.getTranspDiffImage()
        original_img = cv2.cvtColor(self.img1, cv2.COLOR_BGR2BGRA)
        masked = cv2.bitwise_or(original_img, diff_mask)
        return masked
    
    def showDifference(self):
        try:
            self.showImage(self.diff, "Difference image")
        except AttributeError:
            print("Calculate the difference!")
    
    @staticmethod
    def printLayers(img, prefix=""):
        print(prefix)
        for i in range(img.shape[2]):
            print(f"Layer {i}:")
            print(img[:,:,i])

def debug(comp):
    comp.calculateDiffPixels()
    # comp.getTranspDiffImage()
    comp.showImage(comp.mergeDiffImage(), "Masked image") 


if __name__ == "__main__":
    if len(sys.argv) != 3:
        comp = PictureComparator('examples/01_bird_norm.png', 'examples/01_bird_edit.png')
    else:
        comp = PictureComparator(sys.argv[1], sys.argv[2])
    debug(comp)

