from ...encoder import Encoder
from .connection_message import ConnectionMessage, Version
from .metadata_message import MetadataMessage
from .ack_message import AckMessage


BootstrapMessage = Encoder('BootstrapMessage', [], "0x02")
GetCurrentBranchMessage = Encoder('GetCurrentBranchMessage', [], "0x10")
CurrentBranchMessage = Encoder('CurrentBranchMessage', [], "0x11")
GetCurrentHeadMessage = Encoder('GetCurrentHeadMessage', [], "0x13")
CurrentHeadMessage = Encoder('CurrentHeadMessage', [], "0x14")

Message = Encoder('Message', [
    { 
        'type': 'tlist', 
        'name': 'messages', 
        'of': {
            '0x02': BootstrapMessage,
            '0x10': GetCurrentBranchMessage,
            '0x11': CurrentBranchMessage,
            '0x13': GetCurrentHeadMessage,
            '0x14': CurrentHeadMessage
        } 
    }
])