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
	img = img.astype(np.float64)
	height, width = img.shape
	
	while width >= 4:
		print("width", width)
		offset = width
		while offset >= 2:
			print("\toffset", offset)
			img[0:width, 0:width] = np.dot(img[0:width, 0:width], getM(width, offset))
			offset //= 2

		offset = width
		while offset >= 2:
			img[0:width, 0:width] = np.dot(getM(width, offset).T, img[0:width, 0:width])
			offset //= 2

		width //= 2

		break

	img[(threshold1 < img) & (img < threshold2)] = 0

	return img

def wavelet_decode(img):
	height, width = img.shape

	width2 = width
	while width2 <= width:
		print("width", width2)
		offset = 2
		while offset <= width2:
			print("\toffset", offset)
			img[0:width2, 0:width2] = np.dot(np.linalg.inv(getM(width2, offset).T), img[0:width2, 0:width2])
			offset *= 2

		offset = 2
		while offset <= width2:
			img[0:width2, 0:width2] = np.dot(img[0:width2, 0:width2], np.linalg.inv(getM(width2, offset)))
			offset *= 2

		width2 *= 2

	return img

