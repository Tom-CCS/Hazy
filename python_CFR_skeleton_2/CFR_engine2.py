'''
Simple example pokerbot, written in Python.
'''
from copy import copy

from probability import raw_prob, calc_prob, win_or_lose, calcBiasedProb

from allocate import allocate
from guessing import Guessing

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
# average strategy profile
# Denoted S_i(I, a)
strategy_sum = {0:{}, 1:{}}
#Action Types: Fold(F), Check/Call(C), Small Raise(S), Large Raise(L), All in(A)
RAISE_ACTIONS = ["F", "C", "S", "L", "A"]
#Disable pre-flop all ins
PRE_FLOP_ACTIONS = ["F", "C", "S"]
NO_RAISE_ACTIONS = ["F", "C"]
#Number of iterations
ITER = 60000

def getBucket(raw_prob, street, history):
    '''
    Given the situation on the board, return the bucket(information set I) this situation corresponds to
    Params:
        raw_prob:
        Double, the raw probability of winning.(This will be precomputed to save time)
        street:
        Int, The phase of the game street
        history:
        String, The previous actions in the street
    Returns:
        A label for the bucket this situation corresponds to
    '''
    if len(history) >= 2:
        history = history[-2:]
    street_label = str(street)
    prob_label = str(int(raw_prob / 0.1))

    return street_label + prob_label + history

# Initialize a strategy slot
# A strategy slot is defined as player -> bucket -> action
def initialize(player, win_prob, street, history):
    #initialize strategy array
    bucket = getBucket(win_prob, street, history)
    actions[player][bucket] = {}
    regrets[player][bucket] = {}
    strategy_sum[player][bucket] = {}
    # The set of allowed actions
    action_list = RAISE_ACTIONS
    if street == 0:
        action_list = PRE_FLOP_ACTIONS
    if (len(history) >= 1 and history[-1] == "L") or (len(history) >= 2 and history[-2:] == "SS"):
        action_list = NO_RAISE_ACTIONS
    for action in action_list:
        actions[player][bucket][action] = 1 / len(action_list)
        regrets[player][bucket][action] = 0
        strategy_sum[player][bucket][action] = 0

INFLATION = 1 # 0.5 * the number of chips inflated at the beginning
STACK = 200 # the number of chips each player has
SMALL_RAISE_RAIO = 0.66 # The ratio of a small raise
LARGE_RAISE_RAIO = 2 # The ratio of a large raise
CFR_calls = 0
def CFR(deck, pots, street, street_history, button, p1, p2, raw_p, winner):
    '''
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
    '''
    global CFR_calls
    CFR_calls += 1
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
    #extracted precomputed
    win_prob = raw_p[player][street]
    #compute the bucket of the current state
    bucket = getBucket(win_prob, street, street_history)
    if not bucket in actions[player]:
        initialize(player, win_prob, street, street_history)
    action_prob = copy(actions[player][bucket]) # a map taking each action to its probability
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
                util["C"] = CFR(deck, new_pots, next_street, "", 1, next_prob[0], next_prob[1], raw_p, winner)
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
                # raise to 0.66x the amount of stuff
                new_pots[player] = min(new_pots[oppo] + int(SMALL_RAISE_RAIO * pot_sum), STACK)
            elif action == "L":
                # raise to 2x the amount of stuff
                new_pots[player] = min(new_pots[oppo] + int(LARGE_RAISE_RAIO * pot_sum), STACK)
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
    # Line 25 of pseudocode
    for action in action_prob:
        regrets[player][bucket][action] += next_prob[oppo] * (util[action][player] - node_util[player])
    # Update average strategy
    # Line 26 of pseudocode
    player_prob = p1 if player == 0 else p2
    for action in action_prob:
        strategy_sum[player][bucket][action] += player_prob * action_prob[action] 
    return node_util

def deal_str(deck, sz):
    A = deck.deal(sz)
    B = [str(card) for card in A]
    return B
# 
# Run the CFR algorithm
# save breakpoints in FILE
# Write the result to the file given by DEST
def run_CFR(FILE, DEST):
    #output file
    f = open(FILE + str(INFLATION) + ".txt", "w")
    # iterations of CFR
    iters = 0
    while (iters < ITER):
        print(iters)
        # shuffle the deck
        deck = eval7.Deck()
        deck.shuffle()
        # deal card
        hands = [deal_str(deck, 6), deal_str(deck, 6)]
        street_cards = deck.deal(5)
        # precompute probability array
        raw_p = {0:{}, 1:{}}
        guessings = {0: [None]*3, 1: [None]*3}
        # allocate
        # since we might give up on certain boards
        # we will have to continue in such circumstances
        playing = True
        for player in [0,1]:
            # use our allocation algorithm
            allocation = allocate(hands[player])
            # print(allocation)
            if allocation[1] < INFLATION - 1:
                playing = False
            hands[player] = allocation[0][INFLATION - 1]
            for street in [0,3,4,5]:
                raw_p[player][street] = calc_prob(hands[player], street_cards[:street])
        if not playing:
            continue
        # compute game result
        result = win_or_lose([eval7.Card(hands[0][0]), eval7.Card(hands[0][1])], street_cards, [eval7.Card(hands[1][0]), eval7.Card(hands[1][1])])
        if result == 2:
            winner = 0
        elif result == 0:
            winner = 1
        else:
            winner = -1
        # Run Magic
        Blind = [1 + INFLATION, 2 + INFLATION]
        util = CFR(deck, Blind, 0, "", 0, 1, 1, raw_p, winner)
        # Update Strategy
        for player in [0,1]:
            for bucket in actions[player]:
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
        # dumping some info
        if iters % 10 == 0:
            #print(actions)
            #print(regrets)
            #print(iters)
            #print("WINNER:", winner)
            #print("UTIL:", util)
            #print("NUMBER OF CALLS:",CFR_calls)

            #print(hands, street_cards)
            pass
        # compute average strategy every 500 iters
        if iters % 500 == 0:
            average_strategy = {0:{}, 1:{}}
            for player in [0,1]:
                for bucket in actions[player]:
                    viable_actions = list(actions[player][bucket].keys())
                    avg_strategy = {}
                    # Compute normalizing sum
                    normalizing_sum = 0
                    for action in viable_actions:
                        normalizing_sum += strategy_sum[player][bucket][action]
                    # We disable any action unless it has a > 0.1 prob of triggering. 
                    # I hope this would be helpful for all-ins
                    for action in viable_actions:
                        if strategy_sum[player][bucket][action] < 0.1 * normalizing_sum:
                            normalizing_sum -= strategy_sum[player][bucket][action]
                            strategy_sum[player][bucket][action] = 0
                    # Compute the new strategy according to pg 11 of cfr.pdf
                    for action in viable_actions:
                        if normalizing_sum > 0:
                            avg_strategy[action] = strategy_sum[player][bucket][action] / normalizing_sum
                        else:
                            avg_strategy[action]  = 1 / len(viable_actions)
                    average_strategy[player][bucket] = avg_strategy
            # write to file
            f.write(str(average_strategy) + "\n\n")
        # if training is finished, write to destination
        if iters == ITER - 1:   
            DEST.write(str(average_strategy) + "\n")
        iters += 1
    f.close()

if __name__ == '__main__':
    g = open("CFR_dict.txt", "w")
    # run CFR for all 3 tables
    for INFLATION in range(1, 4):
        run_CFR("output", g)
    g.close()

                
            
    
    
