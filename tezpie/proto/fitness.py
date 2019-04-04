from .encoder import Encoder

Fitness = Encoder('Fitness', { 
    'type': 'list', 
    'of': Encoder('FitnessInnerValue', { 'type': 'bytes' }, dynamic=True)
}, dynamic=False)