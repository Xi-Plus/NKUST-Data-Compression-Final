import sys
import os
import math
import time
import cv2
from XIPLUS03 import *
from XIPLUS04 import *


algolist = {
	"auto": [],
	"xp03": [[XIPLUS03_encode, [-2, 2, 32, True]], [XIPLUS03_decode, [True]]],
	"xp04": [[XIPLUS04_encode, [-2, 2, 32, True]], [XIPLUS04_decode, [True]]],
}

ctype = sys.argv[1]

if ctype == "encode":
	algo = sys.argv[2].lower()
	finname = sys.argv[3]
	foutname = sys.argv[4]

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
	algo = sys.argv[2].lower()
	finname = sys.argv[3]
	foutname = sys.argv[4]

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

elif ctype == "error":
	fname1 = sys.argv[2]
	fname2 = sys.argv[3]

	img1 = cv2.imread(fname1, cv2.IMREAD_UNCHANGED)
	img2 = cv2.imread(fname2, cv2.IMREAD_UNCHANGED)

	diff = img2 - img1
	print("error", math.sqrt(np.average(np.square(diff))))

else:
	print("nothing to do")
