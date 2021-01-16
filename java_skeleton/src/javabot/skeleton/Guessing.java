package javabot.skeleton;

import java.util.HashSet;
import java.util.Set;
import java.util.List;

public class Guessing {
	private Set<String> singles = new HashSet<>();
	// A set of SINGLE cards
	// The cards that can make a good hand, such as pairs
	// The cards here ONLY CONTAIN THE NUMBER OF THE CARD
	private Set<String> potentialSingles = new HashSet<>();
	// the cards that can potential make a really good hand, such that make a straight
	// but less than 1.
	// It should be EMPTY if state=5
	private Set<String> strongSingles = new HashSet<>();
	// It is applicable to be in state=3,4
	// It contains the cards (WITH SUIT) that forms a really good hand 
	// such as >=3 of a kind 
	// excluded the cards in singles
	private String majorSuit;
	// It is defined as the most likely suit to have a flush.
	// 3, 4: suit of two
	// 5: suit of three of the same suit
	private String majorSuit2;
	// If there are four cards on 
	private Set<String> doubles = new HashSet<>();
	// The pairs of cards that can potentially make a good hand.
	// DOES NOT include cases above.
	private List<String> common;
	// The common cards on the board
	private int state=3;
	// The state for the board.
	
	/**
	 * Initial three cards on the board
	 * @param three: First three cards for guessing.
	 * Update the class.
	 */
	public Guessing(List<String> three) {
		//Initializing
		initialGuess();
	}
	
	public void initialGuess() {}
	
	/**
	 * @param fourth: the fourth card
	 * update the class
	 */
	public void update3To4(String fourth) {}
	
	/**
	 * @param fifth: the last card
	 * update the class
	 */
	public void update4To5(String fifth) {}
	
	/**
	 * Update the class
	 * @param action: a string indicates the opponent's action.
	 * It is either a positive number (raise, the amount of)
	 * Or 0 (ckeck/call)
	 * Or -1 (fold)
	 */
	public void takeAction(int action) {}
	
	/**
	 * Given the conditions, output the guessing for the 
	 * @return a SET of cards for guessing.
	 * (THE FORMAT MAY CHANGE)
	 */
	public Set<String> outputGuessing (){
		return null;
	}
}
