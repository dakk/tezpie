import threading
import logging
import socket
import random
import time
from ..config import Config
from .peer import Peer

logger = logging.getLogger('tezpie')

class PeerPool:
	def __init__(self):
		self.socket_listen = None
		self.peers = {}
		self.discoveredNodes = []


	def lookup(self):
		self.discoveredNodes = []
		n = 0

		for x in Config.get('p2p_lookup_nodes'):
			try:
				ips = socket.getaddrinfo(x, Config.get('p2p_default_port'))
				for ip in ips:
					if ip[0].value == 2: # Only ipv4
						self.discoveredNodes.append(ip[4][0])
						n += 1
			except:
				pass
		return n
				
	def listen(self):
		self.socket_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket_listen.bind(('localhost', Config.get('p2p_default_port')))
		self.socket_listen.listen(5)
		logger.debug ('listening on port %d' % Config.get('p2p_default_port'))

		while True:
			(clientsocket, ip) = self.socket_listen.accept()
			p = Peer.from_socket(clientsocket, ip)
			if p:
				self.peers[ip] = p




	def bootstrap(self):
		nips = self.lookup()
		logger.debug ('dns lookup: found %d ips' % nips)

		#while len(self.peers.items()) < Config.get('p2p_min_peers') and len(self.discoveredNodes) > 0:
		if True:
			ip = random.choice (self.discoveredNodes)
			self.discoveredNodes.remove(ip)
			p = Peer('localhost', 19732)
			#p = Peer(ip)
			if p.connect():
				self.peers[ip] = p
			#time.sleep(2)