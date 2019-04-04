from ...proto import BlockHeader, Encoder

GetCurrentBranchMessage = Encoder('GetCurrentBranchMessage', [
    { "type": "hash", "name": "chain_id", "of": "chain_id" }
], "0x10")




CurrentBranchMessage = Encoder('CurrentBranchMessage', [
    { "type": "hash", "name": "chain_id", "of": "chain_id" },
    { "type": BlockHeader, "name": "header" },
    #{ "type": 'list', "name": "history", "of": 'u8be' }
], "0x11")