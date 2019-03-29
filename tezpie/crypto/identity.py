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
            "peer_id": "ids2KLbnrBkrxSWny8z5qiSN9gkQXX",
            "public_key":
            "69812c236724196a977617e38b4b6e5494e1e6aa528d6b4bab286f364a81201c",
            "secret_key":
            "f403fad34cac90f5133283a4391f7a115887b6fdbac8c60f5f8def7eed2ec465",
            "proof_of_work_stamp": "10d31d36f16d2849d2d9a47123d18bd0fbdedc6959747650" 
        }
        return Identity(data['peer_id'], data['public_key'], data['secret_key'], data['proof_of_work_stamp'])

    def __init__(self, peerid, pubkey, seckey, powstamp):
        self.peerid = peerid.encode('ascii')
        self.pubkey = pubkey.encode('ascii')
        self.seckey = seckey.encode('ascii')
        self.powstamp = powstamp.encode('ascii')

