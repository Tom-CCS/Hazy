package javabot.test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

import org.junit.jupiter.api.Test;

import javabot.skeleton.CalcProb;

public class ProbabilityTest {
	
	/*
	 *     assert calc_prob([As,Ah],[Ac,Kh,Ks,Kd,Qc])==43/45
    assert calc_prob([As,Ah],[Ac,Kh,Ks,Qd,Qc])==1-4/(44*45)
    # lose iff opp has Kc, Kd or Qs, Qh
    assert calc_prob([Kc,Kd],[Kh,Qh,Th,Ks,Qs])==1-4/(44*45)
    # lose iff As, Js or 9s, Js
    assert calc_prob([Kc,Kd],[Kh,Td,Tc,Ks])==1
    # Never lose
    assert calc_prob([Kc,Kd],[Kh,Ts,Tc,Ks])==1-12/(44*45*46)
    # lose iff the remaining and the opponent are Js, Qs, As/9s 
    assert calc_prob([Kc,Kd],[Kh,Jd,Ks])>0.998
    # There is a four of a kind, almost never lose
    assert calc_prob([Kc,Kd],[Kh,Td,Ts])>0.99
    # There is a large full house, really high prob to win
    assert calc_prob([Jc,Kd],[Kh,Jd,Js])>0.95
    # There is a small full house, very high prob to win
    assert calc_prob([Ac,Kd],[Qh,Jd,Ts])>0.93
    # There is a straight, very high prob to win
    assert calc_prob([Ac,Td],[Th,Jd,Ts])>0.9
    # There is a three of a kind, high prob to win
    assert calc_prob([Jc,Kd],[Kh,Td,Js])>0.8
    # There is a large two pairs, high prob to win
	 */
	
	@Test
	public void testBlind() {
		List<String> ours=List.of("As","Ah");
		List<String> common=List.of();
		assertTrue(CalcProb.calcProb(ours, common, false)>0.85 && CalcProb.calcProb(ours, common, false)<0.86,"Expect a True Raw Prob");
	}
	
	@Test
	public void testBlind2() {
		List<String> ours=List.of("As","Kh");
		List<String> common=List.of();
		assertTrue(CalcProb.calcProb(ours, common, false)>0.65 && CalcProb.calcProb(ours, common, false)<0.66,"Expect a True Raw Prob");
	}
	
	@Test
	public void testBlind3() {
		List<String> ours=List.of("As","Ks");
		List<String> common=List.of();
		assertTrue(CalcProb.calcProb(ours, common, false)>0.67 && CalcProb.calcProb(ours, common, false)<0.68,"Expect a True Raw Prob");
	}
	
	@Test
	public void test251() {
		List<String> ours=List.of("As","Ah");
		List<String> common=List.of("Ac","Kh","Kd","Qs","Kc");
		double prob=CalcProb.calcProb(ours, common, false);
        assertTrue(prob > 0.94 & prob<0.99 ,"Expect a true prob");
    }
	
	@Test
	public void test252() {
		List<String> ours=List.of("Kc","Kd");
		List<String> common=List.of("Kh","Qh","Th","Ks","Qs");
        assertTrue(CalcProb.calcProb(ours, common, false) > 0.98, "Expect a true prob");
    }
	
	@Test
	public void test241() {
		List<String> ours=List.of("Kc","Kd");
		List<String> common=List.of("Kh","Ts","Tc","Ks");
        assertTrue(CalcProb.calcProb(ours, common, false) > 0.98 ,"Expect a true prob");
    }
	
	@Test
	public void test243() {
		List<String> ours=List.of("Kc","Kd");
		List<String> common=List.of("Kh","Td","Tc","Ks");
        assertEquals(CalcProb.calcProb(ours, common, false),(double) 1,"Expect a true prob");
    }
	
	@Test
	public void test231() {
		List<String> ours=List.of("Kc","Kd");
		List<String> common=List.of("Kh","Jd","Ks");
        assertTrue(CalcProb.calcProb(ours, common, false) > 0.98,"Expect a true prob");
    }
	
	@Test
	public void test232() {
		List<String> ours=List.of("Kc","Kd");
		List<String> common=List.of("Kh","Td","Ts");
        assertTrue(CalcProb.calcProb(ours, common, false) > 0.98,"Expect a true prob");
    }
	
	@Test
	public void test233() {
		List<String> ours=List.of("Jc","Kd");
		List<String> common=List.of("Kh","Jd","Js");
        assertTrue(CalcProb.calcProb(ours, common, false) > 0.95,"Expect a true prob");
    }
	
	@Test
	public void test234() {
		List<String> ours=List.of("Ac","Kd");
		List<String> common=List.of("Qh","Jd","Ts");
		double prob=CalcProb.calcProb(ours, common, false);
        assertTrue(prob > 0.92 & prob < 0.99,"Expect a true prob");
    }
	
	@Test
	public void test235() {
		List<String> ours=List.of("Ac","Td");
		List<String> common=List.of("Th","Jd","Ts");
		double prob=CalcProb.calcProb(ours, common, false);
        assertTrue(prob > 0.85 & prob < 0.95,"Expect a true prob");
    }
	
	@Test
	public void test236() {
		List<String> ours=List.of("Jc","Kd");
		List<String> common=List.of("Kh","Td","Js");
		double prob=CalcProb.calcProb(ours, common, false);
        assertTrue(prob > 0.75 & prob < 0.87,"Expect a true prob");
    }
	
}
