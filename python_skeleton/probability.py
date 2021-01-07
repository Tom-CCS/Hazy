import eval7
import random
import json
"""
Handle Probability Computation
"""
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

def calc_prob(self, i, shown_cards):
    '''
    Parameters:
        i: The ith board (i=0,1,2)
        shown_cards: the number of cards shown
    Return: the probability of winning
    '''
    pass
