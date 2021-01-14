package javabot.skeleton;


public class BehaviourStudy {
    // Heuristics related to opponent's behaviour
    private static double ALL_IN_RATIO = 0.5;
    /**
     * 
     * @param largeRaiseCount
     *      the number of raises over LARGE_RAISE_THRESHOLD the opponent made.
            LARGE_RAISE_THRESHOLD is defined in player.py
     * @param roundCount  the number of rounds played.
     * @return
     */
    public static boolean isAllIn(int largeRaiseCount, int roundCount) {
        return largeRaiseCount > ALL_IN_RATIO * roundCount;
    }
}
