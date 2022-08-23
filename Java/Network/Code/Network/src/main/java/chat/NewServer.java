package chat;

import com.google.gson.Gson;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Arrays;

public class NewServer
{
    public static void main(String[] args)
    {
        ServerSocket serverSocket = null;
        try
        {
            System.out.println("服务器运行中");
            serverSocket = new ServerSocket(9999);
            Socket socket = serverSocket.accept();
            System.out.println("连接到客户端");
            new Thread(new NewServerListener(socket)).start();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
        finally
        {
            if(serverSocket!=null)
            {
                try
                {
                    serverSocket.close();
                }
                catch (IOException e)
                {
                    e.printStackTrace();
                }
            }
        }
    }
}

class NewServerListener implements Runnable
{
    private Socket socket = null;
    private ObjectInputStream ois = null;

    public NewServerListener(Socket outerSocket)
    {
        this.socket = outerSocket;
        try
        {
            this.ois = new ObjectInputStream(this.socket.getInputStream());
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    @Override
    public void run()
    {
        try
        {
            // this.ois = new ObjectInputStream(this.socket.getInputStream());
            while (true)
            {
                System.out.print("From Client : ");
                String jsonString = (String) this.ois.readObject();
                System.out.println(jsonString); // 应该它会阻塞，否则肯定一直输出from client
                Gson gson = new Gson();
                TwoInts twoInts = gson.fromJson(jsonString,TwoInts.class);
                twoInts.doAddition();
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        finally
        {
            if(this.ois!=null)
            {
                try
                {
                    this.ois.close();
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
