package javabot.skeleton;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class FakeEval7 {
	private static final String RANKS = "23456789TJQKA";
    private static Map<String, Integer> RTN = new HashMap<>();
    
	public FakeEval7() {
		for(int i=0;i<13;i++) {
			RTN.put(RANKS.substring(i, i+1), i+2);
		}
	}
	
	/**
	 * Calculate the rank of largest combination of the cards
	 * @param ours: our cards
	 * @param common: the common cards
	 * @return an integer, the largest possible score of my cards + common 5 cards
	 */
	public int score(List<String> ours, List<String> common) {
		return 0;
	}
	
	/**
	 * Calculate the rank of the cards
	 * @param cards: a set of 5 cards (represented by strings)
	 * @return an integer, the largest possible score of my cards + common 5 cards
	 */
	public int handScore(List<String> cards) {
		return 0;
	}
	
	/**
	 * Calculate if the cards can constitute a string.
	 * @param cards: a set of 5 cards (represented by strings)
	 * @return a boolean, indicates whether it is a straight
	 */
	public int isStraight(List<String> cards) {
		Map<Integer,Integer> card_dict=this.toMap(cards);
		Set<Integer> ranks=card_dict.keySet();
		int smallest=16;
		for (int i:ranks){
			if (i < smallest) smallest=i;
		}
	    if (smallest==2) {
	        for (int i=1;i<4;i++)
	            if (!ranks.contains(smallest+i)) return 0;
	        if (ranks.contains(6)) return 6;
	        else {if (ranks.contains(14)) return 5;
	        else return 0;}
	    } else {
	    	for (int i=1;i<5;i++) {if (!ranks.contains(smallest+i)) return 0;}
	        return smallest+4;
	    }
	}
	
	/**
	 * Calculate a map type for the string
	 * @param cards: a set of 5 cards (represented by strings)
	 * @return a map counting how many cards for a certain rank for it
	 * */ 
	private Map<Integer,Integer> toMap(List<String> cards) {
		Map<Integer,Integer> result=new HashMap<>();
		for (String card:cards){
			String rank=card.substring(0, 1);
			if(!result.keySet().contains(RTN.get(rank))){
				result.put(RTN.get(rank), 0);
			}
			result.put(RTN.get(rank), result.get(RTN.get(rank))+1);
		}
		return result;
	}
	
	/**
	 * Calculate if the cards can constitute a flush.
	 * @param cards: a set of 5 cards (represented by strings)
	 * @return a boolean, indicates whether it is a flush
	 */
	public boolean isFlush(List<String> cards) {
		String suit=null;
		for (String card:cards){
			if (suit==null) suit=card.substring(1);
			else {if (!suit.equals(card.substring(1))) return false;}
		}
		return true;
	}

}
