from helpers import *
from classes import *
from random import shuffle, choices
from itertools import count
from typing import Optional
from enum import Enum
import threading

def dealHands():
    """player0 always has the 3D"""
    deck = []
    for rank in RANKS:
        for suit in SUITS:
            deck.append(rank + suit)
    shuffle(deck)
    i = deck.index("3D")
    deck[0], deck[i] = deck[i], deck[0]
    assert deck[0] == "3D"
    return [deck[:13], deck[13:26], deck[26:39], deck[39:]]


class VerboseLevel(Enum):
    NO_OUTPUT = 0
    BRIEF = 1
    VERBOSE = 2

VERBOSE_DATA_EMPTY = [" "*10 for _ in range(4)]

class _MatchEngine:
    def __init__(self, player0, player1, player2, player3, nGames=3, outputFile=None, verbose=VerboseLevel.VERBOSE):
        self.outputFile = outputFile
        self.verbose: VerboseLevel = verbose
        self.verboseData = VERBOSE_DATA_EMPTY

        self.playerStrats = [player0, player1, player2, player3]
        self.matchHistory: List[GameHistory] = []
        self.playerPoints = [0, 0, 0, 0]

        for gameNum in range(1, nGames+1):
            self.log(f"\x1b[1;4mStarting Game {gameNum}\x1b[m")
            self.matchHistory.append(GameHistory(finished=False, winnerPlayerNum=-1, gameHistory=[]))
            winner = self._playGame()
            self.matchHistory[-1].finished = True
            self.matchHistory[-1].winnerPlayerNum = winner
            self.log(f"\x1b[32;42mPlayer{winner} won the game!\x1b[m")

            for playerNum in range(4):
                penalty = self.getPenalty(playerNum)
                self.playerPoints[playerNum] -= penalty
                self.playerPoints[winner] += penalty

            # use Median-Buchholz System for tiebreaks
            for playerNum in sorted(range(4), key=self.playerPoints.__getitem__, reverse=True):
                self.log(f"Player{playerNum} finished with {len(self.hands[playerNum])} cards in hand. \
They are now on {self.playerPoints[playerNum]} points")
            self.log()


    def _playGame(self):
        """modifies self.matchHistory, and indirectly self.hands and self.playerData"""
        self.hands = dealHands()
        self.playerData = ["", "", "", ""]

        # for playerNum in range(4):
        #     self.log(f"Player{playerNum} was dealt", " ".join(self.hands[playerNum]))

        playerNum = 0
        for roundNum in count(1):
            self.matchHistory[-1].gameHistory.append([])

            playerNum = self._playRound(playerNum)
            if self.hasWon(playerNum):
                return playerNum
            self.log(f"\x1b[32mPlayer{playerNum} won the round!\x1b[m")

    def _playRound(self, playerNum):
        """modifies self.matchHistory, and indirectly self.hands and self.playerData"""
        toBeat = None

        while True:
            if toBeat != None and toBeat.playerNum == playerNum:
                # you have previously played the highest card, so you win the round
                return playerNum
            
            toBeat = self._playMove(playerNum, toBeat)
            self.matchHistory[-1].gameHistory[-1].append(toBeat)
            
            if self.hands[playerNum] == []:
                # won game!
                return playerNum

            playerNum = (playerNum + 1) % 4

    def _playMove(self, playerNum, toBeat):
        """modifies self.hands and self.playerData"""
        matchState = MatchState(
            myPlayerNum=playerNum,
            players=[Player(points=points, handSize=len(hand)) for points, hand in zip(self.playerPoints, self.hands)],
            myHand=self.hands[playerNum],
            toBeat=toBeat,
            matchHistory=self.matchHistory,
            myData=self.playerData[playerNum]
        )
        # print(matchState)
        action, myData = self.playerStrats[playerNum]().getAction(matchState)
        # if self.playerStrats[playerNum].__module__ == "strategies.w1":
        #     from strategies.w5 import Algorithm as EE
        #     assert sorted(EE().getAction(matchState)[0]) == sorted(action)

        def myAssert(check, errorStr):
            if not check:
                print("\x1b[31m", errorStr)
                print(f"playerNum={playerNum},{self.playerStrats[playerNum]} hand={self.hands[playerNum]} action={action} toBeat={toBeat.cards}")
                exit(0)

        # guarantees
        myAssert((
            isinstance(action, list) and
            all(isinstance(card, str) for card in action) and
            all(len(card)==2 and card[0] in RANKS and card[1] in SUITS for card in action) and
            all(card in self.hands[playerNum] for card in action) and
            len(action) == len(set(action))
        ), f"action should be a list of unique cards from your hand, where each card is a string")
        myAssert(isinstance(myData, str), "specs require data to be a string")

        self.playerData[playerNum] = myData
        self.hands[playerNum] = [card for card in self.hands[playerNum] if card not in action]

        action.sort(key=S1)
        self.logPlay(playerNum, action)
        if action == []:
            myAssert(toBeat != None, "cannot pass at the start of the round")
            return toBeat # toBeat does not change
        if toBeat == None:
            myAssert(numRounds(self.matchHistory[-1]) > 1 or "3D" in action, "first play for first round must contain 3D")
            myAssert(S(action) != -1, "not valid hand")
        else:
            myAssert(len(action) == len(toBeat.cards), "trick must consist of the same number of cards")
            myAssert(toBeat.cards == None or S(action) > S(toBeat.cards), "hand does not beat current trick")
        return Trick(playerNum=playerNum, cards=action)

    def hasWon(self, playerNum):
        return self.hands[playerNum] == []

    def getPenalty(self, playerNum):
        N = len(self.hands[playerNum])
        if N == 13: return N*3
        elif N >= 10: return N*2
        return N



    def log(self, *args):
        if self.verbose != VerboseLevel.NO_OUTPUT:
            print(*args, file=self.outputFile)

    def logPlay(self, playerNum, action):
        if self.verbose == VerboseLevel.VERBOSE:
            if action:
                self.log(f"Player{playerNum} played", " ".join(action))
            else:
                self.log(f"Player{playerNum} passed")
        elif self.verbose == VerboseLevel.BRIEF:
            self.verboseData[playerNum] = "".join(action).ljust(10, ".") if action else "."*10
            if playerNum == 3:
                print(*self.verboseData, file=self.outputFile)
                self.verboseData = VERBOSE_DATA_EMPTY

def playMatch(player0, player1, player2, player3, randomised=False, **kwargs):
    playerStrats = [(player0, 0), (player1, 1), (player2, 2), (player3, 3)]
    if randomised:
        shuffle(playerStrats)

    e = _MatchEngine(
        playerStrats[0][0],
        playerStrats[1][0],
        playerStrats[2][0],
        playerStrats[3][0],
        **kwargs
    )
    points = [0, 0, 0, 0]
    for i in range(4):
        points[playerStrats[i][1]] = e.playerPoints[i]
    return points


def playMatches(players, **kwargs):
    points = [[0, 0] for _ in players]
    def playMatch():
        currPlayers = choices(range(len(players)), k=4)
        E = _MatchEngine(
            players[currPlayers[0]],
            players[currPlayers[1]],
            players[currPlayers[2]],
            players[currPlayers[3]],
            **kwargs
        )
        for i in range(4):
            points[currPlayers[i]][0] += E.playerPoints[i] == max(E.playerPoints)
            points[currPlayers[i]][1] += E.playerPoints[i]

    for matchNum in range(50):
        print("MATCH:", matchNum)
        playMatch()

    return [(player.__module__, point) for player, point in zip(players, points)]
