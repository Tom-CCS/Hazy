'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction, AssignAction
from skeleton.states import GameState, TerminalState, RoundState, BoardState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND, NUM_BOARDS
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

from probability import raw_prob, calc_prob
from algo_for_next_step import algorithm
from allocate import allocate
from behaviour_study import is_all_in

import eval7
import random
import json


# a map that maps each bucket to a list of possible response
# plus the corresponding probability
# we will train this set
available_action = {}
#Raw Probability of winning: 0 - 0.5(S), 0.5 - 0.65(M), 0.65 - 1(L)
#Opponent Action Types: Check/Call(C), Small Raise(S), Large Raise(L), Double Raise(D)
#Action Types: Fold(F), Check/Call(C), Small Raise(S), Large Raise(L)

def getBucket(raw_prob, street, oppo_action):
    '''
    Given the situation on the board, return the bucket this situation corresponds to
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
    if raw_prob < 0.5:
        prob_label = 'S'
    elif raw_prob < 0.65:
        prob_label = 'M'
    else:
        prob_label = 'L'

    return prob_label + oppo_action

def GameState(cards, p1, p2, history):
    """
    A single iteration of the recursive CFR algorithm
    Params:
        cards: a predetermined deck of card
        history: a string representing the history of the game
        p1, p2: the probability that the two bots play this strategy

    Returns:
        The expected util
    """
