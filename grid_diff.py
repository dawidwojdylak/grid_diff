import cv2

if __name__ == "__main__":
    img = cv2.imread('examples/01_bird_norm.png')

    cv2.namedWindow('Image grid difference app', cv2.WINDOW_NORMAL)
    cv2.imshow('Image grid difference app', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
