from ...proto import BlockHeaderEncoder, Encoder

GetCurrentBranchMessage = Encoder('GetCurrentBranchMessage', [
    { "type": "hash", "name": "chain_id", "of": "chain_id" }
], "0x10")


CurrentBranchMessage = Encoder('CurrentBranchMessage', [
    { "type": "hash", "name": "chain_id", "of": "chain_id" },
    { "type": BlockHeaderEncoder, "name": "header" },
    { "type": 'bytes', "length": 'dynamic', "name": "history" }
], "0x11")