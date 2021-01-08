from probability import raw_prob 
import eval7   
def allocate(my_cards):
    """
    Parameters:
    cards: a list of 6 cards

    Returns:
        3 pairs of cards, determining how we would allocate our hand
        plus other related parameters
    """
    """
    Parameters
    """
    NUM_BOARDS = 3
    PLAY_HIGH_THRES = 0.6
    PLAY_MID_THRES = 0.5

    max_prob=0
    best=[]#Best pair
    for i in range(2*NUM_BOARDS-1):
        for j in range(i+1,2*NUM_BOARDS):
            if raw_prob(my_cards[i],my_cards[j])>max_prob:
                max_prob=raw_prob(my_cards[i],my_cards[j])
                best=[my_cards[i],my_cards[j]]
                
    rest=[]
    for card in my_cards:
        if card not in best:
            rest.append(card)
            
    second_max_prob=0
    second_best=[]#Second best pair
    for i in range(2*NUM_BOARDS-3):
        for j in range(i+1,2*NUM_BOARDS-2):
            if raw_prob(rest[i],rest[j])>second_max_prob:
                second_max_prob=raw_prob(rest[i],rest[j])
                second_best=[rest[i],rest[j]]
    
    worst=[]
    for card in rest:
        if card not in second_best: worst.append(eval7.Card(str(card)))
        
    if max_prob>PLAY_HIGH_THRES:# We can have a really good card
        return [worst, second_best, best], 2
    elif max_prob>PLAY_MID_THRES:# We can get a fair pair
        return [second_best, best, worst], 1
    else:# We have really bad luck
        return [best, worst, second_best], 0
