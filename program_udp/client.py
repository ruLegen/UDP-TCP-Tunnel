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

    while 1:
        sock.sendto('12', (export('REMOTE_HOST'), int(export('REMOTE_PORT'))))
        conn, addr = sock.recvfrom(1024)
        print('Tunel probit')
        print('client addr: ', (addr, conn), time.clock())
        time.sleep(1)
        break
    print ('Tunnel is working')