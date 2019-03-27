from io import BytesIO
from .message import *

class Version(MessagePart):
	def __init__ (self, name, major, minor):
		self.name = name
		self.major = major
		self.minor = minor

	#def __repr__(self): 
	#	return 'Version(%s, %d, %d)' % (self.name, self.minor, self.major)

	def serialize(self, bio):
		bio.pack('u16be', 0) # waht's this? 
		bio.pack_string(self.name)
		bio.pack('u16be', self.minor)
		bio.pack('u16be', self.major)
		return bio

	def parse(bio):
		bio.unpack('u16be') # waht's this?
		name = bio.unpack_string()
		minor = bio.unpack('u16be')
		major = bio.unpack('u16be')
		return Version(name, major, minor)


class ConnectionMessage(Message):
	def __init__ (self, port, pubkey, pow_stamp, nonce, versions):
		self.port = port
		self.versions = versions
		self.pubkey = pubkey
		self.pow_stamp = pow_stamp
		self.nonce = nonce

	#def __repr__(self): 
	#	return 'ConnectionMessage(%d, %s)' % (self.port, self.pubkey)

	def serialize(self):
		bio = MessageSerializer()
		bio.pack('u16be', self.port)
		bio.pack_bytes(self.pubkey)
		bio.pack_bytes(self.pow_stamp)
		bio.pack_bytes(self.nonce)
		bio = self.versions[0].serialize(bio)
		return bio.to_bytes()

	def parse(data):
		bio = MessageParser(data)
		port = bio.unpack('u16be')
		pubkey = bio.unpack_bytes(32)
		pow_stamp = bio.unpack_bytes(24)
		nonce = bio.unpack_bytes(24)
		version = Version.parse(bio)	
		return ConnectionMessage(port, pubkey, pow_stamp, nonce, [version])