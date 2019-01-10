import cv2

infile = "small.bmp"
outfile = "small2.bmp"
img = cv2.imread(infile, cv2.IMREAD_UNCHANGED)
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cv2.imwrite(outfile, img)
