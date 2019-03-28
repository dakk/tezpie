from io import BytesIO
import binascii
import struct

FIELDS = {
	'u32le': [4, '<I'],
	'u32be': [4, '>I'],
	'u16le': [2, '<H'],
	'u16be': [2, '>H'],
	'u8le': [1, '<B'],
	'u8be': [1, '>B'],
	'bool': [1, '?']
}

class MessageParseError(Exception):
	pass

class MessageSerializeError(Exception):
	pass

class MessageParser:
	def __init__(self, data):
		self.raw = BytesIO(data)

	def unpack(self, ftype):
		f = FIELDS[ftype]
		return struct.unpack(f[1], self.raw.read(f[0]))[0]

	def unpack_bytes(self, l):
		return binascii.hexlify(self.raw.read(l))

	def unpack_string(self):
		return self.raw.read(self.unpack('u16be')).decode('ascii')

class MessageSerializer:
	def __init__(self):
		self.raw = BytesIO()

	def pack(self, ftype, data):
		f = FIELDS[ftype]
		self.raw.write(struct.pack(f[1], data))

	def pack_bytes(self, data):
		self.raw.write(binascii.unhexlify(data))

	def pack_string(self, s):
		self.pack('u16be', len(s))
		self.raw.write(s.encode('ascii'))

	def to_bytes(self):
		self.raw.seek(0)
		return self.raw.read()

	
class MessagePart:
	def serialize(self, mserializer):
		pass

	def parse(mparser):
		pass

class Message:
	def serialize(self):
		pass

	def parse(data):
		pass