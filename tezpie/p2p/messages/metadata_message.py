from .message import *

class MetadataMessage(Message):
	def __init__ (self, disable_mempool, private_node):
		self.disable_mempool = disable_mempool
		self.private_node = private_node

	def serialize(self):
		bio = MessageSerializer()
		bio.pack('bool', self.disable_mempool)
		bio.pack('bool', self.private_node)
		return bio.to_bytes()
		

	def parse(data):
		bio = MessageParser(data)
		dmempool = bio.unpack('bool')
		privnode = bio.unpack('bool')
		return MetadataMessage(port, dmempool, privnode)