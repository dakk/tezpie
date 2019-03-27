from .message import *

class AckMessage(Message):
	def __init__ (self, status):
		self.status = status

	def serialize(self):
		bio = MessageSerializer()
		bio.pack('u8le', 0x00 if self.status else 0xFF)
		return bio.to_bytes()
		

	def parse(data):
		bio = MessageParser(data)
		v = bio.unpack('u8le') == 0x00 
		return AckMessage(v)