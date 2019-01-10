import math


''' file format
	1 byte: number of chars - 1
	1 byte: length of code length (=k)
	char fixed code (1 byte)
		+ huffman code length (k bits)
		+ huffman code
		(number of chars times)
	encoded content
	1 byte: number of padding zero after content
'''

def huffman_encode(infile, outfile):
	print("----- huffman_encode -----")
	with open(infile, "rb") as fin:
		string = fin.read()

	with open(outfile, "wb") as fout:
		# string = string.decode()

		dic = {}
		for c in string:
			if c not in dic:
				dic[c] = 1
			else:
				dic[c] += 1

		# if there are no char, add a placeholder
		print("\tthere are {} chars".format(len(dic)))
		if len(dic) == 0:
			dic[0] = 0
		fout.write(bytes([len(dic)-1]))

		dicpool = []
		for c in dic:
			dicpool.append(Node(c, dic[c]))

		if len(dicpool) == 1:
			dicpool.append(Node(None, 0))

		while len(dicpool) > 1:
			dicpool.sort(key=lambda v:v.weight)
			a = dicpool.pop(0)
			b = dicpool.pop(0)
			c = Node(None, a.weight+b.weight)
			c.left = a
			c.right = b
			a.parent = c
			a.code = '0'
			b.parent = c
			b.code = '1'
			dicpool.append(c)

		newdicpool = []
		while len(dicpool) > 0:
			c = dicpool.pop(0)
			a = c.left
			b = c.right
			if a is not None:
				a.code = c.code + a.code
				if a.char is None:
					dicpool.append(a)
				else:
					newdicpool.append(a)
				
			if b is not None:
				b.code = c.code + b.code
				if b.char is None:
					dicpool.append(b)
				else:
					newdicpool.append(b)

		newdicpool.sort(key=lambda v:v.char)
		maxcodelen = 0
		for node in newdicpool:
			maxcodelen = max(maxcodelen, len(node.code))
			# print("\t{}\t{:8}\t{}".format(repr(bytes([node.char])), node.code, node.weight))

		print("\tmaxcodelen =", maxcodelen)
		lofcl = math.ceil(math.log2(maxcodelen+1))
		print("\tlofcl =", lofcl)
		fout.write(bytes([lofcl]))

		temp = ""
		headersize = 0
		for node in newdicpool:
			temp += bin(node.char)[2:].zfill(8)
			temp += bin(len(node.code))[2:].zfill(lofcl)
			temp += node.code
			headersize += 8 + lofcl + len(node.code)

			while len(temp) >= 8:
				fout.write(bytes([int(temp[0:8], 2)]))
				temp = temp[8:]

		print("\theadersize(bits, bytes) =", headersize, headersize/8)

		# result = b''

		table = {}
		for node in newdicpool:
			table[node.char] = node.code

		# print(table)
		# temp = ''
		for char in string:
			temp += table[char]

			while len(temp) >= 8:
				fout.write(bytes([int(temp[0:8], 2)]))
				temp = temp[8:]

		paddingzerolen = (8-len(temp)%8)%8
		print("\tpaddingzerolen =", paddingzerolen)
		for i in range(paddingzerolen):
			temp += "0"

		while len(temp) >= 8:
			fout.write(bytes([int(temp[0:8], 2)]))
			temp = temp[8:]

		fout.write(bytes([paddingzerolen]))

	print("----- huffman_encode -----")
	return True

def huffman_decode(infile, outfile):
	print("----- huffman_decode -----")
	with open(infile, "rb") as fin:
		data = fin.read()

	numberofchars = data[0] + 1
	print("\tnumberofchars =", numberofchars)
	lofcl = data[1]
	print("\tlofcl =", lofcl)
	paddingzerolen = data[-1]
	print("\tpaddingzerolen =", paddingzerolen)

	temp = ""
	for b in data[2:-1]:
		temp += bin(b)[2:].zfill(8)
		# print(len(temp))

	offset = 0
	dic = {}
	for x in range(numberofchars):
		char = int(temp[offset:offset+8], 2)
		offset += 8
		codelen = int(temp[offset:offset+lofcl], 2)
		offset += lofcl
		code = temp[offset:offset+codelen]
		offset += codelen

		# print("\t{}\t{:8}".format(repr(bytes([char])), code))
		dic[code] = char

	with open(outfile, "wb") as fout:
		nowcode = ""
		for i in range(offset, len(temp)-paddingzerolen):
			nowcode += temp[i]
			if nowcode in dic:
				fout.write(bytes([dic[nowcode]]))
				nowcode = ""

	# with open(outfile, "wb") as fout:
	print("----- huffman_decode -----")
	return True

class Node():
	def __init__(self, char, weight):
		self.code = ''
		self.char = char
		self.weight = weight
		self.parent = None
		self.left = None
		self.right = None

	def __repr__(self):
		if self.parent is None:
			return "({}, '{}', {}, None)".format(self.code, self.char, self.weight)
		return "({}, '{}', {}, {})".format(self.code, self.char, self.weight, self.parent.char)

if __name__ == '__main__':
	huffman_encode("BILL GATES")
