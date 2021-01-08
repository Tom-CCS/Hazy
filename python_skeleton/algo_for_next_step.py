import eval7
def algorithm(hyperparameters):
    '''
    Parameters:
        Some hyperparameters.
    Return:
        The action algorithm
    '''
    def action(win_prob, current_pot, continue_cost):
        '''
        Parameters:
        win_prob: a float in [0,1]
            represents the probability of winning.
        current_pot: an integer >=0
            represents the current money in the pot.
        continue_cost: an integer >=0
            represents the cost for continuing the game.
        
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
        
        pass
    return action