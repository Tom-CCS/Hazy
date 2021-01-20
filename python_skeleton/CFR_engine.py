'''
Simple example pokerbot, written in Python.
'''
from copy import copy
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction, AssignAction
from skeleton.states import GameState, TerminalState, RoundState, BoardState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND, NUM_BOARDS
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

from probability import raw_prob, calc_prob, win_or_lose
from algo_for_next_step import algorithm
from allocate import allocate
from behaviour_study import is_all_in

import eval7
import random
import json


# a map that maps each bucket to a list of possible response
# plus the corresponding probability
# we will train this set
# Denoted sigma_i(I, a)
actions = {0:{}, 1:{}}
# a map that maps each bucket to a list of possible response
# plus the corresponding probability
# we will update this set
# Denoted R_i(I, a)
regrets = {0:{}, 1:{}}
#Phase of the game. Not used
STREET_BUCKET = ["0", "3", "4", "5"]
#Raw Probability of winning: 0 - 0.5(S), 0.5 - 0.65(M), 0.65 - 1(L)
PROB_BUCKET = ["S", "M", "L"]
#Opponent Action Types: Check/Call(C), Small Raise(S), Large Raise(L), Double Raise(D)
OPPO_BUCKET = ["C", "S", "L", "D"]
#Action Types: Fold(F), Check/Call(C), Small Raise(S), Large Raise(L)
ACTIONS = ["F", "C", "S", "L"]
ALL_IN_ACTIONS = ["F", "C"]
#Number of iterations
ITER = 1000

def getBucket(raw_prob, street, oppo_action):
    '''
    Given the situation on the board, return the bucket(information set I) this situation corresponds to
    Params:
        raw_prob:
        Double, the raw probability of winning.(This will be precomputed to save time)
        street:
        list of strings. The cards in the street
        oppo_action:
        The opponent's action last turn
    Returns:
        A label for the bucket this situation corresponds to
    '''
    if raw_prob < 0.3:
        prob_label = 'S'
    elif raw_prob < 0.6:
        prob_label = 'M'
    else:
        prob_label = 'L'

    return prob_label + oppo_action

STACK = 200
CFR_calls = 0
def CFR(deck, pots, street, street_history, button, p1, p2, raw_p, winner):
    global CFR_calls
    CFR_calls += 1
    """
    A single node of the recursive CFR algorithm
    Params:
        History(h):
                button: the current player. 0 for SB, 1 for BB
                street: the street, or the number of cards revealed
                street_history: a string representing the betting history of the street
                pots: the pot of the two players

        Probability(pi):
            p1, p2: the probability that the two bots play this strategy

        Constants:
            deck: the deck of card
            raw_prob: the raw probability of winning at every given moment. Precomputed. Of the format player -> street -> prob
            winner: the winner of the game overall. Precomputed. 
    Returns:
        The expected util
    """
    player = button
    oppo = 1 - button
    #return payoff for terminal state
    #terminal is when all cards have been revealed or both side have all-ined
    if (street == 6) or (pots[0] == STACK and pots[1] == STACK):
        node_util = {}
        if winner != -1:
            # someone won
            node_util[winner] = pots[1 - winner]
            node_util[1 - winner] = -pots[1 - winner]
        else:
            # draw
            node_util = [0, 0]
        return node_util
    #compute the action of the opponent
    #if no such action, do a check
    if len(street_history) > 0:
        oppo_action = street_history[-1]
    else:
        oppo_action = "C"
    #detecting double raise
    if len(street_history) >= 2 and street_history[-2] == "S" and street_history[-1] == "S":
        oppo_action = "D"
    #extracted precomputed
    win_prob = raw_p[player][street]
    #compute the bucket of the current state
    bucket = getBucket(win_prob, street, oppo_action)
    action_prob = copy(actions[player][bucket]) # a map taking each action to its probability
    # we do not consider >= 4 bets, thus if this happens we merge the raises as checks
    forced_break = False
    if len(street_history) == 3 and oppo_action == "D":
        forced_break = True
        action_prob["C"] = action_prob["C"] + action_prob["S"] + action_prob["L"]
        del action_prob["S"]
        del action_prob["L"]
    util = {} # the expected util array, mapping each action to the expected util
    node_util = {0:0, 1:0} # the expected util for both players at this point
    for action in action_prob:
        #For each action, recursively call cfr with additional history and probability
        # the probability of entering this action
        next_prob = (p1 * action_prob[action], p2) if player == 0 else (p1, p2 * action_prob[action])
        # simply cutoff the game after the fourth raise
        # folds
        if action == "F":
            util["F"] = {player: -pots[player], oppo: pots[player]}
        # checks / calls
        elif action == "C":
            new_pots = {}
            new_pots[player] = max(pots[player], pots[oppo])
            new_pots[oppo] = pots[oppo]
            # the opponent has moved
            if len(street_history) >= 1:
                # In this case, advances to the next street
                next_street = street + 1 if street != 0 else 3
                util["C"] = CFR(deck, new_pots, next_street, "", 0, next_prob[0], next_prob[1], raw_p, winner)
            # the opponent has not moved
            else:
                # give control to the opponent
                util["C"] = CFR(deck, new_pots, street, "C", oppo, next_prob[0], next_prob[1], raw_p, winner)
        # raises
        else:
            new_pots= {}
            new_pots[oppo] = pots[oppo]
            pot_sum = 2 * new_pots[oppo]
            if action == "S":
                # raise to 0.5 the amount of stuff
                new_pots[player] = min(new_pots[oppo] + int(0.5 * pot_sum), STACK)
            else:
                # all in
                new_pots[player] = STACK
            # Betting goes to the opponent
            util[action] = CFR(deck, new_pots, street, street_history + action, oppo, next_prob[0], next_prob[1], raw_p, winner)
    # We have computed the util of each action
    # Compute expected util
    for action in action_prob:
        node_util[0] += util[action][0] * action_prob[action]
        node_util[1] += util[action][1] * action_prob[action]
    # Update culmultative regret
    # i haven't thought about how to update in the special case of consecutive raises
    # so i just don't update for now...
    if not forced_break:
        for action in action_prob:
            regrets[player][bucket][action] += next_prob[oppo] * (util[action][player] - node_util[player])
    return node_util

