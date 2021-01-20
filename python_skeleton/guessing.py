# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 14:06:03 2021

@author: 1
"""

class Guessing:
    def __init__(self):
        self.single=set()
        # A set of SINGLE cards (strs)
        # The cards that can make a good hand, such as pairs
        # The cards here ONLY CONTAIN THE NUMBER OF THE CARD
        self.potentialSingles=set()
        # the cards that can potential make a really good hand, such that make a straight
        # but less than 1.
        # It should be EMPTY if state=5
        self.strongSingles=set()
        # It is applicable to be in state=3,4
        # It contains the cards (WITH SUIT) that forms a really good hand 
        # such as >=3 of a kind 
        # excluded the cards in singles
        self.majorSuit = None
        # It is defined as the most likely suit (str) to have a flush.
        # 3, 4: suit of two
        # 5: suit of three of the same suit
        self.majorSuit2=None
        # If there are four cards on 
        self.doubles = set();
        # The pairs of cards that can potentially make a good hand.
        # DOES NOT include cases above.
        self.common=set();
        # The common cards on the board
        self.state=3;
        # The state for the board.
        
    def Guessing(self,three):
        '''
        Initial three cards on the board
        Parameters: three: a list of strs, first three cards for guessing.
        * Update the class.
        '''
        #Initializing
        self.initialGuess();
        
    def initialGuess(self):
        pass
    
    def update3To4(self,fourth):
        '''
        Parameters:
            fourth : a str, the fourth card
        '''
        pass
    
    def update4To5(self,fifth):
        '''
        Parameters: fifth : a str, the fifth card
        '''
        pass
    
    def taheAction(self,action):
        '''
        Parameters:
        action : int, indicates the opponent's action.
        It is either a positive number (raise, the amount of)
        Or 0 (ckeck/call)
        Or -1 for fold
        '''
        pass
    
    def outputGuessing(self):
        '''
        output some sort of the guessing for the bot
        '''
        pass
