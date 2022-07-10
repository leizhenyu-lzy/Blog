import socket

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    # s.connect(("127.0.0.1",1234))
    s.connect(("192.168.1.106",1234))
    s.sendall(b"hello!")  # b表示字节序列
    data = s.recv(1024)
    print("Received : ",repr(data))
