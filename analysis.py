import matplotlib.pyplot as pl
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
    #Various stat trackers
    line = "start"
    line_cnt = 0
    number_of_raise = {'A':0,'B':0}
    total_of_raise = {'A':0,'B':0}
    bet_ratios = {'A':[],'B':[]}
    raise_ratios = {'A':[],'B':[]}
    number_of_folds = {'A':0,'B':0}
    preflop_folds = {'A':0, 'B':0}
    all_raises = {'A':[], 'B': []}
    awards = {'A': [], 'B': []}
    awards_diff = []
    #read until EOF
    while len(line) > 0:
        #read until the next blank line, which marks the end of the game
        #initialize board
        A_hands = []
        B_hands = []
        board_pots = [2, 4, 6] # the initial board inflation, blinds included
        round_raises = {'A':[[], [], []], 'B':[[], [], []]}
        streets = [[], [], []]
        preflop = True
        pips = {'A':[0,0,0], 'B':[0,0,0]}
        line = f.readline()
        while len(line) > 1:
            #regex match the line
            words = line.split(" ")
            #deal with revealing cards
            if words[0] in ["Flop", "Turn", "River"]:
                preflop = False
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
                    # First discount the cont_cost
                    opponent = 'B' if player == 'A' else 'A'
                    cont_cost = max(pips[opponent][board] - pips[player][board], 0)
                    # The amount the player bets before the raise
                    prev_amount = pips[player][board]
                    raise_amount = amount - prev_amount
                    number_of_raise[player] += 1
                    total_of_raise[player] += raise_amount
                    raise_ratios[player].append((raise_amount - cont_cost)/ (board_pots[board] + cont_cost))
                    # update the pot
                    pips[player][board] = amount
                    board_pots[board] += raise_amount
                #folds
                elif words[1] == "folds":
                    result = re.match(REGEX_FOLD, line)
                    player, board = result.group(1, 2)
                    board = int(board) - 1
                    number_of_folds[player] += 1
                    if preflop:
                        preflop_folds[player] += 1
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
                    # The amount the player bets before the raise
                    bet_ratios[player].append(amount / board_pots[board])

                #endgame awards
                elif words[1] == "awarded":
                    result = re.match(REGEX_AWARD, line)
                    player, award = result.group(1, 2)
                    awards[player].append(int(award))

                else:
                    pass
            line_cnt += 1
            line = f.readline()
#print general statistics
print("Number of raises:", number_of_raise)
print("Number of folds:", number_of_folds)
print("Total amount of raises:", total_of_raise)
pl.hist(raise_ratios['A'], bins = 40, label="A")
pl.hist(raise_ratios['B'], bins = 40, label="B")
pl.legend()
pl.savefig("raise_ratio.png")
pl.clf()
pl.hist(bet_ratios['A'], bins = 40, label="A")
pl.hist(bet_ratios['B'], bins = 40, label="B")
pl.legend()
pl.savefig("bet_ratio.png")
awards_diff = [sum(awards["A"][:i]) - sum(awards["B"][:i]) for i in range(len(awards["A"]))]
pl.clf()
pl.plot(awards_diff)
pl.savefig("awards_over_time.png")
pl.clf()
#print specialize statistics
print("Number of preflop folds:", preflop_folds)
for player in total_of_raise:
    print("Average raise of {}: {}".format(player, total_of_raise[player] / number_of_raise[player]))
#print pre-flop statistics
#print("Awards:", awards)
#TODO: pre-flop raise
#TODO: raise in advantage
#TODO: raise in disadvantage
#TODO: successful intimidation
#etc...
                
                            
