package javabot.test;

import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.util.Set;

import org.junit.jupiter.api.Test;

import javabot.skeleton.FakeEval7;

import java.util.List;

public class FakeEval7Test {
	
	FakeEval7 eval7=new FakeEval7();
	
	@Test
	public void testIsStraight() {
		List<String> straight=List.of("Ts","Kc","Jh","Qs","9d");
        assertEquals(13,FakeEval7.isStraight(straight),"Expect a straight largest K");
    }
	
	@Test
	public void testIsNotStraight() {
		List<String> straight=List.of("Ts","Kc","9h","Qs","9d");
        assertEquals(FakeEval7.isStraight(straight),0,"Expect a 0 for not a straight");
    }
	
	@Test
	public void testA5Straight() {
		List<String> straight=List.of("As","2c","3h","4s","5d");
        assertEquals(5,FakeEval7.isStraight(straight),"Expect a 5 for an A2345 straight");
    }
	
	@Test
	public void test26Straight() {
		List<String> straight=List.of("6s","2c","3h","4s","5d");
        assertEquals(6,FakeEval7.isStraight(straight),"Expect a 6 for an 23456 straight");
    }
	
	@Test
	public void testFlush() {
		List<String> flush=List.of("6s","2s","3s","7s","8s");
        assertTrue(FakeEval7.isFlush(flush),"Expect a flush");
    }
	
	@Test
	public void testNotFlush() {
		List<String> flush=List.of("6s","2c","8h","4s","5d");
        assertFalse(FakeEval7.isFlush(flush),"Expect a non-flush");
    }
	
	@Test
	public void testScoreRoyalFlush() {
		List<String> cards=List.of("Ts","As","Ks","Js","Qs");
		assertEquals(FakeEval7.handScore(cards),10<<20,"Expect a True score");
		
    }
	
	@Test
	public void testScoreStriaghtFlush() {
		List<String> cards=List.of("Jc","9c","8c","Tc","7c");
		assertEquals(FakeEval7.handScore(cards),(9<<20)+(11<<16),"Expect a True score");
    }
	
	@Test
	public void testScoreStriaghtA5Flush() {
		List<String> cards=List.of("Ac","2c","5c","4c","3c");
		assertEquals(FakeEval7.handScore(cards),(9<<20)+(5<<16),"Expect a True score");
    }
	
	@Test
	public void testScore4OfAKind() {
		List<String> cards=List.of("6s","6c","6h","4s","6d");
		assertEquals(FakeEval7.handScore(cards),(8<<20)+(6<<16)+(4<<12),"Expect a True score");
    }
	
	@Test
	public void testScoreFullHouse() {
		List<String> cards=List.of("6s","6c","8h","8s","6d");
		assertEquals(FakeEval7.handScore(cards),(7<<20)+(6<<16)+(8<<12),"Expect a True score");
    }
	
	@Test
	public void testScoreFlush() {
		List<String> cards=List.of("6s","7s","8s","4s","Ts");
		assertEquals(FakeEval7.handScore(cards),(6<<20)+(10<<16)+(8<<12)+(7<<8)+(6<<4)+(4),"Expect a True score");
    }
	
	@Test
	public void testScoreStraight() {
		List<String> cards=List.of("6s","7c","8h","9s","Td");
		assertEquals(FakeEval7.handScore(cards),(5<<20)+(10<<16),"Expect a True score");
    }
	
	@Test
	public void testScoreA5Straight() {
		List<String> cards=List.of("As","2c","3h","5s","4d");
		assertEquals(FakeEval7.handScore(cards),(5<<20)+(5<<16),"Expect a True score");
    }

	@Test
	public void testScore3OfAKind() {
		List<String> cards=List.of("Ts","9c","Th","8s","Td");
		assertEquals(FakeEval7.handScore(cards),(4<<20)+(10<<16)+(9<<12)+(8<<8),"Expect a True score");
    }

	@Test
	public void testScoreTwoPairs() {
		List<String> cards=List.of("6s","2c","4h","4s","6d");
		assertEquals(FakeEval7.handScore(cards),(3<<20)+(6<<16)+(4<<12)+(2<<8),"Expect a True score");
    }

	@Test
	public void testScoreOnePair() {
		List<String> cards=List.of("6s","2c","3h","4s","6d");
		assertEquals(FakeEval7.handScore(cards),(2<<20)+(6<<16)+(4<<12)+(3<<8)+(2<<4),"Expect a True score");
    }
	
	@Test
	public void testScoreOnePair2() {
		List<String> cards=List.of("6s","Ac","3h","4s","4d");
		assertEquals(FakeEval7.handScore(cards),(2<<20)+(4<<16)+(14<<12)+(6<<8)+(3<<4),"Expect a True score");
    }

