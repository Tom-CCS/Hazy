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
def getBucket(our_hand, oppo_hand, street, oppo_action):
    '''
    Given the situation on the board, return the bucket this situation corresponds to
    Params:
        our_hand:
        list of strings. The cards in our hand
        oppo_hand:
        list of strings. The cards in the opponent's hand
        street:
        list of strings. The cards in the street
        oppo_action:
        The opponent's action last turn
    Returns:
        A label for the bucket this situation corresponds to
    '''

def CFR(cards, p1, p2, history):
    """
    A single iteration of the recursive CFR algorithm
    Params:
        cards: a predetermined deck of card
        history: a string representing the history of the game
        p1, p2: the probability that the two bots play this strategy

    Returns:
        The expected util
    """