def deal_str(deck, sz):
    A = deck.deal(sz)
    B = [str(card) for card in A]
    return B
# Run the CFR algorithm
def run_CFR():
    #initialize strategy array
    for player in [0,1]:
        actions[player] = {}
        regrets[player] = {}
        for prob_type in PROB_BUCKET:
            for oppo_act in OPPO_BUCKET:
                bucket = prob_type + oppo_act
                actions[player][bucket] = {}
                regrets[player][bucket] = {}
                if oppo_act != 'L':
                    # is not a all in; all actions allowed
                    for action in ACTIONS:
                        actions[player][bucket][action] = 1 / len(ACTIONS)
                        regrets[player][bucket][action] = 0
                else:
                    # is all in; only check and fold
                    for action in ALL_IN_ACTIONS:
                        actions[player][bucket][action] = 1 / len(ALL_IN_ACTIONS)
                        regrets[player][bucket][action] = 0
    # iterations of CFR
    for iter in range(ITER):
        # shuffle the deck
        deck = eval7.Deck()
        deck.shuffle()
        hands = [deal_str(deck, 2), deal_str(deck, 2)]
        street_cards = deck.deal(5)
        # precompute probability array
        raw_p = {0:{}, 1:{}}
        for player in [0,1]:
            for street in [0,3,4,5]:
                raw_p[player][street] = calc_prob(hands[player], street_cards[:street])
        result = win_or_lose([eval7.Card(hands[0][0]), eval7.Card(hands[0][1])], street_cards, [eval7.Card(hands[1][0]), eval7.Card(hands[1][1])])
        if result == 2:
            winner = 0
        elif result == 0:
            winner = 1
        else:
            winner = -1
        # Run Magic
        util = CFR(deck, [1, 2], 0, "", 0, 1, 1, raw_p, winner)
        # Update Strategy
        for player in [0,1]:
            for prob_type in PROB_BUCKET:
                for oppo_act in OPPO_BUCKET:
                    bucket = prob_type + oppo_act
                    viable_actions = list(actions[player][bucket].keys())
                    strategy = {}
                    # Compute normalizing sum
                    normalizing_sum = 0
                    for action in viable_actions:
                        strategy[action] = max(regrets[player][bucket][action], 0)
                        normalizing_sum += strategy[action]
                    # Compute the new strategy according to pg 11 of cfr.pdf
                    for action in viable_actions:
                        if normalizing_sum > 0:
                            strategy[action] /= normalizing_sum
                        else:
                            strategy[action] = 1 / len(viable_actions)
                    actions[player][bucket] = strategy
        print("WINNER:", winner)
        print("UTIL:", util)
        print("NUMBER OF CALLS:",CFR_calls)
        print(actions)
        print(regrets)
        print(iter)
        print(hands, street_cards)

run_CFR()


                
            
    
    
