from blockchain.pos.lot import Lot


def test_lot():
    lot = Lot("john", 1, "last_hash")
    assert lot.lot_hash()
