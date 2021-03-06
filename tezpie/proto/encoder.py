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
	def __init__(self, encoder, fields, data, tag, dynamic):
		self.fields = fields
		self.data = data
		self.tag = tag
		self.dynamic = dynamic
		self.encoder = encoder

	def __repr__(self):
		return str(self.data)

	def __str__(self):
		s = self.encoder.name
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

	def encoder(self):
		return self.encoder

	def encoder_name(self):
		return self.encoder.name

	def serialize(self, skipSize=False):
		bio = BytesIO()

		if type(self.fields) == list:
			fields = self.fields
		else:
			fields = [ self.fields ]

		for f in fields:
			if f['name'] == 'noname':
				fdata = self.data
			else:
				fdata = self.data[f['name']]

			if type(f['type']) != str:
				bio.write(fdata.serialize())
			elif f['type'] == 'bytes':
				if f['length'] == 'dynamic':
					bio.write(struct.pack('>I', len(fdata)))
				bio.write(binascii.unhexlify(fdata))
			elif f['type'] == 'nonce':
				bio.write(fdata.get())
			elif f['type'] == 'time':
				ff = FIELDS['i64be']
				bio.write(struct.pack(ff[1], int(fdata.timestamp())))
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

		data = bio.read()
		if self.dynamic and not skipSize:
			osize = struct.pack('>I', len(data))
			return osize + data
		else:
			return data

	
class Encoder:
	def __init__(self, name, fields, tag = None, instance = None, dynamic=False):
		self.name = name
		self.fields = fields
		self.tag = tag
		self.dynamic = dynamic

		if instance:
			self.instance = instance 
		else:
			self.instance = EncoderInstance

	def __repr__(self):
		return str(self)

	def __str__(self):
		return self.name

	def from_data(self, data):
		parsed = {}

		for f in self.fields:
			parsed[f['name']] = data[f['name']]

		return self.instance(self, self.fields, parsed, self.tag, self.dynamic)

	def parse(self, data, skipSize=False):
		parsed = {}

		if data.__class__ == bytes:
			bio = BytesIO(data)
		else:
			bio = data

		if self.dynamic and not skipSize:
			osize = struct.unpack('>I', bio.read(4))[0]
			data2 = bio.read(osize)
			bio = BytesIO(data2)

		elif self.dynamic and skipSize:
			osize = len(data)

		if type(self.fields) == list:
			fields = self.fields
		else:
			fields = [ self.fields ]

		ptell = bio.tell()

		for f in fields:
			if not ('name' in f):
				f['name'] = 'noname'

			if type(f['type']) != str:
				parsed[f['name']] = f['type'].parse(bio)

			elif f['type'] == 'bytes':
				if self.dynamic and len(fields) == 1:
					l = osize
				elif f['length'] == 'dynamic':
					l = struct.unpack('>I', bio.read(4))[0]
				else:
					l = f['length']

				parsed[f['name']] = binascii.hexlify(bio.read(l))

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


		if type(self.fields) != list:
			parsed = parsed[self.fields['name']]

		#ptell_end = bio.tell()
				
		return self.instance(self, self.fields, parsed, self.tag, self.dynamic)


