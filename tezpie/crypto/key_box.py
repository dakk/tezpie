class KeyBox:
    def __init__ (self, remote_nonce, remote_pubkey, local_nonce, local_seckey):
        self.remote_pubkey = remote_pubkey
		self.remote_nonce = remote_nonce
        self.local_seckey = local_seckey
		self.local_nonce = local_nonce

    def decrypt(self, data):
        pass
		self.remote_nonce.increment()

    def encrypt(self, data):
        pass
		self.local_nonce.increment()