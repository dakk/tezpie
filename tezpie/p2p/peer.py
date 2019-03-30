import logging
import socket
import struct
from enum import Enum
from ..config import Config
from ..crypto import Identity, Nonce, KeyBox
from .messages import *

logger = logging.getLogger('tezpie')

class PeerStatus(Enum):
	DISCONNECTED = 0
	CONNECTED = 1
	CONNECTING = 2

class Peer:
	def __init__(self, host, port = Config.get('p2p_default_port'), sock = None):
		if sock:
			self.socket = sock
			self.incoming = True
		else:
			self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			self.incoming = False

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
		local_nonce = Nonce.random()

		# Prepare and send the connection message
		conn_msg_sent = ConnectionMessage(Config.get('p2p_default_port'), self.identity.pubkey, self.identity.powstamp, local_nonce, [Version("TEZOS_ALPHANET_2018-11-30T15:30:56Z", 0, 0)])
		if not self.incoming:
			self.send_message(conn_msg_sent, enc=False)

		# Receive the connection message
		conn_msg_recv = self.recv_message(ConnectionMessage, enc=False)
		self.pubkey = conn_msg_recv.pubkey

		# Prepare and send the connection message
		if self.incoming:
			self.send_message(conn_msg_sent, enc=False)

		# From here, communications are encrypted: keybox creation
		nonces = Nonce.generate(conn_msg_sent.serialize(), conn_msg_recv.serialize(), not self.incoming)
		self.keybox = KeyBox(nonces['remote'], self.pubkey, nonces['local'], self.identity.seckey)


		# Send metadata
		self.send_message(MetadataMessage(False, False))

		# Receive metadata
		meta_msg = self.recv_message(MetadataMessage)
		print (meta_msg)

		# Send ack
		self.send_message(AckMessage(True))

		# Receive ack
		ack_msg = self.recv_message(AckMessage)
		print (ack_msg)

		return ack_msg.status

	def from_socket(socket, address):
		logger.info('connection from %s:%d' % (address, Config.get('p2p_default_port')))
		p = Peer(address, Config.get('p2p_default_port'), socket)
		try:
			p.handshake ()
			p.status = PeerStatus.CONNECTED
			logger.info ('Connected')
			return p
		except Exception as e:
			print (e)
			p.status = PeerStatus.DISCONNECTED
			logger.info ('Connection failed')
			return None

	def connect(self):
		logger.info('connecting to %s:%d' % (self.host, self.port))
		if True: #try:
			#self.socket.settimeout (3.0)
			self.socket.connect ((self.host, self.port))
			#self.socket.settimeout (None)
			self.handshake ()
			self.status = PeerStatus.CONNECTED
			logger.info ('connected')
			return True
		else: #except Exception as e:
			print (e)
			self.status = PeerStatus.DISCONNECTED
			logger.info ('connection failed')
			return False
		
		