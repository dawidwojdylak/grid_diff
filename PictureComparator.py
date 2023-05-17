import sys
import cv2
import numpy as np

class PictureComparator:
    TITLE = "Image grid difference app"
    TEXT_COLOR = (0, 0, 255)
    
    def __init__(self, img1 = None, img2 = None):
        self.img1 = img1
        self.img2 = img2

        if self.img1.shape != self.img2.shape:
            raise ValueError("Images are different size")
        
        self.diff_avg = None
        
    def getDiffImg(self):
        diff_percentage = self.calculateDiffPixels()
        masked_img = self.mergeDiffImage()
        diff_perc_txt = "{:.2f}%".format(round(diff_percentage, 2))
        diff_img = self.addText(masked_img, diff_perc_txt)
        return diff_img

    def calculateDiffPixels(self):
        self.diff = cv2.absdiff(self.img1, self.img2)
        self.diff_avg = np.mean(self.diff, axis=2)
        diff_pix = np.count_nonzero(self.diff_avg)
        total = self.diff_avg.shape[0] * self.diff_avg.shape[1]
        self.percentage_diff = diff_pix / total * 100.
        print("Difference: {:.2f}%".format(round(self.percentage_diff, 2)))
        return self.percentage_diff

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
    
    def setImages(self, img1 : np.ndarray, img2 : np.ndarray):
        self.img1 = img1
        self.img2 = img2
    
    @staticmethod
    def addText(img, text):
        font = cv2.FONT_HERSHEY_COMPLEX
        scale = 3
        thickness = 4
        text_size, _ = cv2.getTextSize(text, font, scale, thickness)
        x = int((img.shape[1] - text_size[0]) / 2)
        y = int((img.shape[0] + text_size[1]) / 2)
        text_img = cv2.putText(img=img, text=text, org=(x, y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=scale, color=PictureComparator.TEXT_COLOR, thickness=thickness)
        return text_img
    
    def showDifference(self):
        try:
            self.showImage(self.diff, "Difference image")
        except AttributeError:
            print("Calculate the difference!")

    @staticmethod
    def showImage(img, title="Title"):
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    @staticmethod
    def printLayers(img, prefix=""):
        print(prefix)
        for i in range(img.shape[2]):
            print(f"Layer {i}:")
            print(img[:,:,i])

