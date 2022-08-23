package chat;

import java.io.*;
import java.net.Socket;
import java.util.logging.Level;

// 客户端上传文件
public class FileUpload
{

    public static void main(String[] args) throws IOException
    {
        Socket socket = new Socket("127.0.0.1",8888);
        OutputStream os = socket.getOutputStream();
        FileInputStream fis = new FileInputStream(new File("testSend.png"));

        byte[] buffer = new byte[1024];
        int readLength;
        while((readLength=fis.read(buffer))!=-1)
        {
            os.write(buffer,0, readLength);
            os.flush();
        }

        socket.shutdownOutput();

        fis.close();
        os.close();
        socket.close();
    }
}
