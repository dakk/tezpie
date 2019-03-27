from message import *

class MetadataMessage(Message):
	def __init__ (self, disable_mempool, private_node):
        self.disable_mempool = disable_mempool
        self.private_node = private_node

	def serialize(self):
		return ''

	def parse():
		return None