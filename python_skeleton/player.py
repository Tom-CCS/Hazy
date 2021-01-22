'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction, AssignAction
from skeleton.states import GameState, TerminalState, RoundState, BoardState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND, NUM_BOARDS
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

from probability import raw_prob, calc_prob, calcBiasedProb, raw_prob
from algo_for_next_step import algorithm
from allocate import allocate
from behaviour_study import is_all_in
from guessing import Guessing

import eval7
import random
import json

#characterize all-in bots
LARGE_RAISE_THRESHOLD = 100
#hybrid algorithm
num_alg = 3
algo_timid = {"RAISE_THRES": 0.7, "RAISE_RATIO": 0.4}
algo_normal = {"RAISE_THRES": 0.5, "RAISE_RATIO": 0.4}
algo_aggressive = {"RAISE_THRES": 0.5, "RAISE_RATIO": 0.6}
algorithms = [algo_timid, algo_normal, algo_aggressive]
#The winning probabilities for RAW first two cards,
#calculated OUTSIDE this program and stored in prob.json file.
PROBABILITIES={}
filename="raw_prob.json"
with open(filename,'r') as load_f:
    PROBABILITIES = json.load(load_f)


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

        self.large_raise_count = 0 # count the number of raises greater than LARGE_RAISE_THRESHOLD made
        self.round_count = 0 # count the number of rounds elapsed
        self.algo_index = -1
        self.algo = []
        
        self.guessings=[None,None,None]
        # The guessings for these three boards.
        
        self.last_turn_state=[0,0,0]
        # the jth position is i if it is the last turn is state i on jth board.

        #different possibility of taking each algorithm
        self.algorithms_prob = [0.3, 0.3, 0.4]
        #the gain each algorithm achieved
        self.algorithms_gain = [0] * num_alg

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

    def choose_algo(self):
        '''
        Called for each round. Choose the algorithm parameter for this round.

        Returns:
        A random algorithm parameter from algorithms, as well as its index
        where each algorithm is chosen with probability algorithms_prob
        '''
        seed = random.random()
        i = 0
        sum = 0
        while True:
            sum += self.algorithms_prob[i]
            if seed < sum:
                break
            i += 1
        return i, algorithms[i]
             
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

        self.algo_index, self.algo = self.choose_algo() # select the algo parameters for this round
        
        self.allocate_cards(my_cards) #our old allocation strategy

        self.round_count += 1 

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
        self.guessings=[None]*3
        self.last_turn_state=[0,0,0]

        game_clock = game_state.game_clock #check how much time we have remaining at the end of a game
        round_num = game_state.round_num #Monte Carlo takes a lot of time, we use this to adjust!
        if round_num == NUM_ROUNDS:
            print(game_clock)

        #update the gains of an algorithm
        self.algorithms_gain[self.algo_index] += (my_delta - opp_delta)
        #update our inference on how to weight each algorithm after 150 rounds
        if round_num == 150:
            #you can tune this parameter here
            for i in range(num_alg):
                self.algorithms_prob[i] += self.algorithms_gain[i] * 0.0005
                self.algorithms_gain[i] = 0
                if self.algorithms_prob[i] < 0:
                    self.algorithms_prob[i] = 0
            #normalize
            s = sum(self.algorithms_prob)
            if s == 0:
                self.algorithms_prob = [0.3, 0.3, 0.4]
            else:
                for i in range(num_alg):
                    self.algorithms_prob[i] /= s
            print(self.algorithms_prob)



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
        my_actions = [None] * NUM_BOARDS
        net_cost = 0 # keep track of the net additional amount you are spending across boards this round
        total_cont_cost = sum(continue_cost) # the minimum number of chips to keep playing at all the tables
        total_raise_reserve = my_stack - total_cont_cost
        for i in range(NUM_BOARDS):
            # Study opponent behaviour
            # Decide if the opponent just made a large raise
            if continue_cost[i] > LARGE_RAISE_THRESHOLD:
                self.large_raise_count += 1

            # Decide own action
            if AssignAction in legal_actions[i]: # This indicates it is the allocating round
                cards = self.board_allocations[i] #allocate our cards that we made earlier
                my_actions[i] = AssignAction(cards) #add to our actions
                
            elif isinstance(round_state.board_states[i], TerminalState): #make sure the game isn't over at this board
                my_actions[i] = CheckAction() #check if it is
            
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
                    board_cont_cost = continue_cost[i] #we need to pay this to keep playing
                    board_total = round_state.board_states[i].pot #amount before we started betting
                    pot_total = my_pips[i] + opp_pips[i] + board_total #total money in the pot right now
                    min_raise, max_raise = round_state.board_states[i].raise_bounds(active, round_state.stacks)
                    
                    ###########################
                    #                         #
                    #  My added code is here  #
                    #                         # 
                    ###########################
                    '''
                    #print(min_raise,max_raiseboard_cont_cost)
                    #print("board_cards : ",board_cards)
                    seen_cards=[]
                    for card in board_cards[i]:
                        if card!='':
                            seen_cards.append(eval7.Card(caard))
                    #print(self.board_allocations[i])
                    #print(seen_cards)
                    win_prob=calc_prob(self.board_allocations[i],seen_cards)
                    '''
                    if street == 0:
                        # Only raw probs are Okay
                        win_prob = raw_prob(self.board_allocations[i][0],self.board_allocations[i][1])
                    else:
                        if self.last_turn_state[i] != street:
                            if street==3:
                                self.guessings[i] = Guessing(board_cards[i][:3],self.board_allocations[i])
                            elif street==4:
                                self.guessings[i].update3To4(board_cards[i][3])
                            else:
                                self.guessings[i].update4To5(board_cards[i][4])
                        if self.last_turn_state[i] != street or board_cont_cost > 0:
                            # We are encountering a raise
                            # Or a check of others
                            # This is all the cases when we are not 1st hand
                            # And we should update
                            self.guessings[i].takeAction(board_cont_cost)
                        self.last_turn_state[i] =  street
                        win_prob = calcBiasedProb(self.guessings[i])
                    
                    
                    ###########################
                    #                         #
                    # My added code ends here #
                    #                         # 
                    ###########################
                    #adjust algorithm if the opponent is all-in
                    if is_all_in(self.large_raise_count, self.round_count):
                        #TODO: Optimize this
                        algo = algorithm(INTIMIDATE_DEC=lambda x: 0.9 if x > 0 else 1)
                    else:
                        algo = algorithm(RAISE_THRES=self.algo["RAISE_THRES"] ,RAISE_RATIO = self.algo["RAISE_RATIO"])
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
