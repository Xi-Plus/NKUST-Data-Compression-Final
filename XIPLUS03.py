import cv2
import math
from wavelet import *
from bisect import bisect_left


def XIPLUS03_encode(infile, outfile, threshold1, threshold2, kquantizer):
	img = cv2.imread(infile, cv2.IMREAD_GRAYSCALE)
	height, width = img.shape

	img = wavelet_encode(img, threshold1, threshold2)

	img = img.flatten()

	vmin = math.floor(img.min())
	vmax = math.ceil(img.max())
	vdis = (vmax - vmin) / kquantizer
	lenofbit = int(math.log2(kquantizer))

	print("size", height, width)
	print("v", vmin, vmax, vdis)
	print("lenofbit", lenofbit)

	quantizer = []
	for i in range(1, kquantizer+1):
		quantizer.append(vmin + vdis * i)

	with open(outfile, "wb") as fout:
		fout.write(height.to_bytes(2, 'big'))
		fout.write(width.to_bytes(2, 'big'))
		fout.write(vmin.to_bytes(2, 'big', signed=True))
		fout.write(vmax.to_bytes(2, 'big', signed=True))
		fout.write(kquantizer.to_bytes(1, 'big'))

		temp = ""
		for b in img:
			temp += bin(bisect_left(quantizer, b))[2:].zfill(lenofbit)

			while len(temp) >= 8:
				fout.write(bytes([int(temp[0:8], 2)]))
				temp = temp[8:]

		paddingzerolen = (8-len(temp)%8)%8
		for i in range(paddingzerolen):
			temp += "0"

		while len(temp) >= 8:
			fout.write(bytes([int(temp[0:8], 2)]))
			temp = temp[8:]


def XIPLUS03_decode(infile, outfile):
	with open(infile, "rb") as fin:
		data = fin.read()

	height = int.from_bytes(data[0:2], "big")
	width = int.from_bytes(data[2:4], "big")
	vmin = int.from_bytes(data[4:6], "big", signed=True)
	vmax = int.from_bytes(data[6:8], "big", signed=True)
	kquantizer = int.from_bytes(data[8:9], "big")

	lenofbit = int(math.log2(kquantizer))
	vdis = (vmax - vmin) / kquantizer

	print("size", height, width)
	print("v", vmin, vmax, vdis)
	print("lenofbit", lenofbit)

	quantizer = []
	for i in range(kquantizer+1):
		quantizer.append(vmin + vdis * i)

	for i in range(kquantizer):
		if quantizer[i] <= 0 and quantizer[i+1] > 0:
			quantizer[i] = 0
		else:
			quantizer[i] = round((quantizer[i] + quantizer[i+1]) / 2)

	img = []

	temp = ""
	for offset in range(9, len(data)):
		temp += bin(data[offset])[2:].zfill(8)
		while len(temp) >= lenofbit:
			img.append(quantizer[int(temp[0:lenofbit], 2)])
			temp = temp[lenofbit:]

	img = img[:height*width]

	img = np.array(img)
	img = img.reshape((height, width))

	img = wavelet_decode(img)

	cv2.imwrite(outfile, img)
