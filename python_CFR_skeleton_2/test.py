from probability import calc_prob
from algo_for_next_step import algorithm
import eval7

def test_calc_prob():
    #Testcases:
    As,Ad,Ac,Ah=eval7.Card("As"),eval7.Card("Ad"),eval7.Card("Ac"),eval7.Card("Ah")
    Ks,Kd,Kc,Kh=eval7.Card("Ks"),eval7.Card("Kd"),eval7.Card("Kc"),eval7.Card("Kh")
    Qs,Qd,Qc,Qh=eval7.Card("Qs"),eval7.Card("Qd"),eval7.Card("Qc"),eval7.Card("Qh")
    Js,Jd,Jc,Jh=eval7.Card("Js"),eval7.Card("Jd"),eval7.Card("Jc"),eval7.Card("Jh")
    Ts,Td,Tc,Th=eval7.Card("Ts"),eval7.Card("Td"),eval7.Card("Tc"),eval7.Card("Th")
    assert calc_prob([As,Ah],[])==0.8521635
    assert calc_prob([As,Ah],[Ac,Kh,Ks,Kd,Qc])==43/45
    # lose iff opp has Kc
    assert calc_prob([As,Ah],[Ac,Kh,Ks,Qd,Qc])==1-4/(44*45)
    # lose iff opp has Kc, Kd or Qs, Qh
    assert calc_prob([Kc,Kd],[Kh,Qh,Th,Ks,Qs])==1-4/(44*45)
    # lose iff As, Js or 9s, Js
    assert calc_prob([Kc,Kd],[Kh,Td,Tc,Ks])==1
    # Never lose
    assert calc_prob([Kc,Kd],[Kh,Ts,Tc,Ks])==1-12/(44*45*46)
    # lose iff the remaining and the opponent are Js, Qs, As/9s 
    assert calc_prob([Kc,Kd],[Kh,Jd,Ks])>0.998
    # There is a four of a kind, almost never lose
    assert calc_prob([Kc,Kd],[Kh,Td,Ts])>0.99
    # There is a large full house, really high prob to win
    assert calc_prob([Jc,Kd],[Kh,Jd,Js])>0.95
    # There is a small full house, very high prob to win
    assert calc_prob([Ac,Kd],[Qh,Jd,Ts])>0.93
    # There is a straight, very high prob to win
    assert calc_prob([Ac,Td],[Th,Jd,Ts])>0.9
    # There is a three of a kind, high prob to win
    assert calc_prob([Jc,Kd],[Kh,Td,Js])>0.8
    # There is a large two pairs, high prob to win


def test_action():
    action = algorithm()
    #small probability to win and large cost, fold
    assert action(0, 4, 1, 2, [1, 2]) == -1
    assert action(0.2, 4, 1, 2, [1, 2]) == -1
    #small probability to win but small cost, check/call
    assert action(0.2, 1000, 499, 2, [1, 2]) == 0
    #positive expectation but large cost, check/call
    assert action(0.4, 10, 3, 4, [3, 10]) == 0
    #positive expectation and positive cost, might attempt a valid raise
    cnt = 0
    for _ in range(100):
        act = action(0.7, 10, 3, 4, [3, 10])
        assert (act == 0) or (act >= 3 and act <= 10)
        if (act > 0):
            cnt += 1
    #this has a small probability of failing
    assert cnt > 0
    #positive gain but the opponent is intimidating, check/call
    action(0.7, 100, 3, 94, [94, 100])
    assert action(0.7, 100, 3, 94, [94, 100]) == 0
    
    

test_calc_prob()
print("calc_prob tests passed.")
test_action()
print("action tests passed.")
