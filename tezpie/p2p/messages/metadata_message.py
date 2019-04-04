from ...proto import Encoder

MetadataMessage = Encoder('MetadataMessage', [
	{ 'type': 'bool', 'name': 'disable_mempool' },
	{ 'type': 'bool', 'name': 'private_node' }
])
