import random
# I pledge my honor that I have abided by the Stevens Honor System. - Eric Altenburg
# For the lab, complete modexp(), RSA_enc(), and RSA_dec().
# HW 2 will allow you to submit the fully completed code from the lab,
#   as well as egcd(), mulinv(), and keygen(), for extra credit on the
#   assignment.
# You must work independently since this assignment will be part of HW 2.

# test constants
test_p = 23
test_q = 47
test_e =  35
test_d = 347
message = "Hello world!"

def calc_n(p, q):
	# do not modify!
	return p * q

def calc_phi(p, q):
	# do not modify!
	return (p - 1) * (q - 1)

def modexp(b, e, m):
	# returns b^e % m efficiently
	# use the binary modular exponentiation algorithm explained in the lab slides
	# Complete this part during the lab
	temp = 1

	b = b % m

	if (b == 0):
		return 0

	while (e > 0):
		if (e % 2 == 1):
			temp = (temp * b) % m

		e = e >> 1
		b = (b * b) % m

	return temp

def RSA_enc(plaintext, key):
	# key should be a tuple (n, e)
	# the ord() function will be useful here
	# we recommend extracting the components of the key from the tuple for efficiency purposes
	# return a list of integers
	# Complete this part during the lab

	ciphertext = []

	for p in plaintext:
		ciphertext += [modexp(ord(p), key[1], key[0])]

	return ciphertext

def RSA_dec(ciphertext, key):
	# key should be a tuple (n, e)
	# the chr() function will be useful here
	# we recommend extracting the components of the key from the tuple for efficiency purposes
	# return a string
	# Complete this part during the lab

	plaintext = ''

	for c in ciphertext:
		plaintext += chr(modexp(c, key[1], key[0]))

	return plaintext

def test():
	# do not modify!
	n	   = calc_n(test_p, test_q)
	private = [n, test_d]
	public  = [n, test_e]
	
	print("Public key:",public)
	print("Private key:",private)
	
	ciphertext = RSA_enc(message,public)
	plaintext  = RSA_dec(ciphertext,private)

	print("Original message:",message)
	print("Encrypted message:",ciphertext)
	print("Decrypted message:",plaintext)

# === Below this comment is the portions of this assignment that contribute to HW 2 ===

def egcd(b, n):
	# runs the extended Euclidean algorithm on b and n
	# returns a triple (g, x, y) s.t. bx + ny = g = gcd(b, n)
	# review the extended Euclidean algorithm on Wikipedia
	# Complete for HW 2 extra credit
	
	if (n == 0):
		return (b, 1, 0)

	(tempg, tempx, tempy) = egcd(n, b % n)

	(g, x, y) = (tempg, tempy, tempx - (b // n) * tempy)

	return (g, x, y)

def mulinv(e, n):
	# returns the multiplicative inverse of e in n
	 # make use of the egcd above
	 # Complete for HW 2 extra credit

	(g, x, y) = egcd(e, n)

	if (g != 1):
		raise Exception("No inverse exists")

	return x % n

def checkprime(n, size):
	# do not modify!
	# determine if a number is prime
	if n % 2 == 0 or n % 3 == 0: return False
	i = 0

	# fermat primality test, complexity ~(log n)^4
	while i < size:
		if modexp(random.randint(1, n - 1), n - 1, n) != 1: return False
		i += 1

	# division primality test
	i = 5
	while i * i <= n:
		if n % i == 0: return False
		i += 2
		if n % i == 0: return False
		i += 4
	return True

def primegen(size):
	# do not modify!
	# generates a <size> digit prime
	if(size == 1): return random.choice([2, 3, 5, 7])
	lower = 10 ** (size - 1)
	upper = 10 ** size - 1
	p = random.randint(lower, upper)
	p -= (p % 6)
	p += 1
	if p < lower: p += 6
	elif p > upper: p -= 6
	q = p - 2
	while p < upper or q > lower:
		if p < upper:
			if checkprime(p, size): return p
			p += 4
		if q > lower:
			if checkprime(q, size): return q
			q -= 4
		if p < upper:
			if checkprime(p, size): return p
			p += 2
		if q > lower:
			if checkprime(q, size): return q
			q -= 2
		

def keygen(size):
	# generate a random public/private key pair
	# size is the digits in the rsa modulus, approximately. must be even, >2
	# return a tuple of tuples, [[n, e], [n, d]]
	# Complete this for HW 2 extra credit
	assert(size % 2 == 0 and size > 2) # keep this line!

	p = primegen(size)
	q = primegen(size)

	n = calc_n(p, q)
	phi = calc_phi(p, q)

	for i in range(2, phi):
		(g, x, y) = egcd(i, phi)

		if (g == 1):
			e = i
			break

	d = mulinv(e, phi)

	return [[n, e], [n, d]]


def customkeytest(text, size):
	keypair = keygen(size)
	
	print("Public key:",keypair[0])
	print("Private key:",keypair[1])
	
	ciphertext = RSA_enc(text,keypair[0])
	plaintext  = RSA_dec(ciphertext,keypair[1])

	print("Original message:",text)
	print("Encrypted message:",ciphertext)
	print("Decrypted message:",plaintext)

# for testing
# def main():
# 	test()
# 	customkeytest("We out here!", 12)

# if __name__ == "__main__":
# 	main()