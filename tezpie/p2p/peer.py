import logging
import socket
import struct
from enum import Enum
from .. import config
from ..crypto import Identity, Nonce, KeyBox
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
		self.status = PeerStatus.CONNECTING
		self.identity = Identity.random()
		self.keybox = None

	def recv_message(self, msg_class, enc=True):
		mlen = int.from_bytes(self.socket.recv(2), 'big')
		data = self.socket.recv(mlen)

		if enc:
			data = self.keybox.decrypt(data)

		msg = msg_class.parse(data)
		logger.debug (msg)
		return msg

	def send_message(self, msg, enc=True):
		logger.debug (msg)
		data = msg.serialize()

		if enc:
			data = self.keybox.encrypt(data)

		self.socket.send(struct.pack('>H', len(data)))
		self.socket.send(data)

		
	def handshake(self):
		# Prepare and send the connection message
		local_nonce = Nonce.random()
		msg = ConnectionMessage(config.P2P_DEFAULT_PORT, self.iden.pubkey, iden.powstamp, local_nonce.get_and_increment(), [Version("TEZOS_ALPHANET_2018-11-30T15:30:56Z", 0, 0)])
		self.send_message(msg, enc=False)

		# Receive the connection message
		conn_msg = self.recv_message(ConnectionMessage, enc=False)
		self.pubkey = conn_msg.pubkey
		remote_nonce = Nonce(conn_msg.nonce)

		# From here, communications are encrypted: keybox creation
		self.keybox = KeyBox(remote_nonce, self.pubkey, local_nonce, self.iden.seckey)

		# Receive metadata
		meta_msg = self.recv_message(MetadataMessage)
		print (meta_msg)

		# Send metadata
		self.send_message(MetadataMessage(False, False))

		# Send ack
		self.send_message(AckMessage(True))

		# Receive ack
		ack_msg = self.recv_message(AckMessage)
		print (ack_msg)

		return True


	def connect(self):
		logger.info ('Connecting to %s:%d' % (self.host, self.port))
		try:
			self.socket.settimeout (3.0)
			self.socket.connect ((self.host, self.port))
			self.socket.settimeout (None)
			self.handshake ()
			self.status = PeerStatus.CONNECTED
			logger.info ('Connected')
			return True
		except Exception as e:
			print (e)
			self.status = PeerStatus.DISCONNECTED
			logger.info ('Connection failed')
			return False
		
		