import eval7
import random
from CFR_engine import getBucket
def determine_action(player, street, oppo_action, win_prob, current_pot, my_pot, continue_cost, raise_range, CFR_dict):
    '''
    Parameters:
    player: [0,1]
        0 if we are SB, 1 if we are BB
    street: [0,3,4,5]
        the current number of street cards
    oppo_action: 
        the action of the opponent
        "C" if check, "R(int)" if raise or bet
        ("D" is very inadequately trained now, so we ignore it)
        In the case of a single raise, the integer stands for the raise above the check amount
    win_prob: a float in [0,1]
        represents the raw probability of winning.
    current_pot, my_pot, continue_cost: an integer >=0
        represents the betting situation
    raise_range: a tuple of 2 integers
        represents the minimum/maximum amount that we are allowed to raise
    CFR_dict: the CFR dictionary
    
    Returns:
        an integer n, such that:
        n=-1 if fold
        n=0 if check (or call)
        n>0 for raise the money with n.
    '''
    # first of all, figure out the magnitude of the opponents raise
    # This is heuristic
    if oppo_action[0] == "R":
        raise_amount = int(oppo_action[1:])
        pre_raise_pot = current_pot - raise_amount
        if (raise_amount < pre_raise_pot * 0.33):
            oppo_action = "C"
        elif (raise_amount < pre_raise_pot):
            oppo_action = "S"
        else:
            oppo_action = "L"
    bucket = getBucket(win_prob, street, oppo_action)
    action_choices = CFR_dict[player][bucket]
    # choose an action based on the recommendation of the CFR
    seed = random.random()
    running_sum = 0
    action_choice = ""
    for action_choice in action_choices:
        running_sum += action_choices[action_choice]
        if running_sum > seed:
            break
    # return in the prescribed format
    if action_choice == "F":
        return -1
    elif action_choice == "C":
        return 0
    else:
        raise_amount = 0
        if action_choice == "S":
            raise_amount = (my_pot + continue_cost) + int((current_pot + continue_cost) * 0.66)
        else:
            raise_amount = 200
        raise_amount = min(raise_amount, raise_range[1])
        raise_amount = max(raise_amount, raise_range[0])
        return raise_amount
