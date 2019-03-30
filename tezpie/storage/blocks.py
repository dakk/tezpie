from .store import Store

class Blocks(Store):
    def name(): return 'blocks'

    def __init__ (self):
        super(Store, self).__init__()

        