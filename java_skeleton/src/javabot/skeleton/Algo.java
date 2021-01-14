package javabot.skeleton;

import java.util.List;
import java.util.Random;

public class Algo {
    
    /*
     * Parameters:
        INTIMIDATE_PROB: a float in [0,1]. Set to 1.0.
            the "probability" that the opponent has a good hand when a large raise is made
        INTIMIATE_DEC: a float in [0,1]. Set to 0.7
            the decrease in win probability we should factor in when the opponent is intimidating

        RAISE_THRES: a float in [0,1]. Set to 0.
            how large win_prob must be to consider a raise.
        RAISE_RATIO: a float in [0,1]
            how large we should raise. Set to 0.4
            The formula for raising is my_pips + cont_cost + RAISE_RATIO * (current_pot + cont_cost)
     */
    private double INTIMIDATE_PROB = 1.0;
    private double INTIMIDATE_DEC = 0.5;
    private double RAISE_THRES = 0.5;
    private double RAISE_RATIO = 0.4;
    
    /**
     * Use Default parameters.
     */
    public Algo() {}
    
    /**
     * customize parameters
     * @param RAISE_THRES
     * @param RAISE_RATIO
     */
    public Algo(double RAISE_THRES, double RAISE_RATIO) {
        this.RAISE_RATIO = RAISE_RATIO;
        this.RAISE_THRES = RAISE_THRES;
    }
    
    /**
     * @param raise the ratio the opponent raised
     * @return how much we should lower our expected raise ratio
     */
    private double intimidateDec(double raise) {
        return Math.pow(2, -INTIMIDATE_DEC * raise);
    }
          
    /**
     * 
     * @param winProb The probability of winning.
     * @param currentPot The current money in the pot.
     * @param myPot The current money in my pot
     * @param continueCost The cost for continuing the game.
     * @param raiseRange The minimum/maximum amount that we are allowed to raise
     * @return an integer n, such that:
            n=-1 if fold
            n=0 if check (or call)
            n>0 for raise the money with n.
     */
    public int algorithm(double winProb, int currentPot, int myPot, int continueCost, List<Integer> raiseRange) {
        double intimidateRatio = (double)(continueCost) / (currentPot - continueCost);
        winProb *= intimidateDec(intimidateRatio);
        int minRaise = raiseRange.get(0);
        int maxRaise = raiseRange.get(1);
        
        boolean raiseAllowed;
        double raiseAmount;
        if (minRaise > maxRaise) {
            raiseAllowed = false;
            raiseAmount = 0;
        }
        else {
            raiseAllowed = true;
            raiseAmount = myPot + continueCost + RAISE_RATIO * (currentPot + continueCost) * 0.4;
            if (winProb > 0.7) {
                raiseAmount += RAISE_RATIO * (currentPot + continueCost) * 0.75;
            }
            raiseAmount = Math.max(raiseAmount, minRaise);
            raiseAmount = Math.min(raiseAmount, maxRaise);
        }
        
        Random random = new Random();
        if (continueCost > 0) {
            double potOdds = (double)(continueCost) / (currentPot + continueCost);
            if (potOdds > winProb) {
                return -1;
            }
            else {
                if (raiseAllowed && winProb > RAISE_THRES && random.nextDouble() < winProb) {
                    return (int)(raiseAmount);
                }
                else {
                    return 0;
                }
            }
        }
        else {
            if (raiseAllowed && winProb > RAISE_THRES && random.nextDouble() < winProb) {
                return (int)(raiseAmount);
            }
            else {
                return 0;
            }
        }
    }
}
