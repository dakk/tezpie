import threading
import logging
import socket
import random
import time
from .. import config
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

		for x in config.P2P_LOOKUP_NODES:
			try:
				ips = socket.getaddrinfo(x, config.P2P_DEFAULT_PORT)
				for ip in ips:
					if ip[0].value == 2: # Only ipv4
						self.discoveredNodes.append(ip[4][0])
						n += 1
			except:
				pass
		return n
				
	def listen(self):
		self.socket_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket_listen.bind(('127.0.0.1', config.P2P_DEFAULT_PORT))
		self.socket_listen.listen(5)
		logger.debug ('Listening on port %d' % config.P2P_DEFAULT_PORT)

		while True:
			(clientsocket, ip) = self.socket_listen.accept()
			p = Peer.from_socket(clientsocket, ip)
			if p:
				self.peers[ip] = p




	def bootstrap(self):
		nips = self.lookup()
		logger.debug ('DNS lookup: found %d ips' % nips)

		#while len(self.peers.items()) < config.P2P_MIN_PEERS and len(self.discoveredNodes) > 0:
		if True:
			ip = random.choice (self.discoveredNodes)
			self.discoveredNodes.remove(ip)
			#ip = '127.0.0.1'
			p = Peer(ip)
			if p.connect():
				self.peers[ip] = p
			#time.sleep(2)