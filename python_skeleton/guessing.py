# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 14:06:03 2021

@author: 1
"""
import numpy as np
import random
class Guessing:
    def __init__(self,three,ours):
        '''
        Initial three cards on the board
        Parameters: 
        three: a list of 3 strs, first three cards for guessing.
        ours: our cards, a list of 2 strs
        Update the class.
        '''
        self.singles=set()
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
        
        # A card can be in one or two sets of single or potentialSiggles,
        # But never be in strongSingles and another singles
        self.majorSuit = ""
        # It is defined as the most likely suit (str) to have a flush.
        # 3, 4: suit of two
        # 5: suit of three of the same suit
        self.majorSuit2=""
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
        self.guessing={}
        # self.rise=set()
        num=2
        for i in "23456789TJQKA":
            self.rank2num[i]=num
            self.leftRanks[num]=4
            self.guessing[num]=(num-10)*(num>10)+(num<=10)
            num+=1
        self.restCards={i+j for i in "23456789TJQKA" for j in "cdhs"}
        # A set of rest cards in order to give prob easier
        for card in three+ours:
            self.restCards.remove(card)
        self.initialGuess()
        
    def initialGuess(self):
        # Initialize the informations
        for card in self.common:
            if self.rank2num[card[0]] in self.ranks.keys():
                self.ranks[self.rank2num[card[0]]]+=1
            else: self.ranks[self.rank2num[card[0]]]=1
            self.leftRanks[self.rank2num[card[0]]]-=1
            if card[1] in self.suits.keys():
                self.suits[card[1]]+=1
            else: self.suits[card[1]]=1
            self.leftSuits[card[1]]-=1
        for card in self.ours:
            self.leftRanks[self.rank2num[card[0]]]-=1
            self.leftSuits[card[1]]-=1
        
        # A pair of Ace or triples are really stong, otherwise, just so so
        for rank in self.ranks.keys():
            if rank==14 or self.ranks[rank]>=2:
                self.strongSingles.add(rank)
            else: self.singles.add(rank)
        
        # Find the potential straights
        smallStraight=self.findStraight()[0]
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
        small straight: if three of n n+1 n+2 n+3 are in and n-1 and n+4 are 
        not, put the rest one in the small straight (if applicable)
        big straight: if n n+1 n+2 n+3 are in and n-1 and n+4 are not, put
        these two in the big straight. If n, n+4 are in and two of n+1, n+2,
        n+3 are in, put the third in.
        '''
        smallStraight=set()
        bigStraight=set()
        ranks=set(self.ranks.keys())
        if len(ranks)<3:
            return set(), set()
        else:
            for i in range(2,13):
                if i in ranks:
                    # n n+1 n+2 small straight
                    if i in ranks and i+1 in ranks and i+2 in ranks:
                        smallStraight.add((i-3)%13+2)
                        if i<12: smallStraight.add(i+3)
                    
                    # n n+1/n+2 n+3 small straight
                    if i<12 and i+3 in ranks: 
                        if i+1 in ranks: smallStraight.add(i+2)
                        if i+2 in ranks: smallStraight.add(i+1)
                    
            if 14 in ranks and 2 in ranks:
                if 4 in ranks: smallStraight.add(3)
                if 3 in ranks: smallStraight.add(4)
            
            smallStraight.difference_update(ranks)
            
            # state-3 will not have big straight
            if self.state==3: return smallStraight, set()
            
            if len(ranks)>=4:
                # 4 of the 5 of a straight is gathered.
                for i in ranks:
                    if len(ranks.intersection({i,i+1,i+2,i+3,i+4}))==4:
                        if i+4 not in ranks:
                            if i!=11: bigStraight.add(i+4)
                            bigStraight.add((i-3)%13+2)
                        else:
                            bigStraight.add((5*i+10)-sum(ranks.intersection({i,i+1,i+2,i+3,i+4})))
                
                if ranks.intersection({14,2,3,4,5})==4:
                    bigStraight.add(28-sum(ranks.intersection({14,2,3,4,5})))
                        
                bigStraight.difference_update(ranks)
                smallStraight.difference_update(bigStraight)
            
            if self.state==4:
                return smallStraight, bigStraight
            else:
                return set(), bigStraight
    
    def update3To4(self,fourth):
        '''
        Parameters: fourth : a str, the fourth card
        #Return the rising .
        Update the fields in this class
        NOTE: if okay, report the change
        NOTE2: for robustness, if it is updated, we will not update it again.
        '''
        if self.state==3:
            self.restCards.remove(fourth)
            self.common.add(fourth)
            self.state=4
            self.leftSuits[fourth[1]]-=1
            # rising=set()
            
            # update for suits
            suit=fourth[1]
            if suit not in self.suits.keys():
                self.suits[suit]=1
            else:
                self.suits[suit]+=1
            if self.suits[suit]==2:
                # 2 cases, 2+2 or 1+1+2
                if 1 in self.suits.values():
                    self.majorSuit=suit
                else:self.majorSuit2=suit
            
            # update for ranks
            rank=self.rank2num[fourth[0]]
            self.leftRanks[rank]-=1
            if rank not in self.ranks.keys():
                self.ranks[rank]=1
                if rank==14:
                    self.strongSingles.add(rank) # only one pair
                else: self.singles.add(rank)
            else: # at least 3 of a kind
                self.ranks[rank]+=1
                if rank in self.singles: self.singles.remove(rank)
                self.strongSingles.add(rank)
            # if self.ranks[rank]==2:
            #    rise.add(rank)
            
            # take care of straights
            smallStraight, bigStraight=self.findStraight()
            # for rank in bigStraight:
            #     if rank not in strongSingles:
            #         rise.add(rank)
            self.strongSingles|=bigStraight
            self.potentialSingles|=smallStraight
            self.potentialSingles.difference_update(self.strongSingles)
    
    def update4To5(self,fifth):
        '''
        Parameters: fifth : a str, the fifth card
        Does not return anything.
        Update the fields in the class
        NOTE: if okay, report the change.
        NOTE2: for robustness, if it is updated, we will not update it again.
        '''
        if self.state==4:
            self.restCards.remove(fifth)
            self.common.add(fifth)
            self.state=5
            suit=fifth[1]
            # rise=set()
            
            # update for suits
            if suit not in self.suits.keys():
                self.suits[suit]=1
            else:
                self.suits[suit]+=1
            if 3 not in self.suits.values():
                self.majorSuit, self.majorSuit2=None,None
            elif self.suits[suit]==3:
                self.majorSuit=suit
                self.majorSuit2=None
            
            # update for ranks
            rank=self.rank2num[fifth[0]]
            self.leftRanks[rank]-=1
            if rank not in self.ranks.keys():
                self.ranks[rank]=1
                if rank==14:
                    self.strongSingles.add(rank) # only one pair
                else: self.singles.add(rank)
            else: # at least 3 of a kind
                self.ranks[rank]+=1
                if rank in self.singles: self.singles.remove(rank)
                self.strongSingles.add(rank)
            # if self.ranks[rank]==2:
            #    rise.add(rank)
            
            # we will not care for the XXXYY case in the common card. (X>Y)
            # In this case, Y is not strong
            # It is really rare, like 1.08 occurrences in 500 games
            
            # take care of straights
            bigStraight=self.findStraight()[1]
            # for rank in bigStraight:
            #     if rank not in strongSingles:
            #         rise.add(rank)
            self.strongSingles|=bigStraight
        
    def takeAction(self,action):
        '''
        Parameters:
        action : int, indicates the opponent's action.
        It is either a positive number (raise, the amount of)
        Or 0 (ckeck/call)
        Or -1 for our hand first
        '''
        # Our first hand, we do nothing
        if action==0:
            for i in self.singles:
                self.guessing[i]*=(self.state/2)
            for i in self.potentialSingles:
                self.guessing[i]*=(self.state/2)
            for i in self.strongSingles:
                self.guessing[i]*=(self.state/2)
        elif action>0:
            for i in self.singles:
                self.guessing[i]*=(self.state/2)
            for i in self.potentialSingles:
                self.guessing[i]*=(self.state/2)
            for i in self.strongSingles:
                self.guessing[i]*=self.state
    
    def outputGuessing(self,pairs):
        '''
        Parameters: pairs: the number of the pairs to be output.
        output some sort of the guessing for the bot
        output the probability for each card (rank)
        '''
        output=[]
        cards=[]
        prob=[]
        for card in self.restCards:
            try:
                prob.append(self.guessing[self.rank2num[card[0]]]/self.leftRanks[self.rank2num[card[0]]])
                cards.append(card)
            except:
                pass
        cards=np.array(cards)
        s=sum(prob)
        prob=np.array(prob)/s
        if self.state<5:
            for i in range (pairs):
                while True:
                    choice=np.random.choice(cards,2,replace=True,p=prob)
                    if choice[0]!=choice[1]:
                        common=set(random.sample(self.restCards-set(choice),5-self.state))
                        output.append([list(choice),common])
                        break
            return output
        else:
            for i in range (pairs):
                while True:
                    choice=np.random.choice(cards,2,replace=True,p=prob)
                    if choice[0]!=choice[1]:
                        output.append(list(choice))
                        break
            return output