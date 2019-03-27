import random

class Nonce:
    def __init__(self, h):
        self.nonce = int(h, 16)

    def random():
        rn = random.randint(392318858461667547739736838950479151006397215279002157056, 6277101735386680763835789423207666416102355444464034512895)
        return Nonce(hex(rn)[2:].encode('ascii'))

    def increment(self):
        self.nonce += 1

    def get(self):
        return hex(self.nonce)[2:].encode('ascii')

    def get_and_increment(self):
        n = self.get()
        self.increment()
        return n