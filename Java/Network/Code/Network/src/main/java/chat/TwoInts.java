package chat;

public class TwoInts
{
    private int a = 0;
    private int b = 1;

    public TwoInts(int a, int b)
    {
        this.a = a;
        this.b = b;
    }

    public TwoInts()
    {
        this.a = (int)(Math.random()*20);
        this.b = (int)(Math.random()*20);
    }


    public void doAddition()
    {
        System.out.println("a + b = "+(a+b));
    }
}
