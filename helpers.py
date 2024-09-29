from classes import *
from typing import Union, List
import random
from itertools import combinations, product
import functools

# in increasing strength
RANKS = ["3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A", "2"]
SUITS = ["D", "C", "H", "S"]

def _SRank(card: str):
    rank = card[0]
    assert rank in RANKS
    return RANKS.index(rank)

def _SSuit(card: str):
    suit = card[1]
    assert suit in SUITS
    return SUITS.index(suit)

def S1(card: Union[str, List[str]]):
    if isinstance(card, str):
        return _SRank(card)*4 + _SSuit(card)
    else:
        assert len(card) == 1
        return S1(card[0])

assert S1("3D") == 0, "3D must be lowest"
assert S1("2S") == 51, "2S must be highest"
assert S1(["2S"]) == S1("2S"), "input can be a card or a hand"

def S2(hand: List[str]):
    assert len(hand) == 2
    if _SRank(hand[0]) == _SRank(hand[1]):
        return _SRank(hand[0])*4 + max(_SSuit(hand[0]), _SSuit(hand[1]))
    # assert False, "Two-card tricks must share the same rank"
    return -1

assert S2(["7H", "7D"]) > S2(["4C", "4H"]), "the rank of the first pair (7) is a higher rank than the rank of the second pair (4)"
assert S2(["AS", "AD"]) > S2(["AH", "AC"]), "the ranks are the same but the highest suit of the first pair (S) is higher than the highest suit of the second pair (H)"

def S3(hand: List[str]):
    assert len(hand) == 3
    if _SRank(hand[0]) == _SRank(hand[1]) == _SRank(hand[2]):
        return _SRank(hand[0])
    # assert False, "Three-card tricks must share the same rank"
    return -1

assert S3(["KC", "KD", "KS"]) > S3(["9C", "9H", "9S"]), "the rank of the first triplet (K) is higher than the rank of the second triplet (9)"

def S5(hand):
    hand = sorted(hand, key=S1)
    R = [_SRank(c) for c in hand]
    S = [_SSuit(c) for c in hand]
    numRank0, numRank4 = 0, 0
    for r in R:
        numRank0 += r == R[0]
        numRank4 += r == R[4]


    isFlush = S[0]==S[1]==S[2]==S[3]==S[4]
    isStraight = all(R[i]-R[0]==i for i in range(1, 5))

    if isFlush and isStraight:            # straight flush
        return 50000000 + (R[4]*4+S[4])
    elif numRank0 == 4:                   # 4 of a kind (v1)
        return 40000000 + R[0]
    elif numRank4 == 4:                   # 4 of a kind (v2)
        return 40000000 + R[4]
    elif numRank0 == 2 and numRank4 == 3: # full house (v1)
        return 30000000 + R[4]
    elif numRank0 == 3 and numRank4 == 2: # full house (v2)
        return 30000000 + R[0]
    elif isFlush:                         # flush
        return 20000000 + sum(R[i]*13**i for i in range(5))*4 + S[0]
    elif isStraight:
        return 10000000 + (R[4]*4+S[4])
    # assert False, "hand is not a 5-trick"
    return -1

assert S5(["2H", "2D", "2C", "2S", "3D"]) > S5(["TH", "9H", "6H", "5H", "3H"]), "a four-of-a-kind is stronger than a flush"
assert S5(["KH", "KD", "KC", "9S", "9D"]) > S5(["QD", "JH", "TD", "9C", "8D"]), "a full house is stronger than a straight"
assert S5(["AS", "KC", "QH", "JD", "TH"]) > S5(["KD", "QH", "JC", "TD", "9H"]), "the rank of the highest card in the first straight is (`A`) is higher than the rank of the highest card in the second straight (`K`)."
assert S5(["AH", "QH", "JH", "9H", "3H"]) > S5(["AD", "JD", "8D", "7D", "6D"]), "the rank of the highest cards are the same but the rank of the second highest card in the first flush (`Q`) is higher than the rank of the second highest card in the second flush (`J`)."
assert S5(["KH", "KD", "KC", "9S", "9D"]) > S5(["QH", "QD", "QC", "JS", "JD"]), "the rank of the triplet in the first full house (`K`) is higher than the rank of the triplet in the second full house (`Q`)."
assert S5(["8H", "8D", "8C", "8S", "3D"]) > S5(["6C", "6D", "6H", "6S", "4D"]), "the rank of the four-of-a-kind in the first set (`8`) is higher than the rank of the four-of-a-kind in the second set (`6`)."
assert S5(["9S", "8S", "7S", "6S", "5S"]) > S5(["8H", "7H", "6H", "5H", "4H"]), "the highest card in the first straight flush is (`9`) which is higher than the highest card in the second straight flush (`8`)."

