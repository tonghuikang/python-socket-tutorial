# https://www.hackerrank.com/contests/quora-haqathon/challenges/sortedset/problem
# https://www.hackerrank.com/rest/contests/quora-haqathon/challenges/sortedset/hackers/garygary123456/download_solution

import socket
import struct
import sys
import os
import threading

global data,lock
data = {}
lock = threading.Lock()

def getMsg(connection):
    msg = connection.recv(4)
    msg = (struct.unpack('!I',msg))[0]
    print('received ',msg)
    return msg

def sendMsg(connection,msgs):
    for msg in msgs:
        print('sent',msg)
        msg = struct.pack('!I',msg)
        connection.sendall(msg)

def addScore(sid,key,score):
    global data
    #TODO:LOCK
    lock.acquire()
    if sid not in data:
        data[sid] = {}
    if key not in data[sid]:
        data[sid][key] = 0
    data[sid][key] += score
    lock.release()

def removeKey(sid,key):
    global data
    #TODO:LOCK
    lock.acquire()
    if sid in data:
        if key in data[sid]:
            del data[sid][key]
    lock.release()

def getSize(sid):
    global data
    #TODO:LOCK
    lock.acquire()
    ans = 0
    if sid in data:
        ans = len(data[sid])
    lock.release()
    return ans

def getValue(sid,key):
    global data
    #TODO:LOCK
    lock.acquire()
    ans = 0
    if sid in data:
        if key in data[sid]:
            ans = data[sid][key]
    lock.release()
    return ans

def getRange(sids,lower,upper):
    global data
    ans = []
    lock.acquire()
    for sid in sids:
        if sid not in data:
            continue

        for key in data[sid]:
            if lower <= data[sid][key] <= upper:
                ans.append((key,data[sid][key]))
                #print(ans)
    lock.release()

    return sorted(ans)

def client(connection):
    global data

    while True:
        n = getMsg(connection)
        print(n)

        msg = getMsg(connection)
        print(msg)
        
        if (msg == 1):
            sid = getMsg(connection)
            key = getMsg(connection)
            score = getMsg(connection)
            addScore(sid,key,score)
            sendMsg(connection,[0])

        if (msg == 2):
            sid = getMsg(connection)
            key = getMsg(connection)
            removeKey(sid,key)
            sendMsg(connection,[0])

        if (msg == 3):
            sid = getMsg(connection)
            size = getSize(sid)
            sendMsg(connection,[1,size])

        if (msg == 4):
            sid = getMsg(connection)
            key = getMsg(connection)
            val = getValue(sid,key)
            sendMsg(connection,[1,val])

        if (msg == 5):
            sids = []
            while True:
                sid = getMsg(connection)
                if sid == 0:
                    break
                sids.append(sid)
            
            #print(sids)

            lower = getMsg(connection)
            upper = getMsg(connection)

            ans = getRange(sids,lower,upper)
            r_msg = [len(ans)*2]
            for x in ans:
                r_msg.append(x[0])
                r_msg.append(x[1])
            #print(r_msg)
            sendMsg(connection,r_msg)

        if (msg == 6):
            break

    connection.close()
    #print('Closed')
        

server_address = './socket'

# Make sure the socket does not already exist
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Bind the socket to the port
sock.bind(server_address)

# Listen for incoming connections
sock.listen(10)

while True:
    # Wait for a connection
    # print('waiting for a connection')
    connection, client_address = sock.accept()

    tar = threading.Thread(target = client, args=(connection,))
    tar.start()
