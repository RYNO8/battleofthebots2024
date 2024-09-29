from classes import *
from typing import Union, List
import random
import itertools
import functools
import statistics
print("STRAT=w6.b")

# in increasing strength
RANKS = ["3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A", "2"]
SUITS = ["D", "C", "H", "S"]

@functools.lru_cache()
def _SRank(card: str):
    rank = card[0]
    assert rank in RANKS
    return RANKS.index(rank)

@functools.lru_cache()
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

@functools.lru_cache()
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

def S(hand: List[str]):
    if isinstance(hand, str): return S1(hand)
    if len(hand) == 5: return S5(hand)
    elif len(hand) == 3: return S3(hand)
    elif len(hand) == 2: return S2(hand)
    elif len(hand) == 1: return S1(hand)
    return -1

assert S5(("2H", "2D", "2C", "2S", "3D")) > S5(("TH", "9H", "6H", "5H", "3H")), "a four-of-a-kind is stronger than a flush"
assert S5(("KH", "KD", "KC", "9S", "9D")) > S5(("QD", "JH", "TD", "9C", "8D")), "a full house is stronger than a straight"
assert S5(("AS", "KC", "QH", "JD", "TH")) > S5(("KD", "QH", "JC", "TD", "9H")), "the rank of the highest card in the first straight is (`A`) is higher than the rank of the highest card in the second straight (`K`)."
assert S5(("AH", "QH", "JH", "9H", "3H")) > S5(("AD", "JD", "8D", "7D", "6D")), "the rank of the highest cards are the same but the rank of the second highest card in the first flush (`Q`) is higher than the rank of the second highest card in the second flush (`J`)."
assert S5(("KH", "KD", "KC", "9S", "9D")) > S5(("QH", "QD", "QC", "JS", "JD")), "the rank of the triplet in the first full house (`K`) is higher than the rank of the triplet in the second full house (`Q`)."
assert S5(("8H", "8D", "8C", "8S", "3D")) > S5(("6C", "6D", "6H", "6S", "4D")), "the rank of the four-of-a-kind in the first set (`8`) is higher than the rank of the four-of-a-kind in the second set (`6`)."
assert S5(("9S", "8S", "7S", "6S", "5S")) > S5(("8H", "7H", "6H", "5H", "4H")), "the highest card in the first straight flush is (`9`) which is higher than the highest card in the second straight flush (`8`)."

def isValidHand(hand: List[str]):
    try:
        if len(hand) == 1: S1(hand)
        elif len(hand) == 2: S2(hand)
        elif len(hand) == 3: S3(hand)
        elif len(hand) == 5: S5(hand)
        else:
            return False
    except AssertionError:
        return False
    else:
        return True

def beats(a: List[str], b: List[str]):
    """return if a beats b"""
    assert len(a) == len(b)
    if len(a) == 1: return S1(a) > S1(b)
    elif len(a) == 2: return S2(a) > S2(b)
    elif len(a) == 3: return S3(a) > S3(b)
    elif len(a) == 5: return S5(a) > S5(b)
    assert False, "invalid hand size"

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
            for c1 in itertools.combinations(group1, 3):
                for c2 in itertools.combinations(group2, 2):
                    all5.add(c1 + c2)
                    break

    # flush
    for group in groupS:
        for c in itertools.combinations(group, 5):
            all5.add(c)

    # straight
    for i in range(9):
        for c in itertools.product(*groupR[i:i+5]):
            all5.add(c)
    return all5

def getAll3(other: List[str]):
    groupR = [[c for c in other if c[0] == r] for r in RANKS]
    all3 = set()
    for group in groupR:
        for c in itertools.combinations(group, 3):
            all3.add(c)
    return all3

def getAll2(other: List[str]):
    groupR = [[c for c in other if c[0] == r] for r in RANKS]
    all2 = set()
    for group in groupR:
        for c in itertools.combinations(group, 2):
            all2.add(c)
    return all2

def getAll1(other: List[str]):
    return {(c,) for c in other}

def getAll(other: List[str], sz=None):
    if sz == 1: return getAll1(other)
    elif sz == 2: return getAll2(other)
    elif sz == 3: return getAll3(other)
    elif sz == 5: return getAll5(other)
    return getAll1(other) | getAll2(other) | getAll3(other) | getAll5(other)

def partitionHandSimple(hand):
    t1, t2, t3, t4 = [], [], [], []
    for rank in RANKS:
        cs = tuple(c for c in hand if c[0] == rank)
        if len(cs) == 1: t1.append(cs)
        elif len(cs) == 2: t2.append(cs)
        elif len(cs) == 3: t3.append(cs)
        elif len(cs) == 4: t4.append(cs)
    t = []
    while t1 and t4:
        t.append(t1.pop(-1) + t4.pop(-1))
    while t4:
        c1, c2, c3, c4 = t4.pop(-1)
        t.append((c1, c2))
        t.append((c3, c4))
    return t1 + t2 + t3 + t




def play(hand, is_start_of_round, play_to_beat, round_history, player_no, hand_sizes, scores, round_no):
    """
    The parameters to this function are:
    * `hand`: A list of card strings that are the card(s) in your hand.
    * `is_start_of_round`: A Boolean that indicates whether or not the `play` function is being asked to make the first play of a round.
    * `play_to_beat`: The current best play of the trick. If no such play exists (you are the first play in the trick), this will be an empty list.
    * `round_history`: A list of *trick_history* entries.
      A *trick_history* entry is a list of *trick_play* entries.
      Each *trick_play* entry is a `(player_no, play)` 2-tuple, where `player_no` is an integer between 0 and 3 (inclusive) indicating which player made the play, and `play` is the play that said player made, which will be a list of card strings.
    * `player_no`: An integer between 0 and 3 (inclusive) indicating which player number you are in the game.
    * `hand_sizes`: A 4-tuple of integers representing the number of cards each player has in their hand, in player number order. 
    * `scores`: A 4-tuple of integers representing the score of each player at the start of this round, in player number order.
    * `round_no`: An integer between 0 and 9 (inclusive) indicating which round number is currently being played.

    This function should return an empty list (`[]`) to indicate a pass (see "Playing a Round"), or a list of card strings, indicating that you want to play these cards to the table as a valid play.
    """

    other = sorted(list(set(genAll())-set(parse_used_cards(round_history))-set(hand)), key=S1)
    other_sz = [hand_sizes[i] for i in range(4) if i != player_no]

    def trickScore(trick):
        return sum(S1(c) for c in trick)

    if is_start_of_round:
        opt5 = [trick for trick in itertools.combinations(hand, 5) if "3D" in trick and S5(trick) >= 0]
        if opt5: return min(opt5, key=trickScore)
        return [c for c in hand if c[0] == '3']

    if len(play_to_beat) == 0 and S(hand) != -1:
        return hand

    # instawin
    all3s = [-1, -1, -1] + sorted([S3(t) for t in getAll3(other)])
    otherS3 = all3s[-2]
    otherS2 = max(list(map(S2, getAll2(other))) or [-1])
    otherS1 = max(map(S1, other))

    p = partitionHandSimple(hand)
    if len(play_to_beat) == 0:
        possible = p
    else:
        possible = [t for t in p if len(t) == len(play_to_beat) and S(t) > S(play_to_beat)]
    if possible:
        numLosing = 0
        for trick in p:
            if len(trick) == 1: numLosing += S1(trick) <= otherS1
            elif len(trick) == 2: numLosing += S2(trick) <= otherS2
            elif len(trick) == 3: numLosing += S3(trick) <= otherS3
            elif len(trick) == 5: numLosing += 0
        if numLosing <= 1:
            print("instawin")
            return max(possible, key=S)


    if len(play_to_beat) == 0:
        opt5 = [trick for trick in itertools.combinations(hand, 5) if S5(trick) >= 0]
        if opt5: return min(opt5, key=trickScore)

        op3 = [trick for trick in itertools.combinations(hand, 3) if S3(trick) >= 0]
        if op3: return min(op3, key=trickScore)

        op2 = [trick for trick in itertools.combinations(hand, 2) if S2(trick) >= 0]
        if op2: return min(op2, key=trickScore)

        # another player going to win, play highest
        if min(other_sz) == 1: return [hand[-1]]
        # we can win the round, play lowest
        if S1(hand[-1]) > max(map(S1, other)): return [hand[0]]
        return [hand[0]]

    if len(play_to_beat) == 1:
        beats = [card for card in hand if S1(card) > S1(play_to_beat)]
        if not beats: return []
        return [beats[0]]

    elif len(play_to_beat) == 2:
        op2 = [trick for trick in itertools.combinations(hand, 2) if S2(trick) >= S2(play_to_beat)]
        if op2: return min(op2, key=trickScore)
        return []

    elif len(play_to_beat) == 3:
        op3 = [trick for trick in itertools.combinations(hand, 3) if S3(trick) >= S3(play_to_beat)]
        if op3: return min(op3, key=trickScore)
        return []

    else:
        opt5 = [trick for trick in itertools.combinations(hand, 5) if S5(trick) >= S5(play_to_beat)]
        if opt5: return min(opt5, key=trickScore)
        return []


class Algorithm:
    def getAction(self, state: MatchState):
        round_history = []
        for tricks in state.matchHistory[-1].gameHistory:
            round_history.append(
                [(trick.playerNum, sorted(trick.cards, key=S1)) for trick in tricks])
        round_no = len(state.matchHistory[-1].gameHistory)-1
        # try:
        #     print(sorted(state.myHand, key=S1))
        # except Exception:
        #     pass
        result = sorted(play(
            hand=tuple(sorted(state.myHand, key=S1)),
            is_start_of_round="3D" in state.myHand,
            play_to_beat=[] if state.toBeat is None else tuple(sorted(
                state.toBeat.cards, key=S1)),
            round_history=round_history,
            player_no=state.myPlayerNum,
            hand_sizes=[state.players[i].handSize for i in range(4)],
            scores=[state.players[i].points for i in range(4)],  # unused
            round_no=round_no  # unused
        ), key=S1)
        random.shuffle(result) # lmao what?
        return result, ""

# print(play(
#     ('3D', '4D', '4C', '4H', '5C', '6C', '6H', '7H', '8H', '8S', '9C', 'QD', 'KD'),
#     False,
#     ('3D', '4D', '5D', '3D', '7D', '2D'),
#     [[(0, ['7D', '2D', '4D', '5D', '3D']), (1, [])]],
#     2,
#     [1,1,1,1],
#     1,
#     1
# ))
