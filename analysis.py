import matplotlib
import re
filename = "gamelog.txt"
REGEX_BLIND = "(.) posts the blind of (\d)"
REGEX_ASSIGN = "(.) assigns \[(.*)\] to board (\d)"
REGEX_CALL = "(.) calls on board \d"
REGEX_RAISE = "(.) raises to (\d+) on board (\d)"
REGEX_BET = "(.) bets (\d+) on board (\d)"
REGEX_REVEAL = "(Flop|Turn|River) \[(.*)\], \(\d+\), (.) \(\d+\), (.) \(\d+\) on board (\d)"
REGEX_SHOW = "? shows \[.*\] on board (\d)"
with open(filename, "r") as f:
    f.readline() 
    f.readline() # discard the header
    line = "start"
    number_of_raise = {'A':0,'B':0}
    all_raises = {'A':[], 'B': []}
    #read until EOF
    while len(line) > 0:
        #read until the next blank line, which marks the end of the game
        A_hands = []
        B_hands = []
        round_raises = {'A':[[], [], []], 'B':[[], [], []]}
        B_raises = [[], [], []]
        streets = [[], [], []]
        A_pip = [0,0,0]
        B_pip = [0,0,0]
        line = f.readline()
        while len(line) > 1:
            #regex match the line
            words = line.split(" ")
            #deal with revealing cards
            if words[0] in ["Flop", "Turn", "River"]:
                result = re.match(REGEX_REVEAL, line)
                cards, board = result.group(2, 5)
                streets[int(board) - 1] = cards.split(" ")
                print(streets)
            #deal with making bets
            else:
                #calls
                if words[1] == "raises":
                    result = re.match(REGEX_RAISE)
                    player, amount, board = result.group(1, 2, 3)
                    board = int(board) - 1
                    amount = int(amount)
                    if player == 'A':
                        A_raises[board].append(amount)
            line = f.readline()
                
                            
