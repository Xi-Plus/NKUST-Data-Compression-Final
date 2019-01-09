import sys
import os
import math
import time
import cv2
from XIPLUS03 import *


algolist = {
	"auto": [],
	"xp03": [[XIPLUS03_encode, [-2, 2, 32]], [XIPLUS03_decode, []]],
}


ctype = sys.argv[1]
algo = sys.argv[2].lower()
finname = sys.argv[3]
foutname = sys.argv[4]

if ctype == "encode":
	if algo not in algolist:
		exit("alog not found")
	print("encode by {}".format(algo))

	oldsize = os.path.getsize(finname)
	print("old size: {}".format(oldsize))
	start = time.time()
	if algo == "auto":
		pass
	else:
		algolist[algo][0][0](finname, foutname, *algolist[algo][0][1])

	print("spend {} s".format(time.time()-start))
	newsize = os.path.getsize(foutname)
	print("new size: {}".format(newsize))
	print("compression ratio: {}".format(oldsize/newsize))

elif ctype == "decode":
	if algo not in algolist:
		exit("alog not found")
	print("decode by {}".format(algo))

	oldsize = os.path.getsize(finname)
	print("old size: {}".format(oldsize))
	start = time.time()
	if algo == "auto":
		pass
	else:
		algolist[algo][1][0](finname, foutname, *algolist[algo][1][1])

	print("spend {} s".format(time.time()-start))
	newsize = os.path.getsize(foutname)
	print("new size: {}".format(newsize))
else:
	print("nothing to do")
