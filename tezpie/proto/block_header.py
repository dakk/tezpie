from .encoder import EncoderInstance, Encoder
from .fitness import Fitness


class BlockHeaderInstance(EncoderInstance):
    def hash(self):
        return 'ciao'

BlockHeader = Encoder('BlockHeader', [
    { 'type': 'i32be', 'name': 'level' },
    { 'type': 'u8be', 'name': 'proto' },
    { 'type': 'hash', 'of': 'block', 'name': 'pred' },
    { 'type': 'time', 'name': 'time' },
    { 'type': 'u8be', 'name': 'validation_pass' },
    { 'type': 'hash', 'of': 'operationlist', 'name': 'operations_hash' },
    { 'type': Fitness, 'name': 'fitness' },
    { 'type': 'hash', 'of': 'context', 'name': 'context' },
    { 'type': 'list', 'of': 'u8be', 'name': 'proto_data' }
], instance=BlockHeaderInstance, dynamic=True)
