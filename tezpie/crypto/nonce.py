import struct
import random
import binascii
import nacl
from nacl.hash import blake2b

class Nonce:
	SIZE = 24
	INIT_TO_RESP_SEED = b"Init -> Resp"
	RESP_TO_INIT_SEED = b"Resp -> Init";

	def __init__(self, h):
		self.nonce = int.from_bytes(binascii.unhexlify(h), 'big')

	def random():
		rn = nacl.utils.random(Nonce.SIZE)
		return Nonce(binascii.hexlify(rn))

	def generate(sent, recv, incoming = False):
		if incoming:
			init_msg = recv
			resp_msg = sent
		else:
			init_msg = sent
			resp_msg = recv

		nonce_init_to_resp = blake2b(init_msg + resp_msg + Nonce.INIT_TO_RESP_SEED)[0:Nonce.SIZE]
		nonce_resp_to_init = blake2b(init_msg + resp_msg + Nonce.RESP_TO_INIT_SEED)[0:Nonce.SIZE]

		if incoming:
			[Nonce(nonce_init_to_resp), Nonce(nonce_resp_to_init)]
		else:
			[Nonce(nonce_resp_to_init), Nonce(nonce_init_to_resp)]
		


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