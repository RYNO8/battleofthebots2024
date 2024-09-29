"""
my submission from grok learning big2 comp (it did well but i forgot the rank)
DO NOT MODIFY
"""

from classes import *
print("STRAT=grok_ryno", flush=True)

def getRankings(cards):
    return [[i[0] for i in cards].count(RANK) for RANK in '3456789TJQKA2']


def is_a_full_house(cards):
    similar_rankings = getRankings(cards)
    return similar_rankings.count(2) == 1 and similar_rankings.count(3) == 1


def all_full_houses(hand):
    import itertools
    output = []
    for play in itertools.combinations(hand, 5):
        if is_a_full_house(play):
            output.append(list(play))
    return output


def is_better_full_house(first, second):
    RANK_ORDER = '3456789TJQKA2'
    first_rankings = getRankings(first)
    second_rankings = getRankings(second)

    if first_rankings.index(3) == second_rankings.index(3):
        return first_rankings.index(2) < second_rankings.index(2)
    else:
        return first_rankings.index(3) > second_rankings.index(3)


def is_a_straight(cards):
    rankings = getRankings(cards)
    rankings_is_straight = [all(i == 1 for i in rankings[i:i+5])
                            for i in range(len(rankings)-4)]
    # print(rankings_is_straight)
    if True in rankings_is_straight:
        return True
    return False


def all_straights(hand):
    import itertools
    output = []
    for play in itertools.combinations(hand, 5):
        if is_a_straight(play):
            output.append(list(play))
    return output


def is_better_straight(first, second):
    first, second = sort_cards(
        [[i] for i in first]), sort_cards([[i] for i in second])
    for i in range(-1, -6, -1):
        if is_higher_pair(first[i], second[i]) != None:
            return is_higher_pair(first[i], second[i])
    return "same thing!!"


def is_a_flush(cards):
    return all(cards[0][1] == i[1] for i in cards) and len(cards) == 5


def all_flushes(hand):
    import itertools
    output = []
    for play in itertools.combinations(hand, 5):
        if is_a_flush(play):
            output.append(list(play))
    return output


def is_better_flush(first, second):
    def byRank(card):
        return '3456789TJQKA2'.index(card[0])
    first.sort(key=byRank)
    second.sort(key=byRank)
    for i in -1, -2, -3, -4, -5:
        if first[i][0] != second[i][0]:
            return byRank(first[i][0]) > byRank(second[i][0])
    SUIT_ORDER = 'DCHS'
    return SUIT_ORDER.index(first[0][1]) > SUIT_ORDER.index(second[0][1])


def is_a_straight_flush(cards):
    return is_a_flush(cards) and is_a_straight(cards)


def all_straight_flushes(hand):
    import itertools
    output = []
    for play in itertools.combinations(hand, 5):
        if is_a_straight_flush(play):
            output.append(list(play))
    return output


def is_better_straight_flush(first, second):
    return is_better_flush(first, second)


def is_a_4_of_kind(cards):
    rankings = getRankings(cards)
    return rankings.count(4) == 1 and len(cards) == 5


def all_4_of_kind(hand):
    import itertools
    output = []
    for play in itertools.combinations(hand, 5):
        if is_a_4_of_kind(play):
            output.append(list(play))
    return output


def is_better_4_of_kind(first, second):
    if getRankings(first).index(4) == getRankings(second).index(4):
        return getRankings(first).index(1) >= getRankings(second).index(1)
    return getRankings(first).index(4) > getRankings(second).index(4)


def is_higher_pair(pair1, pair2):
    RANK_ORDER = '3456789TJQKA2'
    SUIT_ORDER = 'DCHS'
    if len(pair1) > len(pair2):
        return True
    elif len(pair1) < len(pair2):
        return False

    else:  # same length
        # print(pair1, pair2)
        pair1bestRank = max([RANK_ORDER.index(pair1[i][0])
                            for i in range(len(pair1))])
        pair2bestRank = max([RANK_ORDER.index(pair2[i][0])
                            for i in range(len(pair2))])
        if pair1bestRank > pair2bestRank:
            return True
        elif pair1bestRank < pair2bestRank:
            return False

        else:  # same rank
            pair1best = max([SUIT_ORDER.index(pair1[i][1])
                            for i in range(len(pair1))])
            pair2best = max([SUIT_ORDER.index(pair2[i][1])
                            for i in range(len(pair2))])
            if pair1best > pair2best:
                return True
            elif pair1best < pair2best:
                return False
            else:  # same suit
                # thus same card
                return None


def is_single(cards):
    return len(cards) == 1


def is_pair(cards):
    try:
        return cards[0][0] == cards[1][0] and len(cards) == 2
    except:
        return False


def is_triplet(cards):
    try:
        return (cards[0][0] == cards[1][0]) and (cards[1][0] == cards[2][0]) and len(cards) == 3
    except:
        return False


def getCombination(cards):
    if is_a_straight_flush(cards):
        return 5
    elif is_a_4_of_kind(cards):
        return 4
    elif is_a_full_house(cards):
        return 3
    elif is_a_flush(cards):
        return 2
    elif is_a_straight(cards):
        return 1
    else:
        return 0


def is_better_fiver(fiver1, fiver2):
    if getCombination(fiver1) > getCombination(fiver2):
        return True
    elif getCombination(fiver1) == getCombination(fiver2):
        if ((getCombination(fiver1) == 1 and is_better_straight(fiver1, fiver2)) or
            (getCombination(fiver1) == 2 and is_better_flush(fiver1, fiver2)) or
            (getCombination(fiver1) == 3 and is_better_full_house(fiver1, fiver2)) or
            (getCombination(fiver1) == 4 and is_better_4_of_kind(fiver1, fiver2)) or
                (getCombination(fiver1) == 5 and is_better_straight_flush(fiver1, fiver2))):
            return True
    return False


def sort_cards(cards):  # smallest to largest
    Sorted = []
    while cards:
        smallest = cards[0]
        for card in cards[1:]:
            # print(smallest, card)
            if (len(smallest) in [1, 2, 3] and is_higher_pair(smallest, card)) or (len(smallest) in [5] and is_better_fiver(smallest, card)):
                smallest = card
        Sorted.append(smallest)
        cards.remove(smallest)
    return Sorted


def all_pairs(hand):
    # print(hand)
    import itertools
    pairs = []
    for cardlength in [1, 2, 3, 5]:
        for pair in itertools.combinations(hand, cardlength):
            if cardlength == 1:
                pairs.append(list(pair))
            if cardlength == 2 and is_pair(pair):
                pairs.append(list(pair))
            elif cardlength == 3 and is_triplet(pair):
                pairs.append(list(pair))
            elif cardlength == 5 and is_a_straight(pair):
                pairs.append(list(pair))
            elif cardlength == 5 and is_a_flush(pair):
                pairs.append(list(pair))
            elif cardlength == 5 and is_a_full_house(pair):
                pairs.append(list(pair))
            elif cardlength == 5 and is_a_4_of_kind(pair):
                pairs.append(list(pair))
            elif cardlength == 5 and is_a_straight_flush(pair):
                pairs.append(list(pair))
    return pairs


def all_pairs_with_len(hand, length):
    return [i for i in all_pairs(hand) if len(i) == length]


def cards_higher_than_card(cards, card):
    output = []
    for i in cards:
        # print(i, card)
        if ((len(card) == 5 and is_better_fiver(i, card)) or
                (len(card) in [1, 2, 3] and is_higher_pair(i, card))):
            output.append(i)
    return output


def create_sorted(hand):
    from copy import deepcopy
    copyHand = [i[0]
                for i in sort_cards([[i] for i in deepcopy(hand)])]  # sort
    sortedHand = [[copyHand.pop()]]
    for func in [is_a_straight_flush, is_a_4_of_kind, is_a_full_house, is_a_flush, is_a_straight, is_triplet, is_pair, is_single]:
        while len([i for i in all_pairs(copyHand) if func(i)]) > 0:  # still plays of that kind
            plays = [i for i in all_pairs(copyHand) if func(i)][0]
            if any(["2" in i[0] for i in plays]):
                # reserve for one play (do not pair)
                sortedHand += [[i] for i in plays]
            else:
                sortedHand.append(plays)  # not one play
            for i in plays:
                copyHand.remove(i)
    return sortedHand

# this is optimal


