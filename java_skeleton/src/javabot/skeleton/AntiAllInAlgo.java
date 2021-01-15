package javabot.skeleton;


public class AntiAllInAlgo extends Algo{
    // Algorithm used to fight all in bots specifically
    @Override
    protected double intimidateDec(double raise) {
        return Math.pow(2, -INTIMIDATE_DEC * raise);
    }
}
