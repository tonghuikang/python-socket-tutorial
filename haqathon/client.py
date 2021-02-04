import socket
import struct


def send_msg(list_of_int):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect("./socket")
    
    for integer in list_of_int:
        s = struct.pack('!I',integer)
        client.send(s)
    
    result = client.recv(4)
    result_arr = []
    if result:
        integer = struct.unpack('!I',result)[0]
        result_arr.append(integer)
        for _ in range(integer):
            result = client.recv(4)
            integer = struct.unpack('!I',result)[0]
            result_arr.append(integer)
    return result_arr


results = []
num_lines = int(input())

for _ in range(num_lines):
    line = list(map(int, input().split()))
    response = send_msg(line)
    results.append(response)
    
for result in results:
    print("\n".join(str(x) for x in result))