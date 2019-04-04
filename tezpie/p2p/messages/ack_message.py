from ...proto import Encoder

AckMessage = Encoder('AckMessage', [
	{ 'type': 'u8be', 'name': 'status' }
])

AckMessage.ACK = 0x00
AckMessage.NACK = 0xFF