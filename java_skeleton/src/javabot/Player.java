package javabot;

import javabot.skeleton.*;

import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Arrays;
import java.util.Collections;
import java.util.ArrayList;
import java.util.Set;
import java.lang.Integer;
import java.lang.String;

/**
 * A pokerbot.
 */
public class Player implements Bot {
    // Playing three boards
    private static final int numBoard = 3;
    // Total number of rounds
    private static final int numRounds = 500;
    // Custom stuff
    private static final int LARGE_RAISE_THRESHOLD = 100;
    private static final int numAlg = 3;
    // Here are the algorithm parameters
    // The first field in RAISE_THRES and the 
    private static final Map<String, Double> algoTIMID = 
            Map.of("RAISE_THRES", 0.7, "RAISE_RATIO", 0.4);
    private static final Map<String, Double> algoNORMAL = 
            Map.of("RAISE_THRES", 0.5, "RAISE_RATIO", 0.4);
    private static final Map<String, Double> algoAGGRESSIVE = 
            Map.of("RAISE_THRES", 0.5, "RAISE_RATIO", 0.6);
    private static final List<Map<String, Double>> algorithms = 
            List.of(algoTIMID, algoNORMAL, algoAGGRESSIVE);
    // Card Allocation
    private List<List<String>> boardAllocations; 
    // Whether we are playing each board
    private boolean[] playing = new boolean[numBoard];
    // Counters
    private int largeRaiseCount;
    private int roundCount;
    private int algoIndex;
    private Map<String, Double> algo;
    private List<Double> algoProb = 
            new ArrayList(List.of(0.3, 0.3, 0.4));
    private List<Integer> algoGain = 
            new ArrayList(List.of(0, 0, 0));
    
    // The random number generator
    private Random random = new Random();
    /**
     * Called when a new game starts. Called exactly once.
     */
    public Player() {
    }
    
    /**
     * Allocate the cards to the tables
     * @param cards the cards we have
     */
    private void allocateCards(List<String> cards) {
        this.boardAllocations = new ArrayList<>();
        List<List<String>> allocation = AllocateCards.allocate(cards);
        //System.out.println(allocation);
        int highestPlaying = allocation.get(numBoard).size();
        for (int i = 0; i < numBoard; i++) {
            this.boardAllocations.add(allocation.get(i));
            if (i <= highestPlaying) {
                this.playing[i] = true;
            }
            else {
                this.playing[i] = false;
            }
        }
    }
    
    /**
     * Called for each round. Choose the algorithm parameter for this round.
     */
    private void chooseAlgo() {
        double seed = random.nextDouble();
        int i = 0;
        double sum = 0;
        while (true) {
            sum += this.algoProb.get(i);
            if (seed < sum) break;
            i += 1;
        }
        this.algoIndex = i;
        this.algo = algorithms.get(i);
    }
    /**
     * Called when a new round starts. Called State.NUM_ROUNDS times.
     *
     * @param gameState The GameState object.
     * @param roundState The RoundState object.
     * @param active Your player's index.
     */
    public void handleNewRound(GameState gameState, RoundState roundState, int active) {
        int myBankroll = gameState.bankroll;  // the total number of chips you've gained or lost from the beginning of the game to the start of this round
        int oppBankroll = gameState.oppBankroll; // ^ but for your opponent
        float gameClock = gameState.gameClock;  // the total number of seconds your bot has left to play this game
        int roundNum = gameState.roundNum;  // the round number from 1 to State.NUM_ROUNDS
        List<String> myCards = roundState.hands.get(active);  // your six cards at the start of the round
        boolean bigBlind = (active == 1);  // true if you are the big blind
        
        chooseAlgo(); // choose the algorithm this round
        allocateCards(myCards); // allocation strategy
        this.roundCount += 1;
    }

    /**
     * Called when a round ends. Called State.NUM_ROUNDS times.
     *
     * @param gameState The GameState object.
     * @param terminalState The TerminalState object.
     * @param active Your player's index.
     */
    public void handleRoundOver(GameState gameState, TerminalState terminalState, int active) {
        int myDelta = terminalState.deltas.get(active);  // your bankroll change from this round
        int oppDelta = terminalState.deltas.get(1-active);  // your opponent's bankroll change from this round
        RoundState previousState = (RoundState)(terminalState.previousState);  // RoundState before payoffs
        int street = previousState.street;  // 0, 3, 4, or 5 representing when this round ended
        double gameClock = gameState.gameClock;
        if (this.roundCount % 100 == 0) {
            System.out.println(gameClock);
        }
        // update the gains of each algorithm
        int grossGain = this.algoGain.get(this.algoIndex) + (myDelta - oppDelta);
        this.algoGain.set(this.algoIndex, grossGain);
        // update the preference for each algorithm
        if (this.roundCount == 150) {
            double sum = 0;
            for (int i = 0; i < numAlg; i++) {
                double newProb = this.algoProb.get(i) + 0.0005 * this.algoGain.get(i);
                if (newProb < 0) newProb = 0;
                sum += newProb;
                this.algoProb.set(i, newProb);
            }
            // Normalization
            if (sum > 0) {
                for (int i = 0; i < numAlg; i++) {
                    double newProb = this.algoProb.get(i);
                    newProb /= sum;
                    this.algoProb.set(i, newProb);
                }
            }
            else {
                // We are losing, attempt most aggressive style
                this.algoProb = List.of(0.2, 0.2, 0.6);
            }
            System.out.println(this.algoProb);
        }
        //List<List<String>> myCards = new ArrayList<List<String>>();
        //List<List<String>> oppCards = new ArrayList<List<String>>();
        //for (State terminalBoardState : previousState.boardStates) {
        //    BoardState previousBoardState = (BoardState)(((TerminalState)terminalBoardState).previousState);
        //    myCards.add(previousBoardState.hands.get(active)); // your cards
        //    oppCards.add(previousBoardState.hands.get(1-active)); // opponent's cards or "" if not revealed
        //}
    }

    /**
     * Where the magic happens - your code should implement this function.
     * Called any time the engine needs a triplet of actions from your bot.
     *
     * @param gameState The GameState object.
     * @param roundState The RoundState object.
     * @param active Your player's index.
     * @return Your action.
     */
    public List<Action> getActions(GameState gameState, RoundState roundState, int active) {
        List<Set<ActionType>> legalActions = roundState.legalActions();  // the actions you are allowed to take
        int street = roundState.street;  // 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        List<String> myCards = roundState.hands.get(active);  // your cards across all boards
        List<List<String>> boardCards = new ArrayList<List<String>>(); // the board cards
        int[] myPips = new int[State.NUM_BOARDS];  // the number of chips you have contributed to the pot on each board this round of betting
        int[] oppPips = new int[State.NUM_BOARDS];  // the number of chips your opponent has contributed to the pot on each board this round of betting
        int[] continueCost = new int[State.NUM_BOARDS];  // the number of chips needed to stay in each pot
        int myStack = roundState.stacks.get(active);  // the number of chips you have remaining
        int oppStack = roundState.stacks.get(1-active);  // the number of chips your opponent has remaining
        int netUpperRaiseBound = roundState.raiseBounds().get(1);  // the maximum value you can raise across all 3 boards
        int netCost = 0;  // to keep track of the net additional amount you are spending across boards this round 
        int totalContCost = 0;
        // Compute some things that need iteration
        for (int i = 0; i < State.NUM_BOARDS; i++) {
            if (roundState.boardStates.get(i) instanceof BoardState) {  // if a board is still active (no one folded)
                 BoardState boardState = (BoardState)roundState.boardStates.get(i);
                 myPips[i] = boardState.pips.get(active);
                 oppPips[i] = boardState.pips.get(1-active);
                 // Trim away all the unrevealed cards
                 List<String> untrimmedCards = boardState.deck;
                 List<String> trimmedCards = new ArrayList<>();
                 for (String s: untrimmedCards) {
                    if (s.length() > 0) {
                        trimmedCards.add(s);
                    }
                 }
                 boardCards.add(Collections.unmodifiableList(trimmedCards));
            } else {  // someone already folded on this board
                 TerminalState terminalBoardState = (TerminalState)roundState.boardStates.get(i);
                 myPips[i] = 0;
                 oppPips[i] = 0;
                 boardCards.add(((BoardState)terminalBoardState.previousState).deck);
            }
            continueCost[i] = oppPips[i] - myPips[i];
            totalContCost += continueCost[i];
        }
        int totalRaiseReserve = myStack - totalContCost;
        
        List<Action> myActions = new ArrayList<Action>();
        
        for (int i = 0; i < State.NUM_BOARDS; i++) {
            // Study Opponent Behaviour
            if (continueCost[i] > LARGE_RAISE_THRESHOLD) {
                this.largeRaiseCount += 1;
            }
            
            // Decide Own Action
            Set<ActionType> legalBoardActions = legalActions.get(i);
            if (legalBoardActions.contains(ActionType.ASSIGN_ACTION_TYPE)) { 
                // default assignment of hands to boards
                myActions.add(new Action(ActionType.ASSIGN_ACTION_TYPE, this.boardAllocations.get(i)));
            }
            else if (roundState.boardStates.get(i) instanceof TerminalState) { 
                // The board has Terminated
                myActions.add(new Action(ActionType.CHECK_ACTION_TYPE));
            } else if (!this.playing[i]) {
                // We are giving up the board
                if (legalBoardActions.contains(ActionType.FOLD_ACTION_TYPE)) {
                    myActions.add(new Action(ActionType.FOLD_ACTION_TYPE));
                    totalRaiseReserve += continueCost[i];
                }
                else {
                    myActions.add(new Action(ActionType.CHECK_ACTION_TYPE));
                }
            }
            else {
                // We are actually playing
                // Extract some info
                int boardContCost = continueCost[i];
                BoardState boardState = (BoardState)(roundState.boardStates.get(i));
                int boardTotal = boardState.pot;
                int potTotal = myPips[i] + oppPips[i] + boardTotal;
                int minRaise = boardState.raiseBounds(active, roundState.stacks).get(0);
                int maxRaise = boardState.raiseBounds(active, roundState.stacks).get(1); 
                
                List<String> streetCard = boardCards.get(i);
                // Calculate unbiased probability
                double winProb = CalcProb.calcProb(this.boardAllocations.get(i), streetCard, false);
                // Choose Algorithm
                Algo chosenAlgo;
                if (BehaviourStudy.isAllIn(this.largeRaiseCount, this.roundCount)) {
                    chosenAlgo = new AntiAllInAlgo();
                }
                else {
                    chosenAlgo = new Algo(this.algo.get("RAISE_THRES"), this.algo.get("RAISE_RATIO"));
                }
                int raiseAmount = chosenAlgo.algorithm(winProb, potTotal, myPips[i], 
                        boardContCost, List.of(minRaise, Math.min(maxRaise, totalRaiseReserve)));
                // Return Action
                if (legalBoardActions.contains(ActionType.RAISE_ACTION_TYPE) && raiseAmount > 0) {
                    myActions.add(new Action(ActionType.RAISE_ACTION_TYPE, raiseAmount));
                    totalRaiseReserve -= raiseAmount;
                }
                else if (legalBoardActions.contains(ActionType.CALL_ACTION_TYPE) && raiseAmount >= 0) {
                    myActions.add(new Action(ActionType.CALL_ACTION_TYPE, raiseAmount));
                }
                else if (legalBoardActions.contains(ActionType.CHECK_ACTION_TYPE) && raiseAmount >= 0) {
                    myActions.add(new Action(ActionType.CHECK_ACTION_TYPE, raiseAmount));
                }
                else {
                    myActions.add(new Action(ActionType.FOLD_ACTION_TYPE, raiseAmount));
                    totalRaiseReserve += boardContCost;
                }
            }
        }
        return myActions;
    }

    /**
     * Main program for running a Java pokerbot.
     */
    public static void main(String[] args) {
        Player player = new Player();
        Runner runner = new Runner();
        runner.parseArgs(args);
        runner.runBot(player);
    }
}