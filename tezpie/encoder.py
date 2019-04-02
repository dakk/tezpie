from .crypto import Nonce
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

class EncoderInstance:
	''' This class keep decoded data '''
	def __init__(self, name, fields, data):
		self.fields = fields
		self.data = data
		self.name = name

	def __repr__(self):
		return self.name

	def __str__(self):
		return self.name
		
	def serialize(self):
		bio = BytesIO()

		for f in self.fields:
			fdata = self.data[f['name']]

			if f['type'] == 'bytes':
				bio.write(binascii.unhexlify(fdata))

			elif f['type'] == 'nonce':
				bio.write(fdata.get())

			elif f['type'] == 'string':
				bio.write(struct.pack('>H', len (fdata)))
				bio.write(fdata.encode('ascii'))

			elif f['type'] == 'list':
				bio.write(struct.pack('>H', len(fdata) - 1))
				for lelem in fdata:
					bio.write(lelem.serialize())

			else:
				bio.write(struct.pack(FIELDS[f['type']][1], fdata))
								
		bio.seek(0)
		return bio.read()

	def __getitem__(self, key):
		return self.data[key]

	def __setitem__(self, key, value):
		self.data[key] = value

	
class Encoder:
	def __init__(self, name, fields):
		self.name = name
		self.fields = fields

	def __repr__(self):
		return self.name

	def __str__(self):
		return self.name

	def from_data(self, data):
		parsed = {}

		for f in self.fields:
			parsed[f['name']] = data[f['name']]

		return EncoderInstance(self.name, self.fields, parsed)

	def parse(self, data):
		parsed = {}

		if data.__class__ == bytes:
			bio = BytesIO(data)
		else:
			bio = data

		for f in self.fields:
			if f['type'] == 'bytes':
				parsed[f['name']] = binascii.hexlify(bio.read(f['length']))

			elif f['type'] == 'nonce':
				parsed[f['name']] = Nonce.from_bin(bio.read(24))


			elif f['type'] == 'string':
				l = struct.unpack('>H', bio.read(2))[0]
				parsed[f['name']] = bio.read(l).decode('ascii')

			elif f['type'] == 'list':
				l = struct.unpack('>H', bio.read(2))[0]
				ll = []
				for i in range(l + 1):
					ll.append(f['of'].parse(bio))
				parsed[f['name']] = ll

			else:
				ff = FIELDS[f['type']]
				parsed[f['name']] = struct.unpack(ff[1], bio.read(ff[0]))[0]
				
		return EncoderInstance(self.name, self.fields, parsed)


