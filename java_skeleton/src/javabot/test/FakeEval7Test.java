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
        assertEquals(13,eval7.isStraight(straight),"Expect a straight largest K");
    }
	
	@Test
	public void testIsNotStraight() {
		List<String> straight=List.of("Ts","Kc","9h","Qs","9d");
        assertEquals(eval7.isStraight(straight),0,"Expect a 0 for not a straight");
    }
	
	@Test
	public void testA5Straight() {
		List<String> straight=List.of("As","2c","3h","4s","5d");
        assertEquals(5,eval7.isStraight(straight),"Expect a 5 for an A2345 straight");
    }
	
	@Test
	public void test26Straight() {
		List<String> straight=List.of("6s","2c","3h","4s","5d");
        assertEquals(6,eval7.isStraight(straight),"Expect a 6 for an 23456 straight");
    }
	
	@Test
	public void testFlush() {
		List<String> flush=List.of("6s","2s","3s","7s","8s");
        assertTrue(eval7.isFlush(flush),"Expect a flush");
    }
	
	@Test
	public void testNotFlush() {
		List<String> flush=List.of("6s","2c","8h","4s","5d");
        assertFalse(eval7.isFlush(flush),"Expect a non-flush");
    }
}