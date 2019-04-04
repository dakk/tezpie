from .encoder import Encoder

Fitness = Encoder('Fitness', { 
    'type': 'bytes', 
}, dynamic=True)


# 'of': Encoder('FitnessValue', { 'type': 'bytes' }, dynamic=True)