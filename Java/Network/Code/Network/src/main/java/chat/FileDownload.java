package chat;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;

// 服务端接收文件
public class FileDownload
{
    public static void main(String[] args) throws IOException
    {
        ServerSocket serverSocket = new ServerSocket(8888);
        Socket accept = serverSocket.accept();
        InputStream is = accept.getInputStream();
        FileOutputStream fos = new FileOutputStream(new File("testReceive.png"));

        byte[] buffer = new byte[1024];
        int readLength;

        while((readLength = is.read(buffer))!=-1)
        {
            fos.write(buffer,0,readLength);
        }

        fos.close();
        is.close();
        serverSocket.close();

        accept.shutdownInput();

    }
}
