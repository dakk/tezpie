from ...proto import Encoder

Version = Encoder('Version', [
	{ 'type': 'string', 'name': 'name' },
	{ 'type': 'u16be', 'name': 'minor' },
	{ 'type': 'u16be', 'name': 'major' }
])

ConnectionMessage = Encoder('ConnectionMessage', [
	{ 'type': 'u16be', 'name': 'port' },
	{ 'type': 'bytes', 'length': 32, 'name': 'pubkey' },
	{ 'type': 'bytes', 'length': 24, 'name': 'powstamp' },
	{ 'type': 'nonce', 'name': 'nonce' },
	{ 'type': 'list', 'of': Version, 'name': 'versions' }
])
