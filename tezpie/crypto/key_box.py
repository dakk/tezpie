import binascii
from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import HexEncoder

class KeyBox:
	def __init__ (self, remote_nonce, remote_pubkey, local_nonce, local_seckey):
		self.remote_nonce = remote_nonce
		self.local_nonce = local_nonce
		self.box = Box(PrivateKey(local_seckey, HexEncoder), PublicKey(remote_pubkey, HexEncoder))

	def native_box(self):
		return self.box

	def decrypt(self, encdata):
		data = self.box.decrypt(encdata, self.remote_nonce.get())
		self.remote_nonce.increment()
		return data

	def encrypt(self, data):
		encdata = self.box.encrypt(data, self.local_nonce.get())[24::]
		self.local_nonce.increment()
		return encdata

	def shared_key(self):
		return binascii.hexlify(self.box.shared_key()).decode('ascii')