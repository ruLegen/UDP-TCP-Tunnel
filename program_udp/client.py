from sub_tools.externalvars import *
from sub_tools import tunnelMaker
import time
import socket
from socketIO_client import SocketIO, LoggingNamespace



def onConnected(*args):
    print('On Connected')

def onUserInfo(*args):
    global REMOTE_HOST
    global REMOTE_PORT
    print "onUserInfo"
    if args[0]:
        REMOTE_HOST = args[0][0]['remoteAddress']
        REMOTE_PORT = args[0][0]['remotePort']
        print REMOTE_HOST
        print REMOTE_PORT
        return 1
    else:
        print ('User {0} not found maybe he is not Regsitered. Will try in {1} seconds'.format(REMOTEUSERNAME,REPEAT_TIME_USERSEARCHER))
        time.sleep(REPEAT_TIME_USERSEARCHER)
        getUser();

def onRegisterError(*args):
    print ('This username {0} already is using. Please Choose another name'.format(args[0]['username']))
    setUsername(raw_input("Enter user name: "))
    regUser()

def onDisconnect(*args):
    print('On Disconnect')


def onRegister(*args):
    # here is trafic redirector
    print "registered"
    getUser()
    tunnelMaker.breakthroughTunnel(SOURCE_HOST,SOURCE_PORT,REMOTE_HOST,REMOTE_PORT)
    localSharePort = 8080
    localRandomPort = 12333
    isServer = IS_SERVER
    BUFF_SIZE = 4096
    MTU_SIZE = 1400

    if isServer:
        tunnelMaker.serverSharePort(SOURCE_HOST,SOURCE_PORT,REMOTE_HOST,REMOTE_PORT,localRandomPort,localSharePort)
    # if you are client
    else:
        while 1:
            localSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            localSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            localSocket.bind((SOURCE_HOST, localRandomPort))
            localSocket.listen(1)
            conn, addr = localSocket.accept()
            print addr
            data = conn.recv(BUFF_SIZE)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((SOURCE_HOST, SOURCE_PORT));

            sock.sendto(data, (REMOTE_HOST, int(REMOTE_PORT)))
            remoteData = ""
            while 1:
                localData = sock.recv(BUFF_SIZE)
                remoteData += localData
                if (len(localData) < MTU_SIZE):
                    break
                print (len(localData))
            conn.sendall(remoteData)
            conn.close()
            localSocket.close()




mySocketIO = SocketIO(SIGNALSERVERHOST);

mySocketIO.on('registered', onRegister)
mySocketIO.on('connect', onConnected)
mySocketIO.on('user-info', onUserInfo)
mySocketIO.on('error', onRegisterError)
mySocketIO.on('disconnect', onDisconnect)
mySocketIO.on('registered', onRegister)
setSocketIO(mySocketIO)
doStunRequest()

if DIRECTCONNECTION:
    tunnelMaker.directConnection(SOURCE_HOST, SOURCE_PORT, REMOTE_HOST, REMOTE_PORT)
else:

    regUser()

    getInfo()


























