from tezpie import crypto
from tezpie.proto import BlockHeader, Fitness
import unittest
import binascii
from nacl.hash import blake2b
from nacl.encoding import RawEncoder

class TestBlockHeader(unittest.TestCase):
    #def test_parse_serialize(self):
    #    bh = b'0000b87c022a849785f4d9ee26309e98c25748abf85659bdce51cb67cdff881d4bcb37eb74000000005b656c8104b30246e7f354c45208b758986a11a5da56b0d924f84c051a878fd6e8a5827d6100000011000000010000000008000000000010eb8cf3c64bb42f12d39134d3a38e43fc81b0bb1cf6053952f5a402edb46c6332a2980000f788a3300779870800aa3f2d6f81a6e414c79bb6969f0cd3cbe5324804103606ab560d9b10191c245a087210c8df746fdcac7e31451477dcec330453ae6a3037855d9977fa60d9b0db'
    #    print (BlockHeader.parse(binascii.unhexlify(bh), True))        
    #    #self.assertEqual()


    def test_parse_serialize_fitness(self):
        f = b'000000010000000008000000000010eb8c'
        parsed = Fitness.parse(binascii.unhexlify(f), True)
        serialized = binascii.hexlify(parsed.serialize(True))
        print(f)
        print(repr(parsed))
        print (serialized)
        self.assertEqual(serialized, f)
