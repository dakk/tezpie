from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import HexEncoder

class KeyBox:
	def __init__ (self, remote_nonce, remote_pubkey, local_nonce, local_seckey):
		self.remote_nonce = remote_nonce
		self.local_nonce = local_nonce
		self.box = Box(PrivateKey(remote_pubkey, HexEncoder), PublicKey(local_seckey, HexEncoder))

	def decrypt(self, encdata):
		data = self.box.decrypt(encdata, self.remote_nonce.get_unhex())
		self.remote_nonce.increment()
		return data

	def encrypt(self, data):
		encdata = self.box.encrypt(data, self.local_nonce.get_unhex())
		self.local_nonce.increment()
		return encdata