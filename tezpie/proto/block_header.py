from .encoder import EncoderInstance, Encoder
from .fitness import Fitness

class BlockHeader(EncoderInstance):
    def hash(self):
        return 'ciao'

BlockHeaderEncoder = Encoder('BlockHeader', [
    { 'type': 'i32be', 'name': 'level' },
    { 'type': 'u8be', 'name': 'proto' },
    { 'type': 'hash', 'of': 'block', 'name': 'pred' },
    { 'type': 'time', 'name': 'time' },
    { 'type': 'u8be', 'name': 'validation_pass' },
    { 'type': 'hash', 'of': 'operationlist', 'name': 'operations_hash' },
    { 'type': 'bytes', 'name': 'fitness', 'length': 'dynamic' },
    { 'type': 'hash', 'of': 'context', 'name': 'context' },
    { 'type': 'bytes', 'length': 'dynamic', 'name': 'proto_data' }
], instance=BlockHeader, dynamic=True)
