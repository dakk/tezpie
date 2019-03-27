import logging
import socket
from enum import Enum
from .. import config
from .messages import *

logger = logging.getLogger('tezpie')

class PeerStatus(Enum):
	DISCONNECTED = 0
	CONNECTED = 1
	CONNECTING = 2

class Peer:
	def __init__(self, host, port = config.P2P_DEFAULT_PORT):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = host
		self.port = port
		self.pubkey = None
		self.nonce = None
		self.status = PeerStatus.CONNECTING

	def recv_message(self, msg_class):
		mlen = int.from_bytes(self.socket.recv(2), 'big')
		data = self.socket.recv(mlen)
		msg = msg_class.parse(data)
		logger.debug (msg)
		return msg

	def send_message(self, msg):
		self.socket.send(msg.serialize())
		
	def handshake(self):
		conn_msg = self.recv_message(ConnectionMessage)
		self.pubkey = conn_msg.pubkey
		self.nonce = conn_msg.nonce
		self.send_message(conn_msg)

	def connect(self):
		logger.info ('Connecting to %s:%d' % (self.host, self.port))
		if True:
			self.socket.settimeout (3.0)
			self.socket.connect ((self.host, self.port))
			self.socket.settimeout (None)
			self.handshake ()
			self.status = PeerStatus.CONNECTED
			logger.info ('Connected')
		else:
			print (e)
			self.status = PeerStatus.DISCONNECTED
			logger.info ('Connection failed')
		
		