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
        self.play_high_thres=0.6 #The probability threshold to make it dare in high
        self.play_mid_thres=0.5 #The probability threshold to make it dare in high
        self.folding_high=0
        #self.opponent_possibility=[[],[],[]] # the guessed possibility of opponent
        pass
        
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
                if raw_prob(my_cards[i],my_cards[j])>max_prob:
                    max_prob=raw_prob(my_cards[i],my_cards[j])
                    best=[my_cards[i],my_cards[j]]
                    
        rest=[]
        for card in my_cards:
            if card not in best:
                rest.append(card)
                
        second_max_prob=0
        second_best=[]#Second best pair
        for i in range(2*NUM_BOARDS-3):
            for j in range(i+1,2*NUM_BOARDS-2):
                if raw_prob(rest[i],rest[j])>second_max_prob:
                    second_max_prob=raw_prob(rest[i],rest[j])
                    second_best=[rest[i],rest[j]]
        
        worst=[]
        for card in rest:
            if card not in second_best: worst.append(card)
        
        worst=[]
        for card in rest:
            if card not in second_best: worst.append(eval7.Card(str(card)))
            
        if max_prob>self.play_high_thres:# We can have a really good card
            self.board_allocations=[worst, second_best, best]
            self.folding_high=2
        elif max_prob>self.play_mid_thres:# We can get a fair pair
            self.board_allocations=[second_best, best, worst]
            self.folding_high=1
        else:# We have really bad luck
            self.board_allocations=[best, worst, second_best]
            self.folding_high=0
            
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
        
        self.allocate_cards(my_cards) #our old allocation strategy

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
        
        self.board_allocations = [[], [], []] #reset our variables at the end of every round!

        game_clock = game_state.game_clock #check how much time we have remaining at the end of a game
        round_num = game_state.round_num #Monte Carlo takes a lot of time, we use this to adjust!
        if round_num == NUM_ROUNDS:
            print(game_clock)


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
        # the card has a type str
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
        total_cont_cost = sum(continue_cost) # the minimum number of chips to keep playing at all the tables
        total_raise_reserve = my_stack - total_cont_cost
        for i in range(NUM_BOARDS):
            
            if AssignAction in legal_actions[i]: # This indicates it is the allocating round
                cards = self.board_allocations[i] #allocate our cards that we made earlier
                str_cards=[str(cards[0]),str(cards[1])]
                my_actions[i] = AssignAction(str_cards) #add to our actions
                
            elif isinstance(round_state.board_states[i], TerminalState): #make sure the game isn't over at this board
                my_actions[i] = CheckAction() #check if it is
            
            else:
                #do we add more resources?
                #forfeit tables that could not be won
                if i>self.folding_high:
                    my_actions[i]=FoldAction()
                    total_raise_reserve += continue_cost[i]
                    
                else:
                    board_cont_cost = continue_cost[i] #we need to pay this to keep playing
                    board_total = round_state.board_states[i].pot #amount before we started betting
                    pot_total = my_pips[i] + opp_pips[i] + board_total #total money in the pot right now
                    min_raise, max_raise = round_state.board_states[i].raise_bounds(active, round_state.stacks)
                    
                    print(min_raise,max_raise,board_cont_cost)
                    #print("board_cards : ",board_cards)
                    seen_cards=[]
                    for card in board_cards[i]:
                        if card!='':
                            seen_cards.append(eval7.Card(card))
                    #print(seen_cards)
                    win_prob=calc_prob(self.board_allocations[i],seen_cards)
                    algo=algorithm(RAISE_RATIO=0.2)
                    # our raise is low bounded by min_raise, and upper bounded by max_raise and the raise reserve
                    raise_ammount=algo(win_prob, pot_total, my_pips[i], board_cont_cost, (min_raise, min(max_raise, total_raise_reserve)))
                    
                    if RaiseAction in legal_actions[i] and raise_ammount > 0: #raise if we want and if we can afford it
                        my_actions[i] = RaiseAction(raise_ammount)
                        commit_cost = board_cont_cost+raise_ammount
                        total_raise_reserve -= raise_ammount
                    
                    elif CallAction in legal_actions[i] and raise_ammount >=0: 
                        my_actions[i] = CallAction()
                        commit_cost = board_cont_cost #the cost to call is board_cont_cost
                    
                    elif CheckAction in legal_actions[i] and raise_ammount >=0: #checking is our only valid move here
                        my_actions[i] = CheckAction()
                        commit_cost = 0
                    
                    else:
                        my_actions[i] = FoldAction()
                        commit_cost = 0
                        # if decide to fold, then the raise reserve could be increased
                        total_raise_reserve += continue_cost[i]

        return my_actions

if __name__ == '__main__':
    run_bot(Player(), parse_args())
