package javabot.skeleton;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

public class CalcProb {
    private static final Map<String, Double> PROBABILITIES = Map.of();
    private static final List<String> Deck = 
            List.of("1s", "1c", "1d", "1h",
                    "2s", "2c", "2d", "2h",
                    "3s", "3c", "3d", "3h",
                    "4s", "4c", "4d", "4h",
                    "5s", "5c", "5d", "5h",
                    "6s", "6c", "6d", "6h",
                    "7s", "7c", "7d", "7h",
                    "8s", "8c", "8d", "8h",
                    "9s", "9c", "9d", "9h",
                    "Ts", "Tc", "Td", "Th",
                    "Js", "Jc", "Jd", "Jh",
                    "Qs", "Qc", "Qd", "Qh",
                    "Ks", "Kc", "Kd", "Kh");
    
    /**
     * @param card1 the first card.
     * @param card2 the second card.
     * @return the probability of winning with these two cards.
     */
    public static double rawProb(String card1, String card2) {
        char num1 = card1.charAt(0);
        char num2 = card2.charAt(0);
        char suit1 = card1.charAt(1);
        char suit2 = card2.charAt(1);
        if (num1 == num2) {
            String query = "" + suit1 + suit2;
            return PROBABILITIES.get(query);
        }
        else {
            String s1 = (suit1 == suit2)? "" + num1 + num2 + "s": "" + num1 + num2 + "u";
            String s2 = (suit1 == suit2)? "" + num2 + num1 + "s": "" + num2 + num1 + "u";
            if (PROBABILITIES.containsKey(s1)) {
                return PROBABILITIES.get(s1);
            }
            else {
                return PROBABILITIES.get(s2);
            }
        }
    }
    
    /**
     * @param cards Our hand. Consists of two cards
     * @param commonCards The cards that have been shown.
     * @param guessingOpponent Whether we are assuming the hidden cards are uniformly distributed. 
     * @return the probability that we win.
     */
    public static double calcProb(List<String> cards, List<String> commonCards, boolean guessingOpponent) {
        if (cards.size() == 0) {
            return rawProb(cards.get(0), cards.get(1));
        }
        else if (cards.size() == 5) {
            List<String> rest = new ArrayList<String>(List.copyOf(cards));
            for (String card: cards) {
                rest.remove(card);
            }
            for (String card: commonCards) {
                rest.remove(card);
            }
            int score = 0;
            for (int i = 0; i < rest.size(); i++) {
                for (int j = i + 1; j < rest.size(); j++) {
                    score += winOrLose(cards, commonCards, List.of(rest.get(i), rest.get(j)), List.of());
                }
            }
            return (double)(score) / (44 * 45);
        }
        else {
            List<String> rest = new ArrayList<String>(List.copyOf(cards));
            for (String card: cards) {
                rest.remove(card);
            }
            for (String card: commonCards) {
                rest.remove(card);
            }
            int score = 0;
            int iteration = 100;
            for (int i = 0; i < iteration; i++) {
                score += winOrLose(cards, commonCards, List.of(), List.of());
            }
            return (double)(score) / iteration;
        }
    }
    /**
     * 
     * @param ourHand Our hand. Consists of two cards.
     * @param currentCommon The cards in the street.
     * @param opponentHand The opponent's hand. Consists of two cards. Empty if unknown.
     * @param rest The cards elsewhere. Empty if unknown.
     * @return An integer, indicating if we won or not
     */
    public static int winOrLose(List<String> ourHand, List<String> currentCommon, List<String> opponentHand, List<String >rest) {
        List<String> ourCards = new ArrayList<String>(List.copyOf(ourHand));
        List<String> opponentCards = new ArrayList<String>(List.copyOf(opponentHand));
        if (opponentHand.size() == 0) {
            if (rest.size() == 0) {
                rest = new ArrayList<String>(Deck);
                for (String card: ourHand) {
                    rest.remove(card);
                }
                for (String card: opponentHand) {
                    rest.remove(card);
                }
                for (String card: currentCommon) {
                    rest.remove(card);
                }
            }
            Collections.shuffle(rest);
            int comm = 5 - currentCommon.size();
            int opp = 2 - opponentHand.size();
            List<String> community = new ArrayList<String>(List.copyOf(currentCommon));
            community.addAll(rest.subList(0, comm));
            opponentCards.addAll(rest.subList(comm, comm + opp));
            ourCards.addAll(community);
            opponentCards.addAll(community);
        }
        else {
            ourCards.addAll(currentCommon);
            opponentCards.addAll(currentCommon);
        }
        
        int ourHandValue = FakeEval7.handScore(ourCards);
        int oppHandValue = FakeEval7.handScore(opponentCards);
        
        if (ourHandValue > oppHandValue) {
            return 2;
        }
        else if (ourHandValue == oppHandValue) {
            return 1;
        }
        else {
            return 0;
        }
    }
}
