import nacl
import base58
from ..proto import constants

class KeyPair:
    ''' Class for key pairs (private and public) '''
    def __init__(self, priv, pub):
        self.pubKey = PublicKey(pub)
        self.privKey = PrivateKey(priv)

    @staticmethod
    def fromMnemonic(words):
        ''' Create a keypair from menmonic words '''
        return None

    @staticmethod
    def fromFundarising(email, password, words):
        ''' Create a keypair from fundraising data '''
        return None

    @staticmethod
    def generate():
        ''' Create a keypair from a random generated key '''
        (priv, pub) = crypto.randomKeys()
        priv = nacl.signing.SigningKey.generate()
        pub = priv.verify_key
        return KeyPair(priv, pub)

    def address(self):
        ''' Returns the string representation of the keypair address '''
        hk = self.pubKey.encode(encoder=nacl.encoding.HexEncoder)
        return base58.b58encode_check(constants.PREFIXES['tz1'] + hk)

    def sign(self, data):
        ''' Sign data '''
        return self.privKey.sign(data)

    def verify(self, data, signature):
        ''' Verify a signature '''
        return self.pubKey.verify(data, signature)