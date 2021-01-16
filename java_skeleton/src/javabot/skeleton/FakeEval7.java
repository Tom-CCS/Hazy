package javabot.skeleton;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class FakeEval7 {
	private static final String RANKS = "23456789TJQKA";
    private static Map<String, Integer> RTN = new HashMap<>();
    
	static {
		for(int i=0;i<13;i++) {
			RTN.put(RANKS.substring(i, i+1), i+2);
		}
	}
	
	/**
	 * Calculate the rank of the cards
	 * @param ours: our cards (2 strings)
	 * @param common: the common cards (3~5 strings)
	 * @return an integer, indicate the largest possible type of my cards + common 5 cards
	 */
	public static int type(List<String> ours, List<String> common){
		int max=0;
		int n=common.size();
		List<String> ls=new ArrayList<>(ours);
		ls.addAll(common);
		int score;
		for (int i=0;i<n-2;i++) {
			for (int j=i+1;j<n-1;j++) {
				for (int k=j+1;k<n;k++) {
					for (int l=k+1;l<n+1;l++) {
						for (int m=l+1;m<n+2;m++) {
							score = handType(List.of(ls.get(i),ls.get(j),ls.get(k),ls.get(l),ls.get(m)));
							max = score>max? score : max;
						}
					}
				}
			}
		}
		return max;
	}
	
	/**
	 * Calculate the rank of the cards
	 * @param ours: our cards (2 strings)
	 * @param common: the common cards (3~5 strings)
	 * @return an integer, the largest possible score of my cards + common 5 cards
	 */
	public static int score(List<String> ours, List<String> common){
		int max=0;
		int n=common.size();
		List<String> ls=new ArrayList<>(ours);
		ls.addAll(common);
		int score;
		for (int i=0;i<n-2;i++) {
			for (int j=i+1;j<n-1;j++) {
				for (int k=j+1;k<n;k++) {
					for (int l=k+1;l<n+1;l++) {
						for (int m=l+1;m<n+2;m++) {
							score = handScore(List.of(ls.get(i),ls.get(j),ls.get(k),ls.get(l),ls.get(m)));
							max = score>max? score : max;
						}
					}
				}
			}
		}
		return max;
	}
	
	/**
	 * Calculate the type of largest combination of the cards
	 * @param cards: a set of 5 cards (represented by strings)
	 * @return an integer, the largest possible score of my cards + common 5 cards
	 * The score is defined by:
	 * 10 classes of cards: 
     * royal_flush/straight_flush=9; four_of_a_kind=8; full_house=7;
     * flush=6; straight=5; three_of_a_kind=4; two_pairs=3; one_pair=2;
     * high_card=1
	 * class<<20 + 1st kicker (if any)<<16+ 2nd kicker (if any)<<12 + ... +5th kicker (is any) <<0
	 */
	public static int handType(List<String> cards) {
	    Map<Integer, Integer> cardDict=toMap(cards);
	    Set<Integer> ranks=cardDict.keySet();
	    int straightIndicator=isStraight(cards);
	    int mag;
	    if(isFlush(cards)) {
	        if (straightIndicator>0) {
	            return 9;
	            // A royal flush or A straight flush
	        } else { // a flush
	            return 6;
	        }
	    } else {
	        if (straightIndicator>0) return 5;// a straight
	        else {
	        	Collection<Integer> values=cardDict.values();
	            if(values.contains(4)) {return 8;
	            } else if (values.contains(3)) {// 3 of a kind or full house
	                if (values.contains(2)){return 7; //Full House
	                } else { return 4;// Three of a kind 
	                }
	            } else if (values.contains(2)) {// One pair or two pairs:
	            	int pairNum=0;
	            	for(int k:ranks) {
	                    if (cardDict.get(k)==2) pairNum+=1;}
	                return pairNum+1;
	            } else {
	                return 1;
	            }
	        }
	    }
	}
	
	/**
	 * Calculate the rank of largest combination of the cards
	 * @param cards: a set of 5 cards (represented by strings)
	 * @return an integer, the largest possible score of my cards + common 5 cards
	 * The score is defined by:
	 * 10 classes of cards: 
     * royal_flush=10; straight_flush=9; four_of_a_kind=8; full_house=7;
     * flush=6; straight=5; three_of_a_kind=4; two_pairs=3; one_pair=2;
     * high_card=1
	 * class<<20 + 1st kicker (if any)<<16+ 2nd kicker (if any)<<12 + ... +5th kicker (is any) <<0
	 */
	public static int handScore(List<String> cards) {
		int classify=1<<20;
		int[] kickers=new int[5];
		for (int i=0;i<5;i++) kickers[i]=1<<(16-4*i);
	    Map<Integer, Integer> cardDict=toMap(cards);
	    Set<Integer> ranks=cardDict.keySet();
	    int straightIndicator=isStraight(cards);
	    int mag;
	    if(isFlush(cards)) {
	        if (straightIndicator>0) {
	            if (Set.copyOf(cards).equals(Set.of("As","Ks","Qs","Js","Ts"))) return 10*classify;
	            // A royal flush
	            else return straightIndicator*kickers[0]+9*classify;
	            // A straight flush
	        } else { // a flush
	            mag=6*classify;
	            for(int i=0;i<5;i++){
	                int max=Collections.max(ranks);
	                ranks.remove(max);
	                mag=mag+max*kickers[i];
	            }
	            return mag;
	        }
	    } else {
	        if (straightIndicator>0) return straightIndicator*kickers[0]+5*classify;
	        // a straight
	        else {
	        	Collection<Integer> values=cardDict.values();
	            if(values.contains(4)) { // Four of a kind
	                mag=8*classify;
	                for(int k:ranks) {
	                    if (cardDict.get(k)==4) mag+=kickers[0]*k;
	                    else mag+=kickers[1]*k;}
	                return mag;
	            } else if (values.contains(3)) {// 3 of a kind or full house
	                if (values.contains(2)){// full house
	                    mag=7*classify;
                		for(int k:ranks) {
    	                    if (cardDict.get(k)==3) mag+=kickers[0]*k;
    	                    else mag+=kickers[1]*k;}
    	                return mag;
	                } else { // Three of a kind
	                    mag=4*classify;
	                    Set<Integer> singles=new HashSet<>();
	                    int cur=0;
	                    for(int k:ranks) {
    	                    if (cardDict.get(k)==3) mag+=kickers[0]*k;
    	                    else singles.add(k);}
    	                return mag+kickers[1]*Collections.max(singles)+kickers[2]*Collections.min(singles);
	                }
	            } else if (values.contains(2)) {// One pair or two pairs:
	            	Set<Integer> pairs=new HashSet<>();
	            	List<Integer> singles=new ArrayList<>();
	                for(int k:ranks) {
	                    if (cardDict.get(k)==2) pairs.add(k);
	                    else singles.add(k);}
	                if (pairs.size()==2) return 3*classify+Collections.max(pairs)*kickers[0]+Collections.min(pairs)*kickers[1]+Collections.max(singles)*kickers[2];
	                // two pairs
	                else {//one pair
	                	mag = 2*classify+Collections.max(pairs)*kickers[0];
	                	Collections.sort(singles);
	                	for(int i=0;i<3;i++) {
	                		mag+=singles.get(i)*kickers[3-i];
	                	}
	                	return mag;
	                }
	            } else {
	                mag=classify;
	                int max;
	        		for(int i=0;i<5;i++){
		                max=Collections.max(ranks);
		                ranks.remove(max);
		                mag=mag+max*kickers[i];
		            }
		            return mag;
	            }
	        }
	    }
	}

	
	/**
	 * Calculate if the cards can constitute a string.
	 * @param cards: a set of 5 cards (represented by strings)
	 * @return a boolean, indicates whether it is a straight
	 */
	public static int isStraight(List<String> cards) {
		Map<Integer,Integer> card_dict = toMap(cards);
		Set<Integer> ranks=card_dict.keySet();
		int smallest=Collections.min(ranks);
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
	private static Map<Integer,Integer> toMap(List<String> cards) {
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
	public static boolean isFlush(List<String> cards) {
		String suit=null;
		for (String card:cards){
			if (suit==null) suit=card.substring(1);
			else {if (!suit.equals(card.substring(1))) return false;}
		}
		return true;
	}

}
