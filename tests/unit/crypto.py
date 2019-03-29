from tezpie import crypto
import unittest
import binascii

class TestNonce(unittest.TestCase):
    def test_nonce_increment(self):
        n = crypto.nonce.Nonce.from_hex('0000000000cff52f4be9352787d333e616a67853640d72c5')
        n.increment()
        self.assertEqual(n.get_hex(), '0000000000cff52f4be9352787d333e616a67853640d72c6')
        self.assertEqual(n.get(), binascii.unhexlify('0000000000cff52f4be9352787d333e616a67853640d72c6'))

    def test_generate_nonces(self):
        sent = binascii.unhexlify('00874d1b98317bd6efad8352a7144c9eb0b218c9130e0a875973908ddc894b764ffc0d7f176cf800b978af9e919bdc35122585168475096d0ebcaca1f2a1172412b91b363ff484d1c64c03417e0e755e696c386a0000002d53414e44424f5845445f54455a4f535f414c5048414e45545f323031382d31312d33305431353a33303a35365a00000000')
        recv = binascii.unhexlify('00874d1ab3845960b32b039fef38ca5c9f8f867df1d522f27a83e07d9dfbe3b296a6c076412d98b369ab015d57247e5380d708b9edfcca0ca2c865346ef9c3d7ed00182cf4f613a6303c9b2a28cda8ff93687bd20000002d53414e44424f5845445f54455a4f535f414c5048414e45545f323031382d31312d33305431353a33303a35365a00000000')
        n = crypto.nonce.Nonce.generate(sent, recv, False)
        self.assertEqual(n['local'].get_hex(), '8dde158c55cff52f4be9352787d333e616a67853640d72c5')
        self.assertEqual(n['remote'].get_hex(), 'e67481a23cf9b404626a12bd405066e161b32dc53f469153')

    def test_generate_nonces_incoming(self):
        sent = binascii.unhexlify('00874d1b98317bd6efad8352a7144c9eb0b218c9130e0a875973908ddc894b764ffc0d7f176cf800b978af9e919bdc35122585168475096d0ebcaca1f2a1172412b91b363ff484d1c64c03417e0e755e696c386a0000002d53414e44424f5845445f54455a4f535f414c5048414e45545f323031382d31312d33305431353a33303a35365a00000000')
        recv = binascii.unhexlify('00874d1ab3845960b32b039fef38ca5c9f8f867df1d522f27a83e07d9dfbe3b296a6c076412d98b369ab015d57247e5380d708b9edfcca0ca2c865346ef9c3d7ed00182cf4f613a6303c9b2a28cda8ff93687bd20000002d53414e44424f5845445f54455a4f535f414c5048414e45545f323031382d31312d33305431353a33303a35365a00000000')
        n = crypto.nonce.Nonce.generate(sent, recv, True)
        self.assertEqual(n['local'].get_hex(), 'ff0451d94af9f75a46d74a2a9f685cff20222a15829f121d')
        self.assertEqual(n['remote'].get_hex(), '8a09a2c43a61aa6eccee084aa66da9bc94b441b17615be58')



class TestKeyBox(unittest.TestCase):
    def test_shared_key(self):
        pk = "96678b88756dd6cfd6c129980247b70a6e44da77823c3672a2ec0eae870d8646"
        sk = "a18dc11cb480ebd31081e1541df8bd70c57da0fa419b5036242f8619d605e75a"
        n = crypto.nonce.Nonce.random()
        shared = crypto.key_box.KeyBox(n, pk, n, sk).shared_key()
        self.assertEqual(shared, "5228751a6f5a6494e38e1042f578e3a64ae3462b7899356f49e50be846c9609c")