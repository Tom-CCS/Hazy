import eval7
import random
def algorithm(INTIMIDATE_PROB=1.0, INTIMIDATE_DEC=0.7, RAISE_PROB=1.0, RAISE_DEC=1.0, RAISE_THRES=0.5, RAISE_RATIO=0.75):
    '''
    Parameters:
        INTIMIDATE_PROB: a float in [0,1]. Set to 1.0.
            the "probability" that the opponent has a good hand when a large raise is made
        INTIMIATE_DEC: a float in [0,1]. Set to 0.7
            the decrease in win probability we should factor in when the opponent is intimidating
        RAISE_PROB: a float in [0,1]. Set to 1.0
            the "probability" that the opponent has a good hand when a small raise is made
        RAISE_DEC: a float in [0,1]. Set to 1.0
            the decrease in win probability we should factor in when the opponent is intimidating

        RAISE_THRES: a float in [0,1]. Set to 0.5
            how large win_prob must be to consider a raise.
        RAISE_RATIO: a float in [0,1]
            how large we should raise. Set to 0.75
            The formula for raising is my_pips + cont_cost + RAISE_RATIO * (current_pot + cont_cost)
        
    Return:
        The action algorithm
    '''
    def action(win_prob, current_pot, my_pot, continue_cost, raise_range):
        '''
        Parameters:
        win_prob: a float in [0,1]
            represents the probability of winning.
        current_pot: an integer >=0
            represents the current money in the pot.
        my_pot: an integer >= 0
            represents the current money in my pot
        continue_cost: an integer >=0
            represents the cost for continuing the game.
        raise_range: a tuple of 2 integers
            represents the minimum/maximum amount that we are allowed to raise
        
        Returns:
            an integer n, such that:
            n=-1 if fold
            n=0 if check (or call)
            n>0 for raise the money with n.
        '''
        intimidate_guess=10
        # a parameter to guessing if the opp is intimidating
        # use as continue_cost>intimidate_guess
        
        intimidate=False
        # a parameter represent whether we are going to intimidate
        # in this round
        
        #decrease win_prob is the opponent is intimidating
        #as the opponent's hand might be very good
        if continue_cost > intimidate_guess:
            if random.random() < INTIMIDATE_PROB:
                win_prob *= INTIMIDATE_DEC
        #decrease win_prob if opponent just raised
        #as the opponent might have a good hand
        elif continue_cost > 0:
            if random.random() < RAISE_PROB:
                win_prob *= RAISE_DEC

        #precompute the amount to raise if we decide to
        #test if we could afford to raise
        if raise_range[0] > raise_range[1]:
            raise_amount = 0
        else:
            raise_amount = my_pot + continue_cost + RAISE_RATIO * (current_pot + continue_cost) * 0.4
            if win_prob > 0.7:
                raise_amount += RAISE_RATIO * (current_pot + continue_cost) * 0.75
            raise_amount = (int)(raise_amount)
        
        truncated_raise_amount = min(raise_amount, raise_range[1])
        truncated_raise_amount = max(truncated_raise_amount, raise_range[0])
        
        #the opponent just raised
        if continue_cost > 0:
            #find the pot odds
            pot_odds = continue_cost / (current_pot + continue_cost)
            #we do not have positive gain, fold
            if pot_odds > win_prob:
                return -1
            #we still have positive gain, decide if to raise
            else:
                #if our hand is good enough, raise, else fold
                if win_prob > RAISE_THRES and random.random() < win_prob and raise_amount > raise_range[0]:
                    return truncated_raise_amount
                else:
                    return 0
        #the opponent did not just raise. we have control.
        else:
            #if our hand is good enough, raise, else fold
            if win_prob > RAISE_THRES and random.random() < win_prob:
                return truncated_raise_amount
            else:
                return 0

    return action
