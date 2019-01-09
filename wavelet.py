import numpy as np


def getM(x, y):
	M = np.zeros((x, x))
	for r in range(y // 2):
		M[r * 2    , r         ] = 0.5
		M[r * 2 + 1, r         ] = 0.5
		M[r * 2    , r + y // 2] = 0.5
		M[r * 2 + 1, r + y // 2] = -0.5
	for r in range(y, x):
		M[r, r] = 1
	return M

def wavelet_encode(img, threshold1=-5, threshold2=5):
	height, width = img.shape
		
	offset = width
	while offset >= 2:
		img = np.dot(img, getM(width, offset))
		offset //= 2

	offset = width
	while offset >= 2:
		img = np.dot(getM(width, offset).T, img)
		offset //= 2

	img[(threshold1 < img) & (img < threshold2)] = 0

	return img

def wavelet_decode(img):
	height, width = img.shape

	offset = 2
	while offset <= width:
		img = np.dot(np.linalg.inv(getM(width, offset).T), img)
		offset *= 2

	offset = 2
	while offset <= width:
		img = np.dot(img, np.linalg.inv(getM(width, offset)))
		offset *= 2

	return img