def getAll5(other: List[str]):
    groupR = [[c for c in other if c[0] == r] for r in RANKS]
    groupS = [[c for c in other if c[0] == s] for s in SUITS]
    all5 = set()
    for s1, group1 in zip(RANKS, groupR):
        for s2, group2 in zip(RANKS, groupR):
            if s1 == s2: continue
            # four of a kind
            if len(group1) == 4:
                for c in group2:
                    all5.add(tuple(group1 + [c]))
            # full house
            for c1 in combinations(group1, 3):
                for c2 in combinations(group2, 2):
                    all5.add(c1 + c2)

    # flush
    for group in groupS:
        for c in combinations(group, 5):
            all5.add(c)

    # straight
    for i in range(9):
        for c in product(*groupR[i:i+5]):
            all5.add(c)
    return all5

def getAll3(other: List[str]):
    groupR = [[c for c in other if c[0] == r] for r in RANKS]
    all3 = set()
    for group in groupR:
        for c in combinations(group, 3):
            all3.add(c)
    return all3

def getAll2(other: List[str]):
    groupR = [[c for c in other if c[0] == r] for r in RANKS]
    all2 = set()
    for group in groupR:
        for c in combinations(group, 2):
            all2.add(c)
    return all2

def getAll1(other: List[str]):
    return {(c,) for c in other}

def getAll(other: List[str], sz=None):
    if sz == 1: return getAll1(other)
    elif sz == 2: return getAll2(other)
    elif sz == 3: return getAll3(other)
    elif sz == 5: return getAll5(other)
    return getAll1(other) + getAll2(other) + getAll3(other) + getAll5(other)

def partitionHand(hand):
    partitions = [{}]
    for rank in RANKS:
        cs = tuple(c for c in hand if c[0] == rank)
        if 1 <= len(cs) < 4: partitions[0].add(cs)
        else: partitions[0].extend((c,) for c in cs)
    for trick in getAll5(hand):
        if S5(trick) == -1: continue
        for p in partitionHand([c for c in hand if c not in trick]):
            partitions.add((trick,) + p)
    return partitions

def S(hand: List[str]):
    if isinstance(hand, str): return S1(hand)
    # print(hand)
    # assert isinstance(hand, list)
    if len(hand) == 5: return S5(hand)
    elif len(hand) == 3: return S3(hand)
    elif len(hand) == 2: return S2(hand)
    elif len(hand) == 1: return S1(hand)
    assert False, hand

def countPasses(history: GameHistory):
    i = 0
    while i < len(history.gameHistory[-1]) and history.gameHistory[-1][-i-1].cards == []:
        i += 1
    return i

def numRounds(history: GameHistory):
    """counting the current round"""
    return len(history.gameHistory)

def nextPlayer(playerNum: int):
    assert 0 <= playerNum < 4
    return (playerNum + 1) % 4

def prevPlayer(playerNum: int):
    assert 0 <= playerNum < 4
    return (playerNum - 1) % 4

def parse_used_cards(round_history):
    """returns all cards that were used"""
    used = []
    for round in round_history:
        for _, trick in round:
            used += trick
    return used

def genAll():
    """returns a set of all cards"""
    return [r+s for r in RANKS for s in SUITS]