def computer(hand, is_start_of_round, play_to_beat, round_history, player_no, hand_sizes, scores, round_no):
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
    # print(hand, is_start_of_round, play_to_beat, round_history, player_no, hand_sizes, scores, round_no)
    # If we are starting a trick, we cannot pass
    play_to_beat = [i[0] for i in sort_cards([[i] for i in play_to_beat])]
    allCards = ['3D', '3C', '3H', '3S', '4D', '4C', '4H', '4S', '5D', '5C', '5H', '5S', '6D', '6C', '6H', '6S', '7D', '7C', '7H', '7S', '8D', '8C', '8H', '8S', '9D',
                '9C', '9H', '9S', 'TD', 'TC', 'TH', 'TS', 'JD', 'JC', 'JH', 'JS', 'QD', 'QC', 'QH', 'QS', 'KD', 'KC', 'KH', 'KS', 'AD', 'AC', 'AH', 'AS', '2D', '2C', '2H', '2S']
    cardsPlayed, cardsLeft = [], []
    cardsLeft = []
    for Round in round_history:
        for cards in Round:
            for card in cards[1]:
                cardsPlayed.append(card)

    for card in allCards:
        if card not in cardsPlayed and card not in hand:
            cardsLeft.append(card)

    cardsLeft, cardsPlayed = [i[0] for i in sort_cards([[i] for i in cardsLeft])], [
        i[0] for i in sort_cards([[i] for i in cardsPlayed])]
    # print(cardsLeft)
    # print(cardsPlayed)
    plays = []

    if len(play_to_beat) == 0:
        # is_triplet, is_pair, is_single
        if all_straight_flushes(hand):
            plays.append(all_straight_flushes(hand))  # lowest straight flush
        if all_4_of_kind(hand):
            plays.append(all_4_of_kind(hand))  # lowest 4 of kind
        if all_full_houses(hand):
            plays.append(all_full_houses(hand))  # lowest full house
        if all_flushes(hand):
            plays.append(all_flushes(hand))  # lowest flush
        if all_straights(hand):
            plays.append(all_straights(hand))  # lowest straight
        if all_pairs_with_len(hand, 3):
            plays.append(all_pairs_with_len(hand, 3))  # lowest triple
        if all_pairs_with_len(hand, 2):
            plays.append(all_pairs_with_len(hand, 2))  # lowest double
        if all_pairs_with_len(hand, 1):
            plays.append(all_pairs_with_len(hand, 1))  # lowest single
        possibles = []  # smallest to largest, longest hand to shortest hand
        for types in plays:
            # len(types) > 1 or len(types[0]) in [1, 5] or types[0][0][0] in ["A", "2"]:
            if types:
                for cards in types:
                    if is_start_of_round and "3D" in cards:  # check so dont have 2
                        possibles.append(cards)
                    elif not is_start_of_round:
                        possibles.append(cards)
        # print(possibles)
        if not possibles:
            return "um"
        else:
            for i in possibles:
                # hand is at least 3 more than play
                if "2" not in [j[0] for j in i] or len(hand) <= len(i)+3:
                    return i  # will be left with 3 other cards after play

    else:
        lastPlay = round_history[-1][-1][1]
        sortedHand = create_sorted(hand)

        # print(sortedHand)
        low, high, middle = [], [], []
        for i in sortedHand:
            # print(i)
            if len(i) == len(play_to_beat):
                if sort_cards([[x] for x in hand])[-1][0] in i:
                    # i contains highest card
                    high += [i]

                elif (len(i) == 1 and i[0][0] in ["A", "2"] or  # one card and card rank in Q, K, 1, 2
                      # two cards and both card rank in 0, J, Q, K, 1, 2
                      len(i) == 2 and i[0][0] in ["Q", "K", "A", "2"] or
                      # three cards
                      len(i) == 3 and i[0][0] in ["5", "6", "7", "8", "9", "0", "J", "Q", "K", "A", "2"] or
                      len(i) == 5 and i[0][0] in ["3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K", "A", "2"]):
                    high += [i]

                else:
                    low += [i]
                """elif (len(i) == 1 and i[0][0] in ["J", "Q", "K"] or #one card and card rank in Q, K, 1, 2
                len(i) == 2 and i[0][0] in ["8", "9", "0", "J"] or #two cards and both card rank in 0, J, Q, K, 1, 2
                len(i) == 3 and i[0][0] in ["3", "4"] or #three cards
                len(i) == 5):
                middle += [i]"""

        # print(low)
        # print(high)
        newLow = sort_cards(cards_higher_than_card(low, play_to_beat))
        newHigh = sort_cards(cards_higher_than_card(high, play_to_beat))
        # print(newLow)
        # print(newHigh)

        if len(play_to_beat) == 1:
            # don't comment this out

            # elif any([high[0] in ["2S"] for high in newHigh]):
            #    return newHigh[-1]

            if low:  # still lows left
                # print(2)
                # if play_to_beat[0][0] in ["K", "A", "2"] and newHigh and newHigh[0][0] not in ["2"]: #last play was high
                #    return newHigh[0]

                if newLow:  # play lowest since you can
                    return newLow[0]
                # own highest card so play it
                elif newHigh and cards_higher_than_card(newHigh, [cardsLeft[-1]]):
                    return cards_higher_than_card(newHigh, [cardsLeft[-1]])[0]

                # own second and third highest
                elif len(newHigh) > 1 and is_higher_pair(newHigh[-2], [cardsLeft[-2]]):
                    # return third highest, force player to play highest, so later own highest
                    return newHigh[-2]
                elif newHigh and len(hand) < 4:
                    return newHigh[0]
                else:
                    return []

            else:  # no more lows, play high
                # print(3)
                # should return card if there is a pass bot
                if newHigh and any([hand < 5 for i, hand in enumerate(hand_sizes) if i != player_no]):
                    return newHigh[-1]
                # elif play_to_beat[0][0] in ["K", "A", "2"] and newHigh and newHigh[0][0] not in ["2"]: #last play was high
                #    return newHigh[0]

                elif newHigh and len(newHigh) < 4:  # one card left
                    return newHigh[-1]
                # own highest card so play it
                elif newHigh and cards_higher_than_card(newHigh, [cardsLeft[-1]]):
                    return cards_higher_than_card(newHigh, [cardsLeft[-1]])[0]

                # own second and third highest
                elif len(newHigh) > 1 and is_higher_pair(newHigh[-2], cardsLeft[-2]):
                    # return third highest, force player to play highest, so later own highest
                    return newHigh[-2]
                else:
                    return []

        elif len(play_to_beat) in [2, 3]:  # len to beat more than 1
            # if newLow:
            #    return newLow[0]
            if len(newHigh) > 1:
                # near end game, worth it to play good cards, as cannot be defeated easily
                return newHigh[-2]
            elif newHigh:
                return newHigh[-1]
            elif newLow:
                return newLow[0]
            # this will split a reserved which is already used in fiver
            for i in cards_higher_than_card(all_pairs_with_len(hand, len(play_to_beat)), play_to_beat):
                # doesn't play stuff like 2D, 2S
                if i[0][0] not in ["2"] or len(hand) < 5:
                    # should be lowest or highest?
                    return cards_higher_than_card(all_pairs_with_len(hand, len(play_to_beat)), play_to_beat)[0]
            return []

        elif len(play_to_beat) == 5:  # go for lowest
            # print(newLow, newHigh)
            if newLow:
                return newLow[0]
            elif newHigh:
                return newHigh[0]
            return []


############################################ PORTING ############################################

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


def S1(card: str):
    return _SRank(card)*4 + _SSuit(card)


class Algorithm:
    def getAction(self, state: MatchState):
        round_history = []
        for tricks in state.matchHistory[-1].gameHistory:
            round_history.append(
                [(trick.playerNum, sorted(trick.cards, key=S1)) for trick in tricks])
        round_no = len(state.matchHistory[-1].gameHistory)-1
        return computer(
            hand=sorted(state.myHand, key=S1),
            is_start_of_round="3D" in state.myHand,
            play_to_beat=[] if state.toBeat == None else sorted(state.toBeat.cards, key=S1),
            round_history=round_history,
            player_no=state.myPlayerNum,
            hand_sizes=[state.players[i].handSize for i in range(4)],
            scores=[state.players[i].points for i in range(4)],  # unused
            round_no=round_no  # unused
        ), ""
