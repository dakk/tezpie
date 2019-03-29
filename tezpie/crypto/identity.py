import json
import nacl.utils

class Identity:
    def load(fpath):
        with open(fpath, 'r') as f:
            data = json.loads(f.read())
            return Identity(data['peer_id'], data['public_key'], data['secret_key'], data['proof_of_work_stamp'])

    def random():
        # key = nacl.utils.random(32)

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

