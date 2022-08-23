package chat;

import com.google.gson.Gson;

import java.io.IOException;
import java.io.ObjectOutputStream;
import java.net.Socket;

public class NewClient
{
    public static void main(String[] args)
    {
        Socket socket = null;
        try
        {
            socket = new Socket("127.0.0.1", 9999);
            new Thread(new NewClientPublisher(socket)).start();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }
}

class NewClientPublisher implements Runnable
{
    private Socket socket = null;
    private ObjectOutputStream oos = null;

    public NewClientPublisher(Socket outerSocket)
    {
        this.socket = outerSocket;
        // try
        // {
        //     this.oos = new ObjectOutputStream(this.socket.getOutputStream());
        // }
        // catch (IOException e)
        // {
        //     e.printStackTrace();
        // }
    }

    @Override
    public void run()
    {
        try
        {
            this.oos = new ObjectOutputStream(this.socket.getOutputStream());
            while (true)
            {
                Gson gson = new Gson();
                TwoInts twoInts = new TwoInts();
                String jsonString = gson.toJson(twoInts, TwoInts.class);
                System.out.println("To Server : "+jsonString);
                Thread.sleep(1000);
                this.oos.writeObject(jsonString);
                this.oos.flush();
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        finally
        {
            if(this.oos!=null)
            {
                try
                {
                    this.oos.close();
                }
                catch (IOException e)
                {
                    e.printStackTrace();
                }
            }

            if(this.socket!=null)
            {
                try
                {
                    this.socket.close();
                }
                catch (IOException e)
                {
                    e.printStackTrace();
                }
            }
        }

    }
}
