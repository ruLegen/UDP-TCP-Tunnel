from sub_tools.externalvars import *
from sub_tools import tunnelMaker
import time
import socket
import threading
from socketIO_client import SocketIO, LoggingNamespace

autostun = threading.Thread(target=autoStunUpdate)

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
    autostun.start()
    if isServer:
        tunnelMaker.serverSharePort(SOURCE_HOST,SOURCE_PORT,REMOTE_HOST,REMOTE_PORT,localRandomPort,localSharePort)
    # if you are client
    else:
        tunnelMaker.clientSharePort(SOURCE_HOST,SOURCE_PORT,REMOTE_HOST,REMOTE_PORT,localRandomPort)





if DIRECTCONNECTION:
    tunnelMaker.breakthroughTunnel(SOURCE_HOST, SOURCE_PORT, REMOTE_HOST, REMOTE_PORT)
    autostun.start()
else:
    mySocketIO = SocketIO(SIGNALSERVERHOST);

    mySocketIO.on('registered', onRegister)
    mySocketIO.on('connect', onConnected)
    mySocketIO.on('user-info', onUserInfo)
    mySocketIO.on('error', onRegisterError)
    mySocketIO.on('disconnect', onDisconnect)
    mySocketIO.on('registered', onRegister)
    setSocketIO(mySocketIO)
    doStunRequest()
    regUser()
    getInfo()


























