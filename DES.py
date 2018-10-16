# this function returns the input left shifted once
def left_shift(to_shift):
	tmp = to_shift[0]
	to_shift = to_shift[1:]
	to_shift = to_shift+(tmp)
	return to_shift

# the following permutation functions take in a string as the argument and handles the permutation via concatenation

# the following 2 permutation functions are for the key generation
def p10(initial_p): # permutation for 10 bit keys
	# 3 5 2 7 4 10 1 9 8 6
	final_p = initial_p[2] + initial_p[4] + initial_p[1] + initial_p[6] + initial_p[3] + initial_p[9] + initial_p[0] + initial_p[8] + initial_p[7] + initial_p[5]
	return final_p

def p8(initial_p): 
	# 6 3 7 4 8 5 10 9
	final_p = initial_p[5] + initial_p[2] + initial_p[6] + initial_p[3] + initial_p[7] + initial_p[4] + initial_p[9] + initial_p[8]
	return final_p

# these permutations are used in the actual encryption/decryption
def initial_p(initial_p): # initial permutation
	# 2 6 3 1 4 8 5 7
	final_p = initial_p[1] + initial_p[5] + initial_p[2] + initial_p[0] + initial_p[3] + initial_p[7] + initial_p[4] + initial_p[6]
	return final_p

def inverseInitialP(initial_p):
	# 2 4 3 1
	final_p = initial_p[1] + initial_p[3] + initial_p[2] + initial_p[0]
	return final_p

# the following 2 functions act as the s boxes
def s0(initial4bit):
	# grab the letters at respective indices and concatenate and convert to base 2 int
	row = int((initial4bit[1]+initial4bit[2]),2)
	col = int((initial4bit[0]+initial4bit[3]),2)

	s0_box = [[1, 0, 3, 2],\
			  [3, 2, 1, 0],\
			  [0, 2, 1, 3],\
			  [3, 1, 3, 2]]

	# get the value from s box of calculated row and col
	s_val = s0_box[row][col]
	# convert to binary
	bin_sval = bin(s_val)

	# return 4 bit val
	return bin_sval[2:].zfill(2)


def s1(initial4bit):
	# grab the letters at respective indices and concatenate and convert to base 2 int
	row = int((initial4bit[1]+initial4bit[2]),2)
	col = int((initial4bit[0]+initial4bit[3]),2)

	s1_box = [[0, 1, 2, 3],\
			  [2, 0, 1, 3],\
			  [3, 0, 1, 0],\
			  [2, 1, 0, 3]]

	# get the value from s box of calculated row and col
	s_val = s1_box[row][col]
	# convert to binary
	bin_sval = bin(s_val)

	# return 4 bit val
	return bin_sval[2:].zfill(2)


def f_func(x, k):
	# first expand/permutate x
	# 4 1 2 3
	first_x = x[3] + x[0] + x[1] + x[2]

	# 2 3 4 1
	last_x = x[1] + x[2] + x[3] + x[0]

	# concatenate and xor new value with key after converting to int base 2
	total_p = first_x + last_x
	xor_ed = int(total_p,2) ^ int(k,2) 
	xor_ed = "{:b}".format(xor_ed) # convert to binary

	# make sure its still 4 digits
	first4 = xor_ed[:4].zfill(4)
	last4 = xor_ed[4:].zfill(4)

	# pass to respective s boxes
	s0_val = s0(first4)
	s1_val = s1(last4)

	# concatenate
	sol = s0_val + s1_val

	# last permutation
	p4 = inverseInitialP(sol)

	return p4


def generateKeys(key10bit):
	# generate K1, K2 

	# permutate
	perm10 = p10(key10bit)

	first5 = perm10[:5]
	last5 = perm10[5:]

	# shift left and find k1
	shifted_first = left_shift(first5)
	shifted_last = left_shift(last5)

	k1 = p8(shifted_first + shifted_last)

	# shift left again and find k2
	shifted_first = left_shift(shifted_first)
	shifted_last = left_shift(shifted_last)

	k2 = p8(shifted_first + shifted_last)

	return k1, k2



def encrypt(plain8bit, k1, k2):
	# implement initial permutation
	perm8 = initial_p(plain8bit)

	# split
	first4 = perm8[:4]
	last4 = perm8[4:]

	# send the latter to the f function with first key
	f_last4 = f_func(last4, k1)

	# xor new value with key after converting to int base 2
	xor1 = int(first4,2) ^ int(f_last4,2) 
	xor1 = "{:b}".format(xor1).zfill(4)

	# send to f function with second key
	f_xor1 = f_func(xor1, k2)

	# xor the returned value with the original latter half
	xor2 = int(f_xor1,2) ^ int(last4,2) 
	xor2 = "{:b}".format(xor2).zfill(4)

	# concatenate
	final = str(xor2) + str(xor1) 

	#final permutation
	# 4 1 3 5 7 2 8 6
	cipher_text = final[3] + final[0] + final[2] + final[4] + final[6] + final[1] + final[7] + final[5]
	print("Here is the encrypted cipher text: "+cipher_text)
	return cipher_text


def decrypt(cipher8bit, k1, k2):
	# implement initial permutation
	perm8 = initial_p(cipher8bit)

	# split
	first4 = perm8[:4]
	last4 = perm8[4:]

	# send the latter to the f function with second key
	f_last4 = f_func(last4, k2)

	# xor new value with key after converting to int base 2
	xor1 = int(first4,2) ^ int(f_last4,2) 
	xor1 = "{:b}".format(xor1).zfill(4)

	# send to f function with first key
	f_xor1 = f_func(xor1, k1)

	# xor the returned value with the original latter half
	xor2 = int(f_xor1,2) ^ int(last4,2) 
	xor2 = "{:b}".format(xor2).zfill(4)

	# concatenate
	final = str(xor2) + str(xor1) 

	# 4 1 3 5 7 2 8 6
	plain_text = final[3] + final[0] + final[2] + final[4] + final[6] + final[1] + final[7] + final[5]
	print("Here is the decrypted plain text: "+plain_text)
	return plain_text


