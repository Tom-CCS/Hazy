import eval7
import random
import json
"""
Handle Probability Computation
"""
PROBABILITIES={}
filename="raw_prob.json"
with open(filename,'r') as load_f:
    PROBABILITIES = json.load(load_f)

def raw_prob(card1, card2):
    '''
    Parameters: two strings
        represent two cards, card1 and card2
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

def calc_prob(cards, common_cards, guessing_opponent=None):
    '''
    Parameters:
        cards: The list (of length 2) of different strings
            indicates the cards we have
        shown_cards: A list of different Cards, length being 0,3,4,5
            indicates the cards to be shown
            The list is not intersecting with the previous list!
        guessing_opponent: A list of cards,
            we guess what cards the opponent have.
            currently, we set it to None
    Return: the conditional probability of winning. Assume the unseen cards are
    distibuted 
    '''
    if len(common_cards)==0:# same as above, we are blind
        return raw_prob(cards[0],cards[1])
    
    elif len(common_cards)==5: 
    #If we calculate the exact probability for 5 cards, it will eat up <0.002s
        deck=eval7.Deck()
        Card_cards=[eval7.Card(cards[0]),eval7.Card(cards[1])]
        for card in Card_cards+common_cards:
            deck.cards.remove(card)
        score = 0
        for i in range(len(deck)-1):
            for j in range(i+1,len(deck)):
                score+=win_or_lose(Card_cards, common_cards, [deck[i],deck[j]])
        return score / (44*45) #this is our win probability!
    
    #elif len(common_cards)==4: 
    # #If we calculate the exact probability for 4 cards, it will eat up ~0.073s
    # #It may be long and we may need to merge into the next case.
    #   deck=eval7.Deck()
    #    for card in cards+common_cards:
    #        deck.cards.remove(eval7.Card(str(card)))
    #    score = 0
    #    for i in range(len(deck)-1):
    #        for j in range(i+1,len(deck)):
    #            for k in range(len(deck)):
    #                if k!=j and k!=i:
    #                    score+=win_or_lose(cards, common_cards+[deck[k]], [deck[i],deck[j]])
    #    return (score) / (44*45*46) #this is our win probability!
    else: 
    # Please, if you find the above slow, 
    # do delete the len(common_cards)==4 case above.
    # 1000 iterations will cost up to ~0.021s. If you find it slow, please lower it.
        deck=eval7.Deck()
        Card_cards=[eval7.Card(cards[0]),eval7.Card(cards[1])]
        for card in Card_cards+common_cards:
            deck.cards.remove(card)
            #print(card)
            #print(type(card))
        score = 0
        iteration = 100# The iteration
        for i in range(iteration):
            score+=win_or_lose(Card_cards, common_cards, opponent_hand=[], rest=deck)
        return score/(2*iteration)
            
            
def win_or_lose(our_hand, current_common, opponent_hand=[], rest=None):
    '''
    Parameters:
        our_hand: The list (of length 2) of different Cards
            indicates the cards we have
        opponent_hand: A List of lists (of length 2) of different Cards
            indicates the cards the opponent have.
            [] (empty list): the opponents' cards are not known
        current_common: The list (of length 2) of different Cards
            indicates the common cards
        shuffle: A boolean
            Indicates whether the missing card need to be randomly chosen
        rest: A Deck of card
            Indicates the rest of the card. Default is None (to be calculated).
    Return: An integer to indicate the total wins/loses divided by n.
    '''
    if len(opponent_hand)==0:
        if rest==None:
            rest=eval7.Deck()
            for card in our_hand+opponent_hand+current_common:
                rest.cards.remove(card)
        rest.shuffle() #make sure our samples are random
        
        _COMM = 5-len(current_common) #the number of cards we need to draw
        _OPP = 2-len(opponent_hand)
    
        draw = rest.peek(_COMM + _OPP)
        opp_hole = draw[: _OPP]
        community = current_common+draw[_OPP: ]
        
        our_cards = our_hand + community #the two showdown hands
        opp_cards = opp_hole + community
    else:
        our_cards = our_hand + current_common #the two showdown hands
        opp_cards = opponent_hand + current_common

    our_hand_value = eval7.evaluate(our_cards) #the ranks of our hands (only useful for comparisons)
    opp_hand_value = eval7.evaluate(opp_cards)

    if our_hand_value > opp_hand_value: #we win!
        return 2
    
    elif our_hand_value == opp_hand_value: #we tie.
        return 1
    
    else: #we lost....
        return 0

'''
#Timer
import time
ST=time.time()
calc_prob([Kc,Kd],[Kh,Td,Ks])
ED=time.time()
print(ED-ST)
'''

calc_prob(["4c","4d"],[eval7.Card("8s"),eval7.Card("3h"),eval7.Card("Ts"),eval7.Card("8d")])