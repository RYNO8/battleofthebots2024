"""DO NOT MODIFY"""
from typing import Any
from classes import *

print("STRAT=hack2")

class List(list, object):
    def __init__(self, l):
        super().__init__(l)
list = List

class Algorithm:

    # Calculates the relative strength of a single card as a number to be used with Python's key comparison mechanism
    def getStrength(self, card: str):
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        suits = ['D', 'C', 'H', 'S']
        return ranks.index(card[0]) * 4 + suits.index(card[1])

    def getAction(self, state: MatchState):
        action = []             # The cards you are playing for this trick
        myData = state.myData   # Communications from the previous iteration

        if not state.toBeat:
            return List([min(state.myHand, key=self.getStrength)]), ""
        else:
            return List([]), ""
