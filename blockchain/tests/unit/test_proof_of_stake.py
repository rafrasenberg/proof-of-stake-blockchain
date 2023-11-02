import random
import string

from blockchain.pos.proof_of_stake import ProofOfStake


def get_random_string(length):
    letters = string.ascii_lowercase
    result_string = "".join(random.choice(letters) for i in range(length))
    return result_string


def test_proof_of_stake():
    pos = ProofOfStake()
    pos.update("john", 10)
    pos.update("jane", 100)

    assert pos.get("john") == 10
    assert pos.get("jane") == 100
    assert not pos.get("jack")


def test_proof_of_stake_winner_lot():
    pos = ProofOfStake()
    pos.update("john", 50)
    pos.update("jane", 100)

    john_wins = 0
    jane_wins = 0

    for _ in range(100):
        forger = pos.forger(get_random_string(1))
        if forger == "john":
            john_wins += 1
        elif forger == "jane":
            jane_wins += 1

    assert jane_wins > 40
    assert john_wins < 60
