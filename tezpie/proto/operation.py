from .encoder import EncoderInstance, Encoder

class Operation(EncoderInstance):
    def hash(self):
        return 'ciao'

OperationEncoder = Encoder('OperationEncoder', [
    { 'type': 'hash', 'of': 'block', 'name': 'branch' },
    { 'type': 'bytes', 'length': 'dynamic', 'name': 'proto_data' }    
], instance=Operation, dynamic=True)
