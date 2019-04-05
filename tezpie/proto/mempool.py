from .encoder import EncoderInstance, Encoder

Mempool = Encoder('Mempool', [
    { 'type': 'list', 'of': Encoder('_', { 'type'; 'hash', 'of': 'operation'}), 'name': 'known_valid' },
    { 'type': 'list', 'of': Encoder('_', { 'type'; 'hash', 'of': 'operation'}), 'name': 'pending' },
], dynamic=True)
