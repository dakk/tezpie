import threading
from .. import config
from .peer import Peer

class PeerPool:
	def __init__(self):
		pass

	def bootstrap(self):
		for x in config.P2P_BOOTSTRAP_NODES:
			p = Peer(x)
			p.connect()