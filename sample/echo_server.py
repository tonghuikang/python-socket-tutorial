# https://gist.github.com/jmhobbs/11276249

import os
import socket
import time

socket_path = './socket'

if os.path.exists(socket_path):
    os.remove(socket_path)

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
    sock.bind(socket_path)
    sock.listen()
    while True:
        conn, _addr = sock.accept()
        data = conn.recv(1024)
        time.sleep(1) # do some work
        conn.send(data)
        conn.close()