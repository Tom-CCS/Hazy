#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 21:17:52 2021
"""

'''
This serves as something we can use to deal with eval7
'''

import eval7
import random

'''
BASIC USAGE:

deck=eval7.Deck() # The deck is a full deck of card
deck.shuffle() # A function to shuffle the deck
card=eval7.Card("As") # A card
cards=deck.cards # A [list] of cards, The cards of a deck
cards.remove(eval7.Card("As"))
cards.remove(eval7.Card("Ac"))
cards.remove(eval7.Card("Ad"))
cards.remove(eval7.Card("Ah"))
#These moves really REMOVES the cards of a deck
eva=eval7.evaluate([eval7.Card("As"),eval7.Card("2s"),eval7.Card("3s"),eval7.Card("4s"),eval7.Card("5s"),eval7.Card("6s")])
#This evaluates the combination of cards
'''
 
'''
The next calculates the UN-conditional probability for winning in all pairs (we
did not distinguish roal flush and straight flush: they are truly super rare
'''

import json

filename="raw_prob.json"

full_deck=eval7.Deck()

probabilities={}

l=len(full_deck)
iters=1000000

def calc_prob(card1,card2):
    deck = eval7.Deck() #eval7 object!
    deck.cards.remove(card1)
    deck.cards.remove(card2)
    score = 0
    for _ in range(iters): #take 'iters' samples
        deck.shuffle() #make sure our samples are random

        _COMM = 5 #the number of cards we need to draw
        _OPP = 2

        draw = deck.peek(_COMM + _OPP)

        opp_hole = draw[: _OPP]
        community = draw[_OPP: ]

        our_hand = [card1, card2] + community #the two showdown hands
        opp_hand = opp_hole + community

        our_hand_value = eval7.evaluate(our_hand) #the ranks of our hands (only useful for comparisons)
        opp_hand_value = eval7.evaluate(opp_hand)

        if our_hand_value > opp_hand_value: #we win!
            score += 2
        
        elif our_hand_value == opp_hand_value: #we tie.
            score += 1
        
        else: #we lost....
            score += 0
    
    return score / (2 * iters) #this is our win probability!

#import time
#ST=time.time()
ALL=325
count=1
nums="23456789TJQKA"
for i in range(12):
    for j in range(i+1,13):
        suited=calc_prob(eval7.Card(nums[i]+"c"),eval7.Card(nums[j]+"c"))
        print("calculated ",count, "/ 325")
        count+=1
        unsuited=calc_prob(eval7.Card(nums[i]+"c"),eval7.Card(nums[j]+"d"))
        print("calculated ",count, "/ 325")
        count+=1
        probabilities[nums[i]+nums[j]+"s"]=suited
        probabilities[nums[i]+nums[j]+"u"]=unsuited

for i in nums:
    pairs=calc_prob(eval7.Card(i+"c"),eval7.Card(i+"d"))
    print("calculated ",count, "/ 325")
    count+=1
    probabilities[i+i]=pairs
#ED=time.time()

with open(filename,"w") as file_obj:
    json.dump(probabilities,file_obj)

print(probabilities)