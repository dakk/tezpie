import logging
import socket
import binascii
import struct
import time
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
	def __init__(self, identity, host, port = Config.get('p2p_default_port'), sock = None):
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
		self.identity = identity
		self.keybox = None

	def disconnect(self):
		self.status = PeerStatus.DISCONNECTED
		self.socket.disconnect()

	def recv_raw_message(self, enc=True):
		mlen = int.from_bytes(self.socket.recv(2), 'big')
		data = self.socket.recv(mlen)

		#print('recv', binascii.hexlify(data))

		if enc:
			data = self.keybox.decrypt(data)
			print('recvdec', binascii.hexlify(data))

		return data

	def recv_message(self, msg_class, enc=True):
		msg = msg_class.parse(self.recv_raw_message(enc))
		logger.debug ('<= %s' % msg)
		return msg


	def send_raw_message(self, data, enc=True):
		if enc:
			data = self.keybox.encrypt(data)
			#print('sentenc', binascii.hexlify(data))

		self.socket.send(struct.pack('>H', len(data)))
		self.socket.send(data)


	def send_message(self, msg, enc=True):
		logger.debug ('=> %s' % msg)
		self.send_raw_message(msg.serialize(), enc)

		
	def handshake(self):
		local_nonce = Nonce.random()

		# Prepare and send the connection message
		conn_msg_sent = ConnectionMessage.from_data({
			'port': Config.get('p2p_default_port'), 
			'pubkey': self.identity.pubkey,
			'powstamp': self.identity.powstamp, 
			'nonce': local_nonce, 
			'versions': [
				Version.from_data({
					'name': "TEZOS_BETANET_2018-06-30T16:07:32Z", 
					'minor': 0, 
					'major': 0
				})
			]
		})

		if not self.incoming:
			self.send_message(conn_msg_sent, enc=False)

		# Receive the connection message
		conn_msg_recv = self.recv_message(ConnectionMessage, enc=False)
		self.pubkey = conn_msg_recv['pubkey']

		# Prepare and send the connection message
		if self.incoming:
			self.send_message(conn_msg_sent, enc=False)

		# From here, communications are encrypted: keybox creation
		sent = conn_msg_sent.serialize()
		sent = struct.pack('>H', len(sent)) + sent
		recv = conn_msg_recv.serialize()
		recv = struct.pack('>H', len(recv)) + recv
		nonces = Nonce.generate(sent, recv, self.incoming)
		self.keybox = KeyBox(nonces['remote'], self.pubkey, nonces['local'], self.identity.seckey)


		# Send metadata
		self.send_message(MetadataMessage.from_data({ 'disable_mempool': False, 'private_node': False }))

		# Receive metadata
		meta_msg = self.recv_message(MetadataMessage)

		# Send ack
		self.send_message(AckMessage.from_data({ 'status': AckMessage.ACK }))

		# Receive ack
		ack_msg = self.recv_message(AckMessage)
		return ack_msg['status'] == AckMessage.ACK

	def from_socket(identity, socket, address):
		logger.info('connection from %s:%d' % (address, Config.get('p2p_default_port')))
		p = Peer(identity, address, Config.get('p2p_default_port'), socket)
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
		

	def loop(self):
		# TODO Send GetCurrentBranch
		self.send_raw_message(binascii.unhexlify('0000000600107a06a770'))

		while self.status == PeerStatus.CONNECTED:
			self.recv_raw_message()
			time.sleep(2)