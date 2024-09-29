from classes import *
from typing import Union, List
import random
print("STRAT=w1")

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
    assert _SRank(hand[0]) == _SRank(hand[1]), "Two-card tricks must share the same rank"
    return _SRank(hand[0])*4 + max(_SSuit(hand[0]), _SSuit(hand[1]))

assert S2(["7H", "7D"]) > S2(["4C", "4H"]), "the rank of the first pair (7) is a higher rank than the rank of the second pair (4)"
assert S2(["AS", "AD"]) > S2(["AH", "AC"]), "the ranks are the same but the highest suit of the first pair (S) is higher than the highest suit of the second pair (H)"

def S3(hand: List[str]):
    assert len(hand) == 3
    assert _SRank(hand[0]) == _SRank(hand[1]) == _SRank(hand[2]), "Three-card tricks must share the same rank"
    return _SRank(hand[0])

assert S3(["KC", "KD", "KS"]) > S3(["9C", "9H", "9S"]), "the rank of the first triplet (K) is higher than the rank of the second triplet (9)"

def _SStraightFlush(hand: List[str]):
    hand.sort(key=S1)
    if all(
        _SSuit(hand[i]) == _SSuit(hand[0]) and
        _SRank(hand[i]) - _SRank(hand[0]) == i
        for i in range(5)):
        return S1(hand[4])
    return -1

# Good question, for our competition we'll have 2s always higher than Aces so JQKA2 is the highest straight and 34567 is the lowest (23456 is invalid)
# assert _SStraightFlush(["JC", "QC", "KC", "AC", "2C"]) > _SStraightFlush(["3C", "4C", "5C", "6C", "7C"])
assert _SStraightFlush(["JC", "QC", "KC", "AC", "2C"]) != -1
assert _SStraightFlush(["3C", "4C", "5C", "6C", "7C"]) != -1
assert _SStraightFlush(["2C", "3C", "4C", "5C", "6C"]) == -1

def _SFourOfAKind(hand: List[str]):
    if sum(_SRank(hand[i]) == _SRank(hand[0]) for i in range(5)) == 4:
        return _SRank(hand[0])
    elif sum(_SRank(hand[i]) == _SRank(hand[1]) for i in range(5)) == 4:
        return _SRank(hand[1])
    else:
        return -1

def _SFullHouse(hand: List[str]):
    hand.sort(key=S1)
    numSuit0 = sum(_SRank(hand[i]) == _SRank(hand[0]) for i in range(5))
    numSuit4 = sum(_SRank(hand[i]) == _SRank(hand[4]) for i in range(5))
    if numSuit0 == 2 and numSuit4 == 3:
        # hand[0], hand[1] is a pair
        # hand[2], hand[3], hand[4] is a triple
        return _SRank(hand[4])
    elif numSuit0 == 3 and numSuit4 == 2:
        # hand[0], hand[1], hand[2] is a triple
        # hand[3], hand[4] is a pair
        return _SRank(hand[0])
    else:
        return -1

def _SFlush(hand: List[str]):
    hand.sort(key=S1)
    if all(_SSuit(hand[i]) == _SSuit(hand[0]) for i in range(5)):
        return sum(_SRank(hand[i])*13**i for i in range(5))*4 + _SSuit(hand[0])
    return -1

def _SStraight(hand: List[str]):
    hand.sort(key=S1)
    if all(_SRank(hand[i]) - _SRank(hand[0]) == i for i in range(5)):
        return S1(hand[4])
    return -1

def S5(hand: List[str]):
    assert len(hand) == 5
    if (s := _SStraightFlush(hand)) != -1:
        assert 0 <= s < 10000000
        return s+50000000
    elif (s := _SFourOfAKind(hand)) != -1: 
        assert 0 <= s < 10000000
        return s+40000000
    elif (s := _SFullHouse(hand)) != -1:
        assert 0 <= s < 10000000
        return s+30000000
    elif (s := _SFlush(hand)) != -1:
        assert 0 <= s < 10000000
        return s+20000000
    elif (s := _SStraight(hand)) != -1:
        assert 0 <= s < 10000000
        return s+10000000
    else:
        assert False, "hand is not a 5-trick"

assert S5(["2H", "2D", "2C", "2S", "3D"]) > S5(["TH", "9H", "6H", "5H", "3H"]), "a four-of-a-kind is stronger than a flush"
assert S5(["KH", "KD", "KC", "9S", "9D"]) > S5(["QD", "JH", "TD", "9C", "8D"]), "a full house is stronger than a straight"
assert S5(["AS", "KC", "QH", "JD", "TH"]) > S5(["KD", "QH", "JC", "TD", "9H"]), "the rank of the highest card in the first straight is (`A`) is higher than the rank of the highest card in the second straight (`K`)."
assert S5(["AH", "QH", "JH", "9H", "3H"]) > S5(["AD", "JD", "8D", "7D", "6D"]), "the rank of the highest cards are the same but the rank of the second highest card in the first flush (`Q`) is higher than the rank of the second highest card in the second flush (`J`)."
assert S5(["KH", "KD", "KC", "9S", "9D"]) > S5(["QH", "QD", "QC", "JS", "JD"]), "the rank of the triplet in the first full house (`K`) is higher than the rank of the triplet in the second full house (`Q`)."
assert S5(["8H", "8D", "8C", "8S", "3D"]) > S5(["6C", "6D", "6H", "6S", "4D"]), "the rank of the four-of-a-kind in the first set (`8`) is higher than the rank of the four-of-a-kind in the second set (`6`)."
assert S5(["9S", "8S", "7S", "6S", "5S"]) > S5(["8H", "7H", "6H", "5H", "4H"]), "the highest card in the first straight flush is (`9`) which is higher than the highest card in the second straight flush (`8`)."

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

    if is_start_of_round:
        # return 

class Algorithm:
    def getAction(self, state: MatchState):
        round_history = []
        for tricks in state.matchHistory[-1].gameHistory:
            round_history.append(
                [(trick.playerNum, sorted(trick.cards, key=S1)) for trick in tricks])
        round_no = len(state.matchHistory[-1].gameHistory)-1
        result = sorted(play(
            hand=sorted(state.myHand, key=S1),
            is_start_of_round="3D" in state.myHand,
            play_to_beat=[] if state.toBeat is None else sorted(
                state.toBeat.cards, key=S1),
            round_history=round_history,
            player_no=state.myPlayerNum,
            hand_sizes=[state.players[i].handSize for i in range(4)],
            scores=[state.players[i].points for i in range(4)],  # unused
            round_no=round_no  # unused
        ), key=S1)
        random.shuffle(result) # lmao what?
        return result, ""
