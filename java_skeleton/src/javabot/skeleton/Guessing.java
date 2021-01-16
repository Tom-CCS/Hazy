package javabot.skeleton;

import java.util.HashSet;
import java.util.Set;
import java.util.List;

public class Guessing {
	private Set<String> singles = new HashSet<>();
	// A set of SINGLE cards
	// The cards that can make a pair, 3 of a kind, straight, etc
	private Set<String> potentialSingles = new HashSet<>();
	// the cards that can 
	private Set<String> strongSingles = new HashSet<>();
	private String majorSuit;
	private String majorSuit2;
	private Set<String> doubles = new HashSet<>();
	private int state=3;
	
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
