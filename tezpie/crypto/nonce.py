import struct
import random
import binascii
import nacl
from nacl.hash import blake2b
from nacl.encoding import RawEncoder


class Nonce:
	SIZE = 24

	def __init__(self):
		self.nonce = 0

	def from_hex(h, endianess="big"):
		return Nonce.from_bin(binascii.unhexlify(h), endianess)

	def from_bin(h, endianess="big"):
		n = Nonce()
		n.nonce = int.from_bytes(h, endianess)
		return n

	def random():
		rn = nacl.utils.random(Nonce.SIZE)
		return Nonce.from_bin(rn)

	def generate(sent, recv, incoming = False):
		if incoming:
			init_msg = recv
			resp_msg = sent
		else:
			init_msg = sent
			resp_msg = recv

		print ('gennonces')
		nonce_init_to_resp = blake2b(init_msg + resp_msg + b"Init -> Resp", encoder=RawEncoder)[0:Nonce.SIZE]
		nonce_resp_to_init = blake2b(init_msg + resp_msg + b"Resp -> Init", encoder=RawEncoder)[0:Nonce.SIZE]
		print(len(nonce_init_to_resp))
		a = Nonce.from_bin(nonce_init_to_resp, 'big')
		b = Nonce.from_bin(nonce_resp_to_init, 'big')

		return { 'local': a, 'remote': b } if incoming else { 'local': b, 'remote': a }		


	def increment(self):
		self.nonce += 1

	def __int__(self):
		return self.nonce

	def __repr__(self):
		return str(self.nonce)

	def get_hex(self):
		return binascii.hexlify(self.get()).decode('ascii')

	def get(self):
		return self.nonce.to_bytes(Nonce.SIZE, 'big')

	def get_and_increment(self):
		n = self.get()
		self.increment()
		return n