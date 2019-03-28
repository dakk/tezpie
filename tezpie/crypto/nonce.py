import struct
import random
import binascii
import nacl

class Nonce:
	def __init__(self, h):
		self.nonce = int.from_bytes(binascii.unhexlify(h), 'big')

	def random():
		rn = nacl.utils.random(24)
		return Nonce(binascii.hexlify(rn))

	def increment(self):
		self.nonce += 1

	def __int__(self):
		return self.nonce

	def __repr__(self):
		return str(self.nonce)

	def get(self):
		return binascii.hexlify(self.nonce.to_bytes(24, 'big'))

	def get_unhex(self):
		return self.nonce.to_bytes(24, 'big')

	def get_and_increment(self):
		n = self.get()
		self.increment()
		return n