from ...proto import Encoder
from .connection_message import ConnectionMessage, Version
from .metadata_message import MetadataMessage
from .ack_message import AckMessage
from .current_branch_message import GetCurrentBranchMessage, CurrentBranchMessage


BootstrapMessage = Encoder('BootstrapMessage', [], "0x02")
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
            # '0x12': DeactivateMessage
            '0x13': GetCurrentHeadMessage,
            '0x14': CurrentHeadMessage,
            #'0x20': GetBlockHeaderMessage,
            #'0x21': BlockHeaderMessage
            #'0x30': GetOperationsMessage,
            #'0x31': OperationsMessage
            #'0x40': GetProtocolMessage,
            #'0x41': ProtocolMessage
            #'0x50': GetOperationHashesForBlocksMessage
            #'0x51': OperationHashesForBlocksMessage
            #'0x60': GetOperationForBlocksMessage
            #'0x61': OperationForBlocksMessage
        } 
    }
])