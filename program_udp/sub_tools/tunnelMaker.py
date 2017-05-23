import socket
import time
from math import ceil
def directConnection(LOCAL_IP,LOCAL_PORT,REMOTE_IP,REMOTE_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    sock.bind((LOCAL_IP, LOCAL_PORT));
    while 1:
        message = raw_input();
        sock.sendto(message, (REMOTE_IP, REMOTE_PORT))
        conn, addr = sock.recvfrom(1024)
        print('client addr: ', (addr, conn), time.clock())
        time.sleep(1)

def breakthroughTunnel(LOCAL_IP,LOCAL_PORT, REMOTE_IP, REMOTE_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    sock.bind((LOCAL_IP, LOCAL_PORT));
    iterator = 0
    message = 'Hi'
    while 1:
        sock.sendto(message, (REMOTE_IP, int(REMOTE_PORT)))
        print ('sended from {0} {1} to {2} {3}'.format(LOCAL_IP,LOCAL_PORT,REMOTE_IP,REMOTE_PORT))
        conn, addr = sock.recvfrom(1024)
        print('Tunel probit')
        if iterator > 1:
            message = 'close'
        if conn == 'close':
            print ('Tunnel is working')
            sock.sendto('close', (REMOTE_IP, int(REMOTE_PORT)))
            sock.close()
            break
        print('client addr: ', (addr, conn), time.clock())
        time.sleep(1)
        iterator = iterator+1


def serverSharePort(LOCAL_IP,LOCAL_PORT,REMOTE_IP,REMOTE_PORT,LOCAL_RANDOM_PORT,LOCAL_SHARE_PORT=8080,BUFF_SIZE=4096,MTU_SIZE=1400):
    print "I'm a server listening {0}:{1} and sharing {2}:{3}".format(LOCAL_IP, LOCAL_PORT,LOCAL_IP,LOCAL_SHARE_PORT)
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock1.bind((LOCAL_IP, LOCAL_PORT));
    while 1:

        connection, address = sock1.recvfrom(2048)
        print address
        sdata = connection
        localData = ""
        if sdata and sdata != 'close':
            print "Something came\n{0}".format(sdata)
            localSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            localSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            localSocket.bind((LOCAL_IP, LOCAL_RANDOM_PORT))
            print "Redirecting to {0}:{1}".format(LOCAL_IP, LOCAL_SHARE_PORT, sdata)
            localSocket.connect((LOCAL_IP, LOCAL_SHARE_PORT))
            localSocket.send(sdata)
            buff = ""
            while 1:
                localData = localSocket.recv(BUFF_SIZE)
                buff += localData
                if (len(localData) <= 0):
                    break
                print (len(localData))
            localSocket.close()
            # separate message by MTU size
            if len(buff) > MTU_SIZE:
                for i in range(0, int(ceil(len(buff) / MTU_SIZE)) + 1, 1):
                    sock1.sendto(buff[MTU_SIZE * i:MTU_SIZE * (i + 1)],
                                 (REMOTE_IP, int(REMOTE_PORT)))
            else:
                sock1.sendto(buff, (REMOTE_IP, int(REMOTE_PORT)))
            sdata = None