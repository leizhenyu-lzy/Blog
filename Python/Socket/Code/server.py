#!C:\\Program Files\\Python39\\python.exe

import socket

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind(("192.168.1.106",1234))
    s.listen()
    c,addr = s.accept()  # c是与客户端对接的socket
    with c:
        print(addr," connected")

        while True:
            data=c.recv(1024)
            if not data:
                break
            print(data)
            c.sendall(data)

