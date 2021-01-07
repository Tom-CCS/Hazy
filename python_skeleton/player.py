'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction, AssignAction
from skeleton.states import GameState, TerminalState, RoundState, BoardState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND, NUM_BOARDS
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

import eval7
import random
import json

PROBABILITIES={}
filename="raw_prob.json"
with open(filename,'r') as load_f:
    PROBABILITIES = json.load(load_f)

#The winning probabilities for RAW first two cards,
#calculated OUTSIDE this program and stored in prob.json file.

class Player(Bot):
    '''
    A pokerbot.
    '''

    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''
        self.board_allocations=[[],[],[]]#The board allocation for three boards
        self.play_high_thres=0.8 #The probability threshold to make it dare in high
        #self.opponent_possibility=[[],[],[]] # the guessed possibility of opponent
        pass
    
    def raw_prob(self, card1, card2):
        '''
        Parameters: two cards, card1 and card2
        Return the raw probability of winning of two cards
        '''
        num1,num2=card1[0],card2[0]
        suit1,suit2=card1[1],card2[1]
        if num1==num2:
            return PROBABILITIES[num1+num2]
        else:
            s1=num1+num2+"s" if suit1==suit2 else num1+num2+"u"
            s2=num2+num1+"s" if suit1==suit2 else num2+num1+"u"
            if s1 not in PROBABILITIES.keys():
                return PROBABILITIES[s2]
            return PROBABILITIES[s1]
            
        
    def allocate_cards(self, my_cards):
        '''
        Parameters:
        my_cards: 
            A list of strings 6 cards of [2-9TJQKA][cdhs].
            It represent the first six cards
        Returns:
        None.
        '''
        max_prob=0
        best=[]#Best pair
        for i in range(2*NUM_BOARDS-1):
            for j in range(i+1,2*NUM_BOARDS):
                if self.raw_prob(my_cards[i],my_cards[j])>max_prob:
                    best=[my_cards[i],my_cards[j]]
        
        rest=[]
        for card in my_cards:
            if card not in best: rest.append(card)
        
        second_max_prob=0
        second_best=[]#Second best pair
        for i in range(2*NUM_BOARDS-3):
            for j in range(i+1,2*NUM_BOARDS-2):
                if self.raw_prob(my_cards[i],my_cards[j])>second_max_prob:
                    second_best=[my_cards[i],my_cards[j]]
        
        worst=[]
        for card in rest:
            if card not in second_best: worst.append(card)
        
        if max_prob>self.play_high_thres:# We can have a really good card
            self.board_allocations=[worst, second_best, best]
        elif max_prob>self.play_high_thres:# We can get a fair pair
            self.board_allocations=[second_best, best, worst]
        else:# We have really bad luck
            self.board_allocations=[best, worst, second_best]
            
    def calc_prob(self, i, shown_cards):
        '''
        Parameters:
            i: The ith board (i=0,1,2)
            shown_cards: the number of cards shown
        Return: the probability of winning
        '''
        pass

    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        opp_bankroll = game_state.opp_bankroll # ^but for your opponent
        game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        my_cards = round_state.hands[active]  # your six cards at teh start of the round
        big_blind = bool(active)  # True if you are the big blind
        pass

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        opp_delta = terminal_state.deltas[1-active] # your opponent's bankroll change from this round 
        previous_state = terminal_state.previous_state  # RoundState before payoffs
        street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        for terminal_board_state in previous_state.board_states:
            previous_board_state = terminal_board_state.previous_state
            my_cards = previous_board_state.hands[active]  # your cards
            opp_cards = previous_board_state.hands[1-active]  # opponent's cards or [] if not revealed
        pass

    def get_actions(self, game_state, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs a triplet of actions from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your actions.
        '''
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards across all boards
        board_cards = [board_state.deck if isinstance(board_state, BoardState) else board_state.previous_state.deck for board_state in round_state.board_states] #the board cards
        my_pips = [board_state.pips[active] if isinstance(board_state, BoardState) else 0 for board_state in round_state.board_states] # the number of chips you have contributed to the pot on each board this round of betting
        opp_pips = [board_state.pips[1-active] if isinstance(board_state, BoardState) else 0 for board_state in round_state.board_states] # the number of chips your opponent has contributed to the pot on each board this round of betting
        continue_cost = [opp_pips[i] - my_pips[i] for i in range(NUM_BOARDS)] #the number of chips needed to stay in each board's pot
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        stacks = [my_stack, opp_stack]
        net_upper_raise_bound = round_state.raise_bounds()[1] # max raise across 3 boards
        net_cost = 0 # keep track of the net additional amount you are spending across boards this round
        my_actions = [None] * NUM_BOARDS
        for i in range(NUM_BOARDS):
            if AssignAction in legal_actions[i]: # This indicates it is the allocating round
                #cards = [my_cards[2*i], my_cards[2*i+1]]
                #my_actions[i] = AssignAction(cards)
                pass
            elif CheckAction in legal_actions[i]:  # check-call
                my_actions[i] = CheckAction()
            else:
                my_actions[i] = CallAction()
        return my_actions

"""
def magnitude(cards):
    '''
    Parameter: 
        cards: A list of 5 strings of [2-9TJQKA][cdhs]. It represent a card set.
        (it also applicable to a [set] of strings)
    Return: the "magnitude" of the card, such that if the cardset 1 is smaller than
    cardset 2, then the magnitude of cardset 1 is smaller than cardset 2.
    '''
    classify=1<<20
    # 10 classes of cards: 
    # royal_flush=10; straight_flush=9; four_of_a_kind=8; full_house=7;
    # flush=6; straight=5; three_of_a_kind=4; two_pairs=3; one_pair=2;
    # high_card=1
    kickers=[1<<16,1<<12,1<<8,1<<4,1]
    card_dict=to_dict(cards)
    if is_flush(cards):
        if is_straight(card_dict):
            if set(cards)==set(("As","Ks","Qs","Js","Ts")): return 10*classify
            # A royal flush
            else: return is_straight(card_dict)*kickers[0]+9*classify
            # A straight flush
        else: # a flush
            mag=6*classify
            for i in range(5):
                MAX=max(card_dict.keys())
                del card_dict[MAX]
                mag+=MAX*kickers[i]
            return mag
    else:
        if is_straight(card_dict): # a straight
            return is_straight(card_dict)*kickers[0]+5*classify
        else:
            if 4 in card_dict.values(): # Four of a kind
                print("yay")
                mag=8*classify
                for k,v in card_dict.items():
                    if v==4: mag+=kickers[0]*k
                    else: mag+=kickers[1]*k
                return mag
            elif 3 in card_dict.values(): # 3 of a kind or full house
                if 2 in card_dict.values(): # full house
                    mag=7*classify
                    for k,v in card_dict.items():
                        if v==3: mag+=kickers[0]*k
                        else: mag+=kickers[1]*k
                    return mag
                else: # Three of a kind
                    singles=set()
                    mag=4*classify
                    for k,v in card_dict.items():
                        if v==3: mag+=kickers[0]*k
                        else: singles.add(k)
                    return mag+max(singles)*kickers[1]+min(singles)*kickers[2]
            elif 2 in card_dict.values(): # One pair or two pairs:
                pairs=set()
                singles=set()
                for k,v in card_dict.items():
                    if v==2: pairs.add(k)
                    else: singles.add(k)
                if len(pairs)==2: # two pairs
                    return 3*classify+max(pairs)*kickers[0]+min(pairs)*kickers[1]+max(singles)*kickers[2]
                else:
                    return 2*classify+max(pairs)*kickers[0]+max(singles)*kickers[1]+(sum(singles)-max(singles)-min(singles))*kickers[2]+min(singles)*kickers[3]
            else:
                mag=1*classify
                for i in range(5):
                    MAX=max(card_dict.keys())
                    del card_dict[MAX]
                    mag+=MAX*kickers[i]
                return mag
    
def to_dict(cards):
    '''
    Parameters:
    cards : A list of 5 strings of [2-9TJQKA][cdhs]. It represent a card set.
    (it also applicable to a [set] of strings)
    Returns: A dictionary representation for cards, compressed by NUMBERS only
    '''
    mag={"T":10,"J":11,"Q":12,"K":13,"A":14}
    for i in "23456789": mag[i]=int(i)
    card_dict={}
    for card in cards:
        if mag[card[0]] not in card_dict.keys():
            card_dict[mag[card[0]]]=0
        card_dict[mag[card[0]]]+=1
    return card_dict

def is_straight(card_dict):
    '''
    Parameters:
    card_dict: a dictionary of cards, transformed by the previous funtion.
    Returns 0 if it is not a straight, or the largest number of the straight
    if it is a straight
    '''
    smallest=min(card_dict.keys())
    if smallest==2:
        for i in range(3):
            if smallest+i+1 not in card_dict.keys():
                return 0
        if 6 in card_dict.keys(): return 6
        elif 14 in card_dict.keys(): return 5
        return 0
    else:
        for i in range(4):
            if smallest+i+1 not in card_dict.keys():
                return 0
        return smallest+4

def is_flush(cards):
    '''
    Parameters:
    cards : a list of 5 strings of [2-9TJQKA][cdhs]. It represents a card set.
    (it also applicable to a [set] of strings)
    Returns: a boolean to detect whether it is a flush.
    '''
    suit=None
    flag=True
    for card in cards:
        if flag: suit=card[1]; flag=False
        else: 
            if card[1]!=suit:
                return False
    return True
"""

if __name__ == '__main__':
    run_bot(Player(), parse_args())
