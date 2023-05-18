import argparse
from PictureComparator import PictureComparator
from GridDiff import GridDiff
import cv2

def parse():
    parser = argparse.ArgumentParser()
    parser.description = "Script to show difference between two images."
    parser.add_argument("img1", type=str, help="1st image path")
    parser.add_argument("img2", type=str, help="2nd image path")
    parser.add_argument("-g", "--grid", nargs=2, metavar=('rows', 'cols'), default=None, help="Grid size (rows x cols)", type=int)
    parser.add_argument("-o", "--output", type=str, help="Output image path")
    parser.add_argument("-t", "--tolerance", type=int, help="Pixel comparison tolerance")

    args = parser.parse_args()
    return args

def compare(img1_path, img2_path, dimensions, output, tolerance):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None: 
        raise FileNotFoundError(f"Failed to read image {img1_path}")
    elif img2 is None:
        raise FileNotFoundError(f"Failed to read image {img2_path}")

    if dimensions is None:
        comp = PictureComparator(img1, img2)
        comp.setTolerance(tolerance)
        img = comp.getDiffImg()
        if output is not None:
            cv2.imwrite(output, img)
        comp.showImage(img, comp.TITLE)

    else:
        gridDiff = GridDiff(img1, img2)
        gridDiff.divideIntoGrid(dimensions[0], dimensions[1])
        compared = gridDiff.compareTiles(tolerance)
        merged = gridDiff.mergeGrid(compared)
        if output is not None:
            cv2.imwrite(output, merged)
        PictureComparator.showImage(merged)

    

if __name__ == "__main__":
    args = parse()
    compare(args.img1, args.img2, args.grid, args.output, args.tolerance)