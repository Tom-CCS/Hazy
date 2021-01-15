package javabot.skeleton;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Timer {
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
	
	public static void main(String[] args) {
		List<String> cards=List.of("Kh","6s");
		List<String> com=List.of("Ks","6h","Ac");
		long startTime =  System.currentTimeMillis();
		List<String> rest = new ArrayList<String>(Deck);
		List<String> seen=new ArrayList<>(cards);
        seen.addAll(com);
        for (String card: seen) {
            rest.remove(card);
        }
        String card1;
        String card2;
        Set<Set<String>> goodGuess=new HashSet<>();
        List<String> rest2=new ArrayList<>(rest);
        int iteration=100;
        for (int i=0;i<rest.size();i++) {
        	for (int j=i+1;j<rest.size();j++) {
        		card1=rest.get(i);
        		card2=rest.get(j);
            	rest2.remove(card1);
            	rest2.remove(card2);
            	int score=0;
            	//for(int k=0;k<iteration;k++) {
            	//	score+=CalcProb.winOrLose(List.of(card1,card2), com, List.of(), rest2);
            	//}
            	if (score>100) {goodGuess.add(Set.of(card1,card2));}
            	rest2.add(card1);
            	rest2.add(card2);
            }
        }
		long endTime =  System.currentTimeMillis();
		long usedTime = (endTime-startTime);
		System.out.println(usedTime);
		System.out.println(goodGuess);
	}

}