	@Test
	public void testScoreHighCard() {
		List<String> cards=List.of("6s","2c","8h","4s","5d");
        assertEquals(FakeEval7.handScore(cards),(1<<20)+(8<<16)+(6<<12)+(5<<8)+(4<<4)+(2),"Expect a True score");
    }
	
	@Test
	public void testMixingHighCard() {
		List<String> common=List.of("6s","2c","8h","4s","5d");
		List<String> ours=List.of("Kc","Ad");
		List<String> highest=List.of("Kc","Ad","8h","5d","6s");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(highest),"Expect a True score");
    }
	
	@Test
	public void testMixingOnePair() {
		List<String> common=List.of("6s","2c","8h","4s","5d");
		List<String> ours=List.of("6c","Ad");
		List<String> highest=List.of("6c","Ad","8h","5d","6s");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(highest),"Expect a True score");
    }
	
	@Test
	public void testMixingOnePair2() {
		List<String> common=List.of("6s","2c","8h","4s","5d");
		List<String> ours=List.of("Ac","Ad");
		List<String> highest=List.of("Ac","Ad","8h","5d","6s");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(highest),"Expect a True score");
    }
	
	@Test
	public void testMixingTwoairs() {
		List<String> common=List.of("6s","2c","8h","4s","5d");
		List<String> ours=List.of("6c","8d");
		List<String> highest=List.of("6c","8d","8h","5d","6s");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(highest),"Expect a True score");
    }
	
	@Test
	public void testMixingThreeOfAKind() {
		List<String> common=List.of("6s","2c","8h","4s","5d");
		List<String> ours=List.of("6c","6d");
		List<String> highest=List.of("6c","5c","8h","6d","6s");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(highest),"Expect a True score");
    }

	@Test
	public void testMixingStraight() {
		List<String> common=List.of("6s","2c","8h","4s","5d");
		List<String> ours=List.of("3c","Ac");
		List<String> highest=List.of("6c","5c","4s","2c","3c");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(highest),"Expect a True score");
    }

	@Test
	public void testMixingFlush() {
		List<String> common=List.of("6s","2s","8h","4s","5d");
		List<String> ours=List.of("As","Ks");
		List<String> highest=List.of("As","Ks","6s","2s","4s");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(highest),"Expect a True score");
    }

	@Test
	public void testMixingFullHouse() {
		List<String> common=List.of("6s","2c","6h","4s","5d");
		List<String> ours=List.of("6c","4c");
		List<String> highest=List.of("6c","6h","4s","4c","6s");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(highest),"Expect a True score");
    }
	
	@Test
	public void testMixingFullHouse2() {
		List<String> common=List.of("6s","6d","6h","4s","4d");
		List<String> ours=List.of("Ac","Kc");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(common),"Expect a True score");
    }
	
	@Test
	public void testMixingFullHouse3() {
		List<String> common=List.of("6s","6d","6h","4s","4d");
		List<String> ours=List.of("Ac","4c");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(common),"Expect a True score");
    }
	
	@Test
	public void testMixingFullHouse4() {
		List<String> common=List.of("6s","6d","6h","4s","3d");
		List<String> ours=List.of("Ac","4c");
		List<String> highest=List.of("6c","6h","4s","4c","6s");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(highest),"Expect a True score");
    }
	
	@Test
	public void testMixingFullHouse5() {
		List<String> common=List.of("6s","6d","4c","4s","3d");
		List<String> ours=List.of("Ac","6h");
		List<String> highest=List.of("6c","6h","4s","4c","6s");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(highest),"Expect a True score");
    }
	
	@Test
	public void testMixing4OfaKind() {
		List<String> common=List.of("6s","2c","6h","4s","5d");
		List<String> ours=List.of("6c","6d");
		List<String> highest=List.of("6c","6h","5d","6h","6d");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(highest),"Expect a True score");
    }

	@Test
	public void testMixingStraightFlush() {
		List<String> common=List.of("6s","2d","8h","4d","5d");
		List<String> ours=List.of("6d","3d");
		List<String> highest=List.of("6d","3d","2d","5d","4d");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(highest),"Expect a True score");
    }

	@Test
	public void testMixingTwoairs2() {
		List<String> common=List.of("6s","2c","3c","4c","5c");
		List<String> ours=List.of("6c","Ac");
		List<String> highest=List.of("6c","5c","4c","3c","2c");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(highest),"Expect a True score");
    }

	@Test
	public void testMixingRoyalFlush2() {
		List<String> common=List.of("As","Ks","Qs","Ts","5d");
		List<String> ours=List.of("6c","Js");
		List<String> highest=List.of("As","Ts","Qs","Ks","Js");
        assertEquals(FakeEval7.score(ours, common),FakeEval7.handScore(highest),"Expect a True score");
    }

}