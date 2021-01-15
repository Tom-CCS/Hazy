package javabot.skeleton;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class AllocateCards {
    // Parameters
    private static final int NUM_BOARD = 3;
    private static final double PLAY_HIGH_THRES = 0.6;
    private static final double PLAY_MID_THRES = 0.6;
      
    /**
     * @param myCards the cards in our hand.
     * @return the allocation of our cards on the three tables
     *         the size of the 4th list indicate the highest table we should keep
     */
    public static List<List<String>> allocate(List<String> myCards) {
        double maxProb = 0;
        List<String> best = List.of();
        // Search for best pair
        for (int i = 0; i < myCards.size(); i++) {
            for (int j = i + 1; j < myCards.size(); j++) {
                double prob = CalcProb.rawProb(myCards.get(i), myCards.get(j));
                if (prob > maxProb) {
                    maxProb = prob;
                    best = List.of(myCards.get(i), myCards.get(j));
                }
            }
        }
        
        List<String> rest = new ArrayList(Collections.unmodifiableList(myCards));
        rest.removeAll(best);
        
        double secondMaxProb = 0;
        List<String> secondBest = List.of();
        // Search for second best pair
        for (int i = 0; i < rest.size(); i++) {
            for (int j = i + 1; j < rest.size(); j++) {
                double prob = CalcProb.rawProb(rest.get(i), rest.get(j));
                if (prob > secondMaxProb) {
                    secondMaxProb = prob;
                    secondBest = List.of(rest.get(i), rest.get(j));
                }
            }
        }
        // Extract the worst pair
        List<String> worst = new ArrayList(Collections.unmodifiableList(rest));
        worst.removeAll(secondBest);
        worst = List.of(worst.get(0), worst.get(1));
        
        // Return the allocation
        if (maxProb > PLAY_HIGH_THRES) {
            return List.of(worst, secondBest, best, List.of("a", "a"));
        }
        else if (maxProb > PLAY_MID_THRES) {
            return List.of(secondBest, best, worst, List.of("a"));
        }
        else {
            return List.of(best, worst, secondBest, List.of());
        }
        
    }
    
}
