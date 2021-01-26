'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction, AssignAction
from skeleton.states import GameState, TerminalState, RoundState, BoardState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND, NUM_BOARDS
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

from probability import raw_prob, calc_prob
from algo_for_next_step import determine_action, classify_action
from allocate import allocate

import eval7
import random
import json

#The winning probabilities for RAW first two cards,
#calculated OUTSIDE this program and stored in prob.json file.
PROBABILITIES={}
filename_PROB="raw_prob.json"
with open(filename_PROB,'r') as load_f:
    PROBABILITIES = json.load(load_f)

#The CFR Dictionary
#A list of three dicts
# indicating strategy at each board
CFR_dict = [{}, {}, {}]
filename_CFR = "CFR_dict.txt"
with open(filename_CFR,'r') as load_c:
    for board in range(3):
        CFR_dict[board] = eval(load_c.readline())


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
        self.playing=[]

        self.round_count = 0 # count the number of rounds elapsed
        self.player = 0 # 0 if we are playing as SB, 1 if we are playing as BB
        self.raise_count = [0,0,0] # The number of consecutive raises at a table
        self.prev_street = 0 # the street we were in last turn
        self.history = [] # the street history at each board

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
        self.board_allocations, index = allocate(my_cards)
        #print(self.board_allocations)
        if index==2: self.playing=[1,1,1]
        if index==1: self.playing=[1,1,0]
        if index==0: self.playing=[1,0,0]
             
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

        if my_bankroll - opp_bankroll > 24 * (500 - round_num) + 50:
            self.playing = [0,0,0]

        self.round_count += 1 

        self.player = 1 if big_blind else 0

        self.raise_count = [0,0,0]

        self.history = ["","",""]

        self.prev_street = -1 

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
        if round_num % 50 == 0:
            print(game_clock)

    def update_history(self, street, oppo_action_bucket, board):
        """
        Update the self.history array to reflect the current street history
        """
        if street > self.prev_street:
            # a new street
            if (self.player == 1 and street != 0) or (self.player == 0 and street == 0):
                # in this case we go first
                self.history[board] = ""
            else:
                self.history[board] = oppo_action_bucket
        else:
            # the same street
            self.history[board] += oppo_action_bucket
            # if round too long, forget previous actions
            if len(self.history[board]) > 2:
                self.history[board] = self.history[board][-2:]


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

        # Decide own action
        for i in range(NUM_BOARDS):
            if AssignAction in legal_actions[i]: # This indicates it is the allocating round
                cards = self.board_allocations[i] #allocate our cards that we made earlier
                my_actions[i] = AssignAction(cards) #add to our actions
                
            elif isinstance(round_state.board_states[i], TerminalState): #make sure the game isn't over at this board
                my_actions[i] = CheckAction() #check if the game is over
            
            else:
                #do we add more resources?
                #forfeit tables that could not be won
                if self.playing[i]==0:
                    if FoldAction in legal_actions[i]:
                        my_actions[i]=FoldAction()
                        total_raise_reserve += continue_cost[i]
                    else:
                        my_actions[i]=CheckAction()
                else:
                    # We keep playing at this table
                    board_cont_cost = continue_cost[i] #we need to pay this to keep playing
                    board_total = round_state.board_states[i].pot #amount before we started betting
                    pot_total = my_pips[i] + opp_pips[i] + board_total #total money in the pot right now
                    min_raise, max_raise = round_state.board_states[i].raise_bounds(active, round_state.stacks)

                    # classify the opponent's action and update history
                    oppo_action = classify_action(board_cont_cost, pot_total)
                    self.update_history(street, oppo_action, i)
                    
                    # compute probability
                    seen_cards=[]
                    for card in board_cards[i]:
                        if card!='':
                            seen_cards.append(eval7.Card(card))
                    
                    win_prob=calc_prob(self.board_allocations[i], seen_cards)


                    # apply CFR
                    raise_amount = determine_action(self.player, street, win_prob, self.history[i],
                                        pot_total, my_pips[i], board_cont_cost, 
                                        (min_raise, min(max_raise, total_raise_reserve)), CFR_dict[i])
                
                    if RaiseAction in legal_actions[i] and raise_amount > 0: #raise if we want and if we can afford it
                        my_actions[i] = RaiseAction(raise_amount)
                        commit_cost = board_cont_cost+raise_amount
                        total_raise_reserve -= raise_amount
                        # classify self action as well
                        # and update history
                        self_action = classify_action(raise_amount - opp_pips[i], raise_amount + opp_pips[i] + board_total)
                        self.history[i] += self_action
                    
                    elif CallAction in legal_actions[i] and raise_amount >=0: 
                        my_actions[i] = CallAction()
                        commit_cost = board_cont_cost #the cost to call is board_cont_cost
                        self.history[i] += "C"
                    
                    elif CheckAction in legal_actions[i] and raise_amount >=0: #checking is our only valid move here
                        my_actions[i] = CheckAction()
                        commit_cost = 0
                        self.history[i] += "C"
                    
                    else:
                        if FoldAction in legal_actions[i]:
                            # if decide to fold, then the raise reserve could be increased
                            my_actions[i] = FoldAction()
                            total_raise_reserve += board_cont_cost
                            self.history[i] += "F"
                        else:
                            my_actions[i] = CheckAction()
                            self.history[i] += "C"


        # update street, if we are not assigning
        if self.prev_street < street and not AssignAction in legal_actions[0]:
            self.prev_street = street
        return my_actions

if __name__ == '__main__':
    run_bot(Player(), parse_args())
