import sys
import cv2
import numpy as np

class PictureComparator:
    """
    A class for comparing two images, pixel by pixel.
    """
    TITLE = "Image grid difference app"
    TEXT_COLOR = (0, 0, 255)
    
    def __init__(self, img1 = None, img2 = None):
        """
        Initializes a class instance with images to be compared.

        Args:
            img1 (numpy.ndarray) : first image
            img2 (numpy.ndarray) : second image
        """
        self.img1 = img1
        self.img2 = img2

        if self.img1.shape != self.img2.shape:
            raise ValueError("Images are different size")
        
        self.diff_avg = None
        self.tolerance = None

    def setTolerance(self, tol):
        """
        Sets pixel comparison tolerance.

        Args:
            tol (int) : Pixel comparison tolerance
        """
        if tol is not None and (tol > 255 or tol < 0):
            raise ValueError("Tolerance should be in range [0, 255]")
        self.tolerance = tol
        
    def getDiffImg(self):
        """
        Returns compared image with differences marked red and printed difference percentage.

        Returns:
            Compared image
        """
        diff_percentage = self.calculateDiffPixels()
        masked_img = self.mergeDiffImage()
        masked_img[self.diff_avg != 0, :2] = 0
        diff_perc_txt = "{:.2f}%".format(round(diff_percentage, 2))
        diff_img = self.addText(masked_img, diff_perc_txt)
        return diff_img

    def calculateDiffPixels(self):
        """
        Computes an array of differences and merges BGR colors layers to one layer of average values. 

        Returns:
            The percentage difference value 
        """
        self.diff = cv2.absdiff(self.img1, self.img2)
        self.diff_avg = np.mean(self.diff, axis=2)
        if self.tolerance: self.diff_avg = self.diff_avg > self.tolerance
        diff_pix = np.count_nonzero(self.diff_avg)
        total = self.diff_avg.shape[0] * self.diff_avg.shape[1]
        self.percentage_diff = diff_pix / total * 100.
        return self.percentage_diff

    def getTranspDiffImage(self):
        """
        Computes a transparent mask with different pixels marked red.

        Returns:
            A transparent mask with different pixels marked red
        """
        if self.diff_avg is None:
            self.calculateDiffPixels()

        matching_pixels = np.where(self.diff_avg == 0., 255., 0.).astype(np.uint8)
        different_pixels = np.where(self.diff_avg != 0., 255., 0.).astype(np.uint8)

        diff_mask = np.zeros((self.img1.shape[0], self.img1.shape[1], 4), dtype=np.uint8)
        diff_mask[:,:,2] = different_pixels
        diff_mask[:,:,3] = matching_pixels

        return diff_mask
    
    def mergeDiffImage(self):
        """
        Merges (first) original image with a red mask.

        Returns:
            Original image with differences marked red.
        """
        diff_mask = self.getTranspDiffImage()
        original_img = cv2.cvtColor(self.img1, cv2.COLOR_BGR2BGRA)
        masked = cv2.bitwise_or(original_img, diff_mask)
        return masked
    
    @staticmethod
    def addText(img, text):
        """
        Adds red text to the image.

        Args:
            img (numpy.ndarray) : image
            text (str) : text

        Returns:
            Image with text
        """
        font = cv2.FONT_HERSHEY_COMPLEX
        scale = 3
        thickness = 4
        text_size, _ = cv2.getTextSize(text, font, scale, thickness)
        x = int((img.shape[1] - text_size[0]) / 2)
        y = int((img.shape[0] + text_size[1]) / 2)
        text_img = cv2.putText(img=img, text=text, org=(x, y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=scale, color=PictureComparator.TEXT_COLOR, thickness=thickness)
        return text_img
    

    @staticmethod
    def showImage(img, title="Title"):
        """
        Shows image in window.

        Args:
            img (numpy.ndarray) : image
            title (str) : window title
        """
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.imshow(title, img)

        while cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) >= 1:
            keyCode = cv2.waitKey(1000)
            if (keyCode & 0xFF) == ord("q"):
                cv2.destroyAllWindows()
                break
    
    @staticmethod
    def printLayers(img, prefix=""):
        """
        Prints color layers for debug purposes.

        Args:
            img (numpy.ndarray) : image
            prefix (str) : prefix printed before color layers
        """
        print(prefix)
        for i in range(img.shape[2]):
            print(f"Layer {i}:")
            print(img[:,:,i])

