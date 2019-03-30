from .store import Store

class ChainState(Store):
    def name(): return 'chainstate'

    def __init__ (self):
        super(Store, self).__init__()

        