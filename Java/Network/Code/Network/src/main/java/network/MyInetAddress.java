package network;

import java.net.InetAddress;
import java.net.UnknownHostException;

public class MyInetAddress
{
    public static void main(String[] args) throws UnknownHostException
    {
        InetAddress localHost = InetAddress.getLocalHost();
        System.out.println(localHost);  // DESKTOP-D4K3O6R/192.168.95.1



    }
}
