package javabot.skeleton;

import java.util.HashSet;
import java.util.Set;
import java.util.List;

public class Guessing {
	private Set<String> singles = new HashSet<>();
	private Set<String> potentialSingles = new HashSet<>();
	private Set<String> strongSingles = new HashSet<>();
	private String majorSuit;
	private String majorSuit2;
	private Set<String> doubles = new HashSet<>();
	private int state=3;
	
	public Guessing(List<String> three) {
		//Initializing
		initialGuess();
	}
	
	public void initialGuess() {}
	
	public void update3To4(String fourth) {}
	
	public void update4To5(String fifth) {}

}
