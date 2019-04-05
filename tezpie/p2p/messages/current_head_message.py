from ...proto import BlockHeaderEncoder, Encoder, MempoolEncoder

GetCurrentHeadMessage = Encoder('GetCurrentHeadMessage', [
    { "type": "hash", "name": "chain_id", "of": "chain_id" }
], "0x13")


CurrentHeadMessage = Encoder('CurrentHeadMessage', [
    { "type": "hash", "name": "chain_id", "of": "chain_id" },
    { "type": BlockHeaderEncoder, "name": "header" },
    { "type": Mempool, "name": "mempool" },
], "0x14")
