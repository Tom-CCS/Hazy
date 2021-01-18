import matplotlib
import re
filename = "gamelog.txt"
REGEX_BLIND = "(.) posts the blind of (\d)"
REGEX_ASSIGN = "(.) assigns \[(.*)\] to board (\d)"
REGEX_CALL = "(.) calls on board (\d)"
REGEX_CHECK = "(.) checks on board (\d)"
REGEX_RAISE = "(.) raises to (\d+) on board (\d)"
REGEX_FOLD = "(.) folds on board (\d)"
REGEX_BET = "(.) bets (\d+) on board (\d)"
REGEX_REVEAL = "(Flop|Turn|River) \[(.*)\], \((\d+)\), (.) \(\d+\), (.) \(\d+\) on board (\d)"
REGEX_SHOW = "(.) shows \[.*\] on board (\d)"
REGEX_AWARD = "(.) awarded (.*)"
with open(filename, "r") as f:
    f.readline() 
    f.readline() # discard the header
    line = "start"
    line_cnt = 0
    number_of_raise = {'A':0,'B':0}
    total_of_raise = {'A':0,'B':0}
    number_of_folds = {'A':0,'B':0}
    all_raises = {'A':[], 'B': []}
    awards = {'A': [], 'B': []}
    #read until EOF
    while len(line) > 0:
        #read until the next blank line, which marks the end of the game
        #initialize board
        A_hands = []
        B_hands = []
        board_pots = [2, 4, 6] # the initial board inflation, blinds included
        round_raises = {'A':[[], [], []], 'B':[[], [], []]}
        streets = [[], [], []]
        pips = {'A':[0,0,0], 'B':[0,0,0]}
        line = f.readline()
        while len(line) > 1:
            #regex match the line
            words = line.split(" ")
            #deal with revealing cards
            if words[0] in ["Flop", "Turn", "River"]:
                result = re.match(REGEX_REVEAL, line)
                cards, amount, board = result.group(2, 3, 6)
                amount = int(amount)
                # Clear the pips
                pips['A'] = [0,0,0]
                pips['B'] = [0,0,0]
                # Assert we are computing the boards correctly
                if (amount != board_pots[int(board) - 1]):
                    print("Check failed!")
                    print("Line No. ", line_cnt)
                    print(amount, board_pots[int(board) - 1])
                    assert False
                streets[int(board) - 1] = cards.split(" ")
                print(streets)
            #deal with making bets
            else:
                #blind
                if words[1] == "posts":
                    result = re.match(REGEX_BLIND, line)
                    player, amount = result.group(1,2)
                    amount = int(amount)
                    for board in range(3):
                        pips[player][board] = amount
                        board_pots[board] += amount
                #raises
                if words[1] == "raises":
                    result = re.match(REGEX_RAISE, line)
                    player, amount, board = result.group(1, 2, 3)
                    board = int(board) - 1
                    amount = int(amount)
                    # The amount the player bets before the raise
                    prev_amount = pips[player][board]
                    raise_amount = amount - prev_amount
                    number_of_raise[player] += 1
                    total_of_raise[player] += raise_amount
                    # update the pot
                    pips[player][board] = amount
                    board_pots[board] += raise_amount
                #folds
                elif words[1] == "folds":
                    result = re.match(REGEX_FOLD, line)
                    player, board = result.group(1, 2)
                    board = int(board) - 1
                    number_of_folds[player] += 1
                #calls  
                elif words[1] == "calls":
                    result = re.match(REGEX_CALL, line)
                    player, board = result.group(1, 2)
                    board = int(board) - 1
                    opponent = 'B' if player == 'A' else 'A'
                    # The amount the player bets before the call
                    amount = pips[opponent][board]
                    prev_amount = pips[player][board]
                    call_amount = amount - prev_amount
                    # update the pot
                    pips[player][board] = amount
                    board_pots[board] += call_amount
                #bets
                elif words[1] == "bets":
                    result = re.match(REGEX_BET, line)
                    player, amount, board = result.group(1, 2, 3)
                    board = int(board) - 1
                    amount = int(amount)
                    pips[player][board] = amount
                    board_pots[board] += amount
                    number_of_raise[player] += 1
                    total_of_raise[player] += amount

                #endgame awards
                elif words[1] == "awarded":
                    result = re.match(REGEX_AWARD, line)
                    player, award = result.group(1, 2)
                    awards[player].append(int(award))

                else:
                    pass
            line_cnt += 1
            line = f.readline()
#print statistics
print("Number of raises:", number_of_raise)
print("Number of folds:", number_of_folds)
print("Total amount of raises:", total_of_raise)
for player in total_of_raise:
    print("Average raise of {}: {}".format(player, total_of_raise[player] / number_of_raise[player]))
#print("Awards:", awards)
#TODO: pre-flop raise
#TODO: raise in advantage
#TODO: raise in disadvantage
#TODO: successful intimidation
#etc...
                
                            
