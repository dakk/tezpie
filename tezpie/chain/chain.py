from threading import Lock

class Chain:
    def __init__(self):
        self.lock = Lock()

    def add_header(self, header):
        self.lock.acquire()
        self.lock.release()

    def add_block(self, block):
        self.lock.acquire()
        self.lock.release()


    def get_current_branch(self):
        pass

    def get_header(self, hash):
        pass

    def get_block(self, hash):
        pass

    def get_block_level(self, hash):
        pass

    def get_block_hash(self, level):
        pass