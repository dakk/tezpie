from .encoder import Encoder

Fitness = Encoder('Fitness', [
    #{ 'type': 'list', 'of': 'u8be', 'name': 'list' }
    { 'type': 'bytes', 'length': 21, 'name': 'list' }
])