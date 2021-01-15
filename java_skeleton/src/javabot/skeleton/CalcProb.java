package javabot.skeleton;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class CalcProb {
    private static Map<String,Double> PROBABILITIES = new HashMap<>();
	static{
		JSONParser jsonParser = new JSONParser();
		try (FileReader reader = new FileReader("src/javabot/skeleton/rawProb.json")) {
	        // Read JSON file
	        Object obj = jsonParser.parse(reader);
	
	        JSONObject ProbJson = (JSONObject) obj;
	        
	        @SuppressWarnings("unchecked")
			Iterator<String> it =ProbJson.keySet().iterator();
	        while (it.hasNext()) {
	        	String combo = it.next();
	        	PROBABILITIES.put(combo, (Double)ProbJson.get(combo));
	        }
	    } catch (FileNotFoundException e) {
	        e.printStackTrace();
	    } catch (IOException e) {
	        e.printStackTrace();
	    } catch (ParseException e) {
	        e.printStackTrace();
	    }
	}
	
    private static final List<String> Deck = 
            List.of("As", "Ac", "Ad", "Ah",
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
            String query = ""+ num1 + num1;
            return PROBABILITIES.get(query);
        }
        else {
            String s1 = (suit1 == suit2)? "" + num1 + num2 + "s": "" + num1 + num2 + "u";
            String s2 = (suit1 == suit2)? "" + num2 + num1 + "s": "" + num2 + num1 + "u";
            if (PROBABILITIES.containsKey(s1)) {
                return PROBABILITIES.get(s1);
            } else {
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
        if (commonCards.size() == 0) {
            return rawProb(cards.get(0), cards.get(1));
        } else {
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
            return (double)(score) / (2*iteration);
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
        List<String> opponentCards;
        List<String> community;
        if (opponentHand.size() == 0) {
        	opponentCards = new ArrayList<String>();
            if (rest.size() == 0) {
                rest = new ArrayList<String>(Deck);
                List<String> seen=new ArrayList<>(ourHand);
                seen.addAll(currentCommon);
                for (String card: seen) {
                	rest.remove(card);
                }
            }
            Collections.shuffle(rest);
            int comm = 5 - currentCommon.size();
            int opp = 2 - opponentHand.size();
            community = new ArrayList<String>(currentCommon);
            community.addAll(rest.subList(0, comm));
            opponentCards=rest.subList(comm, comm + opp);
        } else {
        	opponentCards = opponentHand;
        	community=currentCommon;
        }
        int ourHandValue = FakeEval7.score(ourHand,community);
        int oppHandValue = FakeEval7.score(opponentCards,community);
        
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
