import os
import json
import logging
import nacl.utils
from nacl.hash import blake2b
from ..config import Config
from .nonce import Nonce

logger = logging.getLogger('tezpie')

class Identity:
    def load(fpath=None):
        if fpath == None:
            fpath = Config.get('data_dir') + '/indentity.json'

        with open(fpath, 'r') as f:
            data = json.loads(f.read())
            logger.debug ('loaded from %s' % fpath)
            return Identity(data['peer_id'], data['public_key'], data['secret_key'], data['proof_of_work_stamp'])

    def save(self, fpath=None):
        if fpath == None:
            fpath = Config.get('data_dir') + '/indentity.json'

        if os.path.isfile(fpath):
            raise Exception("Identity file already present, not saving")

        with open(fpath, 'w') as f:
            logger.debug ('saved to %s' % fpath)
            f.write(json.dumps({
                "peer_id": self.peerid.decode('ascii'),
                "public_key": self.pubkey.decode('ascii'),
                "secret_key": self.seckey.decode('ascii'),
                "proof_of_work_stamp": self.powstamp.decode('ascii')
            }, indent=4, separators=(',', ': ')))

    def generate(diff=26.0):
        def make_target (diff):
            return 0

        def check_pow (pk, nonce, target):
            h = int.of_bytes (blake2b(pk + nonce.get()))
            if h < target:
                return True
            else:
                return False

        nonce = Nonce.random()
        
        logger.debug ('generating new identity with %f pow diff, please wait...' % diff)
        # key = nacl.utils.random(32)

        #while not check_pow(pk, nonce, target):
        #    nonce.increment()

        data = { 
            "peer_id": "idswiPoos4ZZ8S2WT4SCz6eUhjXMhU",
            "public_key": "1c0df7cfe10010d0784ee426c0e8fad73c8241d29fa15c8782df66f972f33e48",
            "secret_key": "93ef324958163f72a9105847f28702c3e272ba9b1eeafb6dc51578630ac8b819",
            "proof_of_work_stamp": "cb7909aeef66b57be8a7f2d31cd9742bbc4c68850b6c9399" 
        }
        return Identity(data['peer_id'], data['public_key'], data['secret_key'], data['proof_of_work_stamp'])

    def __init__(self, peerid, pubkey, seckey, powstamp):
        self.peerid = peerid.encode('ascii')
        self.pubkey = pubkey.encode('ascii')
        self.seckey = seckey.encode('ascii')
        self.powstamp = powstamp.encode('ascii')

