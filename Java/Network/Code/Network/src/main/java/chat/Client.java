package chat;

import org.json.simple.JSONObject;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;
import java.util.Scanner;

public class Client
{
    private static Socket socket;
    private static boolean connectionState = false;
    private static ObjectOutputStream oos;

    public static void main(String[] args)
    {
        connect();
        if(connectionState)
        {
            try
            {
                oos = new ObjectOutputStream(socket.getOutputStream());
                new Thread(new ClientListener(socket)).start();
                new Thread(new ClientPublisher(socket, oos)).start();
                new Thread(new ClientHeart(socket, oos)).start();
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
        }
    }

    private static void connect()
    {
        try
        {
            socket = new Socket("127.0.0.1", 9999);
            connectionState = true;
        }
        catch (IOException e)
        {
            e.printStackTrace();
            connectionState = false;
        }

    }

}


class ClientListener implements Runnable
{
    private Socket innerSocket;

    ClientListener(Socket outerSocket)
    {
        this.innerSocket = outerSocket;
    }

    @Override
    public void run()
    {
        try
        {
            ObjectInputStream ois = new ObjectInputStream(innerSocket.getInputStream());
            while(true)
                System.out.println(ois.readObject());
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }
}

class ClientPublisher implements Runnable
{
    private Socket innerSocket;
    private ObjectOutputStream innerOos;

    ClientPublisher(Socket outerSocket, ObjectOutputStream outerOos)
    {
        this.innerSocket = outerSocket;
        this.innerOos = outerOos;
    }

    @Override
    public void run()
    {
        try
        {
            // Scanner scanner = new Scanner(System.in);
            while(true)
            {
                Thread.sleep(1000);
                System.out.println("请输入要发送的内容");
                // String string = scanner.nextLine();
                // JSONObject object = new JSONObject();
                // object.put("type", "chat");
                // object.put("msg", string);
                // innerOos.writeObject(object);
                String tempString = "hello server";
                innerOos.writeObject(tempString);
                innerOos.flush();
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }
}


class ClientHeart implements Runnable
{
    private Socket innerSocket;
    private ObjectOutputStream innerOos;

    ClientHeart(Socket outerSocket, ObjectOutputStream outerOos)
    {
        this.innerSocket = outerSocket;
        this.innerOos = outerOos;
    }

    @Override
    public void run()
    {
        try
        {
            System.out.println("心跳包线程已启动");
            while(true)
            {
                Thread.sleep(5000);
                JSONObject object = new JSONObject();
                object.put("type", "heart");
                object.put("msg", "heart");
                innerOos.writeObject(object);
                innerOos.flush();
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }
}

