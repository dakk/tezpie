from .encoder import EncoderInstance, Encoder
from .fitness import Fitness

ShellHeader = Encoder('ShellHeader', [
    { 'type': 'i32be', 'name': 'level' },
    { 'type': 'u8be', 'name': 'proto' },
    { 'type': 'hash', 'of': 'block', 'name': 'pred' },
    { 'type': 'time', 'name': 'time' },
    { 'type': 'u8be', 'name': 'validation_pass' },
    { 'type': 'hash', 'of': 'operationlist', 'name': 'operations_hash' },
    { 'type': Fitness, 'name': 'fitness' },
    { 'type': 'hash', 'of': 'context', 'name': 'context' }
])

class BlockHeaderInstance(EncoderInstance):
    def hash(self):
        return 'ciao'

BlockHeader = Encoder('BlockHeader', [
    { 'type': ShellHeader, 'name': 'shell' },
    { 'type': 'bytes', 'name': 'proto_data', 'length': 2 }
], instance=BlockHeaderInstance, dynamic=True)
