from ..crypto import Nonce
from . import constants
from io import BytesIO
from datetime import datetime
import binascii
import struct
import base58
import json

FIELDS = {
	'i64le': [8, '<q'],
	'i64be': [8, '>q'],
	'u64le': [8, '<Q'],
	'u64be': [8, '>Q'],
	'i32le': [4, '<i'],
	'i32be': [4, '>i'],
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
	def __init__(self, name, fields, data, tag):
		self.fields = fields
		self.data = data
		self.name = name
		self.tag = tag

	def __repr__(self):
		return str(self.data)

	def __str__(self):
		s = self.name
		if 'messages' in self.data:
			s += ' [ '
			for m in self.data['messages']:
				s += str(m) + ' '
			s += ']'
		return s

	def __getitem__(self, key):
		return self.data[key]

	def __setitem__(self, key, value):
		self.data[key] = value

	def __iter__(self):
		if 'messages' in self.data:
			return iter(self.data['messages'])
		else:
			return None

	def encoder_name(self):
		return self.name

	def serialize(self):
		bio = BytesIO()

		for f in self.fields:
			fdata = self.data[f['name']]

			if type(f['type']) != str:
				bio.write(fdata.serialize())

			if f['type'] == 'bytes':
				bio.write(binascii.unhexlify(fdata))

			elif f['type'] == 'nonce':
				bio.write(fdata.get())

			elif f['type'] == 'time':
				ff = FIELDS['i64be']
				bio.write(fstruct.pack(ff[1], datetime.timestamp(fdata)))

			elif f['type'] == 'string':
				bio.write(struct.pack('>H', len (fdata)))
				bio.write(fdata.encode('ascii'))

			elif f['type'] == 'hash' and f['of'] == 'block':
				bio.write(base58.b58decode_check(fdata)[len(constants.PREFIXES['b'])::])

			elif f['type'] == 'hash' and f['of'] == 'chain_id':
				bio.write(base58.b58decode_check(fdata)[len(constants.PREFIXES['Net'])::])

			elif f['type'] == 'hash' and f['of'] == 'context':
				bio.write(base58.b58decode_check(fdata)[len(constants.PREFIXES['Co'])::])

			elif f['type'] == 'hash' and f['of'] == 'operationlist':
				bio.write(base58.b58decode_check(fdata)[len(constants.PREFIXES['LLo'])::])

			elif f['type'] == 'hash' and f['of'] == 'operation':
				bio.write(base58.b58decode_check(fdata)[len(constants.PREFIXES['o'])::])

			elif f['type'] == 'list':
				bio.write(struct.pack('>H', len(fdata) - 1))
				for lelem in fdata:
					if type(f['of']) == str:
						ff = FIELDS[f['of']]
						bio.write(struct.pack(ff[1], lelem))
					else:
						bio.write(lelem.serialize())

			elif f['type'] == 'tlist':
				bio.write(struct.pack('>H', len(fdata) - 1))
				
				for lelem in fdata:
					elser = lelem.serialize()
					bio.write(struct.pack('>H', len(elser) + 2))
					bio.write(struct.pack('>H', int(lelem.tag, 16)))
					bio.write(elser)

			else:
				bio.write(struct.pack(FIELDS[f['type']][1], fdata))
								
		bio.seek(0)
		return bio.read()

	
class Encoder:
	def __init__(self, name, fields, tag = None):
		self.name = name
		self.fields = fields
		self.tag = tag

	def __repr__(self):
		return str(self)

	def __str__(self):
		return self.name

	def from_data(self, data):
		parsed = {}

		for f in self.fields:
			parsed[f['name']] = data[f['name']]

		return EncoderInstance(self.name, self.fields, parsed, self.tag)

	def parse(self, data):
		parsed = {}

		if data.__class__ == bytes:
			bio = BytesIO(data)
		else:
			bio = data

		for f in self.fields:
			if type(f['type']) != str:
				parsed[f['name']] = f['type'].parse(bio)

			elif f['type'] == 'bytes':
				parsed[f['name']] = binascii.hexlify(bio.read(f['length']))

			elif f['type'] == 'nonce':
				parsed[f['name']] = Nonce.from_bin(bio.read(24))

			elif f['type'] == 'time':
				ff = FIELDS['i64be']
				parsed[f['name']] = datetime.fromtimestamp(struct.unpack(ff[1], bio.read(ff[0]))[0])

			elif f['type'] == 'string':
				l = struct.unpack('>H', bio.read(2))[0]
				parsed[f['name']] = bio.read(l).decode('ascii')

			elif f['type'] == 'hash' and f['of'] == 'block':
				parsed[f['name']] = base58.b58encode_check(constants.PREFIXES['b'] + bio.read(32))

			elif f['type'] == 'hash' and f['of'] == 'chain_id':
				parsed[f['name']] = base58.b58encode_check(constants.PREFIXES['Net'] + bio.read(4))

			elif f['type'] == 'hash' and f['of'] == 'context':
				parsed[f['name']] = base58.b58encode_check(constants.PREFIXES['Co'] + bio.read(32))

			elif f['type'] == 'hash' and f['of'] == 'operationlist':
				parsed[f['name']] = base58.b58encode_check(constants.PREFIXES['LLo'] + bio.read(32))

			elif f['type'] == 'hash' and f['of'] == 'operation':
				parsed[f['name']] = base58.b58encode_check(constants.PREFIXES['o'] + bio.read(32))

			elif f['type'] == 'list':
				l = struct.unpack('>H', bio.read(2))[0]
				ll = []
				for i in range(l + 1):
					if type(f['of']) == str:
						ff = FIELDS[f['of']]
						ll.append(struct.unpack(ff[1], bio.read(ff[0]))[0])
					else:
						ll.append(f['of'].parse(bio))
				parsed[f['name']] = ll

			# Tagged list, a list where elements are tags of other types
			elif f['type'] == 'tlist':
				l = struct.unpack('>H', bio.read(2))[0]
				ll = []
				for i in range(l + 1):
					# Read the type
					elsize = struct.unpack('>H', bio.read(2))[0]
					t = hex(struct.unpack('>H', bio.read(2))[0])

					# Get the data
					if t in f['of']:
						ll.append (f['of'][t].parse(bio))
					else:
						bio.read(elsize - 2) # skip data if message is not recognized
				parsed['messages'] = ll

			else:
				ff = FIELDS[f['type']]
				parsed[f['name']] = struct.unpack(ff[1], bio.read(ff[0]))[0]

		t = bio.tell()
		print(t, len(bio.read()))
		bio.seek(t)
				
		return EncoderInstance(self.name, self.fields, parsed, self.tag)


