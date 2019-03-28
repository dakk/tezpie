import threading
import logging
import socket
import random
from .. import config
from .peer import Peer

logger = logging.getLogger('tezpie')

class PeerPool:
	def __init__(self):
		self.peers = {}
		self.availableNodes = []

	def lookup(self):
		self.availableNodes = []
		n = 0

		for x in config.P2P_LOOKUP_NODES:
			ips = socket.getaddrinfo(x, config.P2P_DEFAULT_PORT)
			for ip in ips:
				if ip[0].value == 2:
					self.availableNodes.append(ip[4][0])
					n += 1
		
		return n
				

	def bootstrap(self):
		nips = self.lookup()
		logger.debug ('DNS lookup: found %d ips' % nips)

		#while len(self.peers.items()) < config.P2P_MAX_PEERS:
		ip = self.availableNodes[random.randint(0, len(self.availableNodes) - 1)]
		p = Peer(ip)
		if p.connect():
			self.peers[ip] = p