from ...proto import BlockHeaderEncoder, Encoder

# Todo
GetCurrentHeadMessage = Encoder('GetCurrentHeadMessage', [
    { "type": "hash", "name": "chain_id", "of": "chain_id" }
], "0x13")


# Todo
CurrentHeadMessage = Encoder('CurrentHeadMessage', [
    { "type": "hash", "name": "chain_id", "of": "chain_id" },
    { "type": BlockHeaderEncoder, "name": "header" },
    { "type": 'bytes', "length": 'dynamic', "name": "history" }
], "0x14")
