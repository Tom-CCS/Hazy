def magnitude(cards):
    '''
    Parameter: 
        cards: A list of 5 strings of [2-9TJQKA][cdhs]. It represent a card set.
        (it also applicable to a [set] of strings)
    Return: the "magnitude" of the card, such that if the cardset 1 is smaller than
    cardset 2, then the magnitude of cardset 1 is smaller than cardset 2.
    '''
    classify=1<<20
    # 10 classes of cards: 
    # royal_flush=10; straight_flush=9; four_of_a_kind=8; full_house=7;
    # flush=6; straight=5; three_of_a_kind=4; two_pairs=3; one_pair=2;
    # high_card=1
    kickers=[1<<16,1<<12,1<<8,1<<4,1]
    card_dict=to_dict(cards)
    if is_flush(cards):
        if is_straight(card_dict):
            if set(cards)==set(("As","Ks","Qs","Js","Ts")): return 10*classify
            # A royal flush
            else: return is_straight(card_dict)*kickers[0]+9*classify
            # A straight flush
        else: # a flush
            mag=6*classify
            for i in range(5):
                MAX=max(card_dict.keys())
                del card_dict[MAX]
                mag+=MAX*kickers[i]
            return mag
    else:
        if is_straight(card_dict): # a straight
            return is_straight(card_dict)*kickers[0]+5*classify
        else:
            if 4 in card_dict.values(): # Four of a kind
                print("yay")
                mag=8*classify
                for k,v in card_dict.items():
                    if v==4: mag+=kickers[0]*k
                    else: mag+=kickers[1]*k
                return mag
            elif 3 in card_dict.values(): # 3 of a kind or full house
                if 2 in card_dict.values(): # full house
                    mag=7*classify
                    for k,v in card_dict.items():
                        if v==3: mag+=kickers[0]*k
                        else: mag+=kickers[1]*k
                    return mag
                else: # Three of a kind
                    singles=set()
                    mag=4*classify
                    for k,v in card_dict.items():
                        if v==3: mag+=kickers[0]*k
                        else: singles.add(k)
                    return mag+max(singles)*kickers[1]+min(singles)*kickers[2]
            elif 2 in card_dict.values(): # One pair or two pairs:
                pairs=set()
                singles=set()
                for k,v in card_dict.items():
                    if v==2: pairs.add(k)
                    else: singles.add(k)
                if len(pairs)==2: # two pairs
                    return 3*classify+max(pairs)*kickers[0]+min(pairs)*kickers[1]+max(singles)*kickers[2]
                else:
                    return 2*classify+max(pairs)*kickers[0]+max(singles)*kickers[1]+(sum(singles)-max(singles)-min(singles))*kickers[2]+min(singles)*kickers[3]
            else:
                mag=1*classify
                for i in range(5):
                    MAX=max(card_dict.keys())
                    del card_dict[MAX]
                    mag+=MAX*kickers[i]
                return mag
    
def to_dict(cards):
    '''
    Parameters:
    cards : A list of 5 strings of [2-9TJQKA][cdhs]. It represent a card set.
    (it also applicable to a [set] of strings)
    Returns: A dictionary representation for cards, compressed by NUMBERS only
    '''
    mag={"T":10,"J":11,"Q":12,"K":13,"A":14}
    for i in "23456789": mag[i]=int(i)
    card_dict={}
    for card in cards:
        if mag[card[0]] not in card_dict.keys():
            card_dict[mag[card[0]]]=0
        card_dict[mag[card[0]]]+=1
    return card_dict

def is_straight(card_dict):
    '''
    Parameters:
    card_dict: a dictionary of cards, transformed by the previous funtion.
    Returns 0 if it is not a straight, or the largest number of the straight
    if it is a straight
    '''
    smallest=min(card_dict.keys())
    if smallest==2:
        for i in range(3):
            if smallest+i+1 not in card_dict.keys():
                return 0
        if 6 in card_dict.keys(): return 6
        elif 14 in card_dict.keys(): return 5
        return 0
    else:
        for i in range(4):
            if smallest+i+1 not in card_dict.keys():
                return 0
        return smallest+4

def is_flush(cards):
    '''
    Parameters:
    cards : a list of 5 strings of [2-9TJQKA][cdhs]. It represents a card set.
    (it also applicable to a [set] of strings)
    Returns: a boolean to detect whether it is a flush.
    '''
    suit=None
    flag=True
    for card in cards:
        if flag: suit=card[1]; flag=False
        else: 
            if card[1]!=suit:
                return False
    return True
