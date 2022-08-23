package chat;

import org.json.simple.JSONObject;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

public class Server
{
    public static void main(String[] args)
    {
        try
        {
            System.out.println("Socket服务器开始运行");
            ServerSocket serverSocket = new ServerSocket(9999);
            while (true)  // 一直循环以接收多个客户请求
            {
                Socket socket = serverSocket.accept();
                new Thread(new ServerListener(socket)).start();
                new Thread(new ServerPublisher(socket)).start();
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }
}




// 监听线程
class ServerListener implements Runnable
{
    private Socket innerSocket;

    ServerListener(Socket outerSocket)
    {
        this.innerSocket = outerSocket;
    }

    @Override
    public void run()
    {
        try
        {
            ObjectInputStream ois = new ObjectInputStream(innerSocket.getInputStream());
            while (true)  // 保持监听状态
            {
                System.out.print("From Client:");
                System.out.println(ois.readObject());
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        finally
        {
            try
            {
                innerSocket.close();
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
        }

    }
}

class ServerPublisher implements Runnable
{
    private Socket innerSocket;

    ServerPublisher(Socket outerSocket)
    {
        this.innerSocket = outerSocket;
    }


    @Override
    public void run()
    {
        try
        {
            ObjectOutputStream oos = new ObjectOutputStream(innerSocket.getOutputStream());
            Scanner scanner = new Scanner(System.in);
            while (true)
            {
                System.out.println("请输入要发送的内容");
                String string = scanner.nextLine();
                JSONObject object = new JSONObject();
                object.put("type", "chat");
                object.put("msg", string);
                oos.writeObject(object);
                oos.flush();
            }
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }
}

