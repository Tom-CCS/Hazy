# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 14:06:03 2021

@author: 1
"""

class Guessing:
    def __init__(self,three,ours):
        '''
        Initial three cards on the board
        Parameters: 
        three: a list of 3 strs, first three cards for guessing.
        ours: our cards, a list of 2 strs
        Update the class.
        '''
        self.single=set()
        # A set of SINGLE cards (ints)
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
        # If there are four cards on, ans the suits are 2+2
        self.doubles = set()
        # The pairs of cards that can potentially make a good hand.
        # DOES NOT include cases above.
        # This is a set of strs
        self.common=set(three)
        self.ours=set(ours)
        # The common and our cards on the board
        self.state=3
        # The state for the board.
        self.ranks={}
        # The ranks
        self.suits={}
        # The suits
        self.leftRanks={}
        self.leftSuits={"c":13, "d":13, "h":13, "s":13}
        # Count hou many cards for a certain ranks / suits have
        self.rank2num={}
        num=2
        for i in "23456789TJKQA":
            self.rank2num[i]=num
            self.leftRanks[num]=4
            num+=1
        self.initialGuess()
        
    def initialGuess(self):
        # Initialize the informations
        for card in self.common:
            if card[0] in self.ranks.keys():
                self.ranks[card]+=1
            else: self.ranks[card]=1
            self.leftRanks[card[0]]-=1
            if card[1] in self.suits.keys():
                self.suits[card]+=1
            else: self.suits[card]=1
            self.leftSuits[card[1]]-=1
        
        # A pair of Ace or triples are really stong, otherwise, just so so
        for rank in self.ranks.keys():
            if rank=="A" or self.ranks[rank]>=2:
                self.strongSingles.add(rank)
            else: self.single.add(rank)
        
        # Find the potential straights
        smallStraight=self.find_straight()[0]
        for rank in smallStraight:
            self.potentialSingles.add(rank)
        
        # Find the potential flush of suit
        for suit in self.suits.keys():
            if self.suits[suit]>1:
                self.majorSuit=suit
                break
    
    def findStraight(self):
        '''
        Returns
        Two sets of ranks(int): small straight and big straight.
        small straight: if n n+1 n+2 are in and n-1 and n+3 are not, put n-1
        and n+3 in the small straight (if applicable)
        big straight: if n n+1 n+2 n+3 are in and n-1 and n+4 are not, put
        these two in the big straight. If n, n+4 are in and two of n+1, n+2,
        n+3 are in, put the third in.
        '''
        smallStraight=set()
        bigStraight=set()
        if self.state==3:
            # In this state, bigStraight must be empty
            pass
        elif self.state==4:
            pass
        else:
            # In this state, small straight are meaningless, so only calc for
            # big straight
            pass
        return smallStraight, bigStraight
    
    def update3To4(self,fourth):
        '''
        Parameters: fourth : a str, the fourth card
        Does not return anything.
        Update the fields in this class
        NOTE: if okay, report the change
        '''
        self.state+=1
        pass
    
    def update4To5(self,fifth):
        '''
        Parameters: fifth : a str, the fifth card
        Does not return anything.
        Update the fields in the class
        NOTE: if okay, report the change.
        '''
        self.state+=1
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
