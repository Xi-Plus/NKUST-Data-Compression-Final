import cv2
import math
from bisect import bisect_left
from wavelet import *
from huffman import *


rn = 32
cn = 32

def XIPLUS04_encode(infile, outfile, threshold1, threshold2, kquantizer, usehuffman=False):
	img = cv2.imread(infile, cv2.IMREAD_UNCHANGED)
	if len(img.shape) == 2:
		channel = 1
		height, width = img.shape
	else:
		height, width, channel = img.shape

	print("size", height, width, channel)
	imgs = img.reshape((height, width, channel))

	with open(outfile, "wb") as fout:
		fout.write(height.to_bytes(2, 'big'))
		fout.write(width.to_bytes(2, 'big'))
		fout.write(channel.to_bytes(1, 'big'))
		fout.write(kquantizer.to_bytes(1, 'big'))

		for ichannel in range(channel):
			print("channel", ichannel)
			img = imgs[:,:,ichannel]
			imgall = wavelet_encode(img, threshold1, threshold2)

			for r in range(rn):
				for c in range(cn):
					print("r/c", r, c)
					img = imgall[int(r*height/rn):int((r+1)*height/rn), int(c*width/cn):int((c+1)*width/cn)].flatten()

					vmin = math.floor(img.min())
					vmax = math.ceil(img.max())
					vdis = (vmax - vmin) / kquantizer
					lenofbit = int(math.log2(kquantizer))

					print("v", vmin, vmax, vdis)
					print("lenofbit", lenofbit)

					fout.write(vmin.to_bytes(2, 'big', signed=True))
					fout.write(vmax.to_bytes(2, 'big', signed=True))

					quantizer = []
					for i in range(1, kquantizer+1):
						quantizer.append(vmin + vdis * i)

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

	if usehuffman:
		huffman_encode(outfile, outfile)

def XIPLUS04_decode(infile, outfile, usehuffman):
	if usehuffman:
		huffman_decode(infile, "temp.bin")
		infile = "temp.bin"

	with open(infile, "rb") as fin:
		data = fin.read()

	height = int.from_bytes(data[0:2], "big")
	width = int.from_bytes(data[2:4], "big")
	channel = int.from_bytes(data[4:5], "big")
	kquantizer = int.from_bytes(data[5:6], "big")

	lenofbit = int(math.log2(kquantizer))

	print("size", height, width)
	print("lenofbit", lenofbit)

	offset = 6

	imgs = []
	for ichannel in range(channel):
		print("channel", ichannel)

		imgall = np.empty((height, width))
		for r in range(rn):
			for c in range(cn):
				print("r/c", r, c)

				vmin = int.from_bytes(data[offset:offset+2], "big", signed=True)
				vmax = int.from_bytes(data[offset+2:offset+4], "big", signed=True)

				vdis = (vmax - vmin) / kquantizer

				print("v", vmin, vmax, vdis)

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
				for i in range(offset+4, offset+4+math.ceil(height*width//rn//cn*lenofbit/8)):
					temp += bin(data[i])[2:].zfill(8)
					while len(temp) >= lenofbit:
						img.append(quantizer[int(temp[0:lenofbit], 2)])
						temp = temp[lenofbit:]

				img = img[:height*width//4]

				img = np.array(img)
				img = img.reshape((height//rn, width//cn))

				imgall[int(r*height/rn):int((r+1)*height/rn), int(c*width/cn):int((c+1)*width/cn)] = img

				offset += 4 + math.ceil(height*width//rn//cn*lenofbit/8)

		imgall = imgall.astype(np.float64)
		imgall = wavelet_decode(imgall)
		imgall = imgall.astype(np.uint8)

		imgs.append(imgall)

	imgs = np.array(imgs)
	imgs = cv2.merge(imgs)

	cv2.imwrite(outfile, imgs)
