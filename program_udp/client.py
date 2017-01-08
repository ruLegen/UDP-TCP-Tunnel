from sub_tools.externalvars import *
import time
import socket
import threading
doStunRequest()

if DIRECTCONNECTION:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    sock.bind((SOURCE_HOST, SOURCE_PORT));
    while 1:
        message = raw_input();
        sock.sendto(message, (REMOTE_HOST, REMOTE_PORT))
        conn, addr = sock.recvfrom(1024)
        print('client addr: ', (addr, conn), time.clock())
        time.sleep(1)
else:
    regUser()
    getUser()
    getInfo()
    print 'Trying connect to him'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    sock.bind((SOURCE_HOST, SOURCE_PORT));
    iterator = 0
    message = 'Hi'
    while 1:
        sock.sendto(message, (export('REMOTE_HOST'), int(export('REMOTE_PORT'))))
        conn, addr = sock.recvfrom(1024)
        print('Tunel probit')
        if iterator > 3:
            message = 'close'
        if conn == 'close':
            print ('Tunnel is working')
            sock.sendto('close', (export('REMOTE_HOST'), int(export('REMOTE_PORT'))))
            sock.close()
            break
        print('client addr: ', (addr, conn), time.clock())
        time.sleep(1)
        iterator = iterator+1



localSharePort = 8080
localRandomPort = 12333
isServer = IS_SERVER


if isServer:
    print """I'm a server listening {0}:{1}""".format(SOURCE_HOST,SOURCE_PORT)
    while 1:
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock1.bind((SOURCE_HOST, SOURCE_PORT));
        connection,address = sock1.recvfrom(2048)
        print connection
        sdata = connection
        localData = None
        if sdata and sdata != 'close':
            print """Something came\n{0}""".format(sdata)
            localSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            localSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            localSocket.bind((SOURCE_HOST,localRandomPort))
            print """Redirecting to {0}:{1} -- {2}""".format(SOURCE_HOST,localSharePort,sdata)
            localSocket.connect((SOURCE_HOST,localSharePort))
            localSocket.send(sdata)
            localData = localSocket.recv(2048)
        if localData:
            localSocket.close()
            sock1.sendto(localData,(export('REMOTE_HOST'), int(export('REMOTE_PORT'))))
            sdata = None
            localData = None
else:
    while 1:
        localSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        localSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        localSocket.bind((SOURCE_HOST,localRandomPort))
        localSocket.listen(1)
        conn,addr = localSocket.accept()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((SOURCE_HOST, SOURCE_PORT));
        data = conn.recv(2048)
        sock.sendto(data, (export('REMOTE_HOST'), int(export('REMOTE_PORT'))))
        remoteData = sock.recv(2048)

        localSocket.sendto(remoteData,addr)
        localSocket.close()
