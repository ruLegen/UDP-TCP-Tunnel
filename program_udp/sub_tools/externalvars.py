from sub_tools.argcontroler import getargs

import stun,requests,json,time

#initialize all variables

args=getargs();

USERNAME = args.username
REMOTEUSERNAME = args.remoteusername

DIRECTCONNECTION = args.directconnection

SOURCE_PORT = args.sourceport
SOURCE_HOST = args.sourcehost
REMOTE_HOST = args.remotehost
REMOTE_PORT = args.remoteport
IS_SERVER = args.server
OWN_EXTERNAL_IP = ''
OWN_EXTERNAL_PORT=0

SIGNALSERVERHOST = args.signalserver
SOCKETIO_CLIENT = ""

OWN_DATA = {
    'id':"",
    'username': "",
    'localAddress':"",
    'localPort':"",
    'remoteAddress':"",
    'remotePort': ""
}
REPEAT_TIME_USERSEARCHER = 2
FORCENAME = args.forcename
URLS = {
    'register':'/reguser',
    'getuser':'/viewuser',
    'update': '/updateuser'
}
#print(args)
def setSocketIO(socket):
    global SOCKETIO_CLIENT
    SOCKETIO_CLIENT=socket

    #SOCKETIO_CLIENT.on('connect', onConnected)
    #SOCKETIO_CLIENT.on('user-info', onUserInfo)
    #SOCKETIO_CLIENT.on('error', onRegisterError)
    #SOCKETIO_CLIENT.on('disconnect', onDisconnect)
    #SOCKETIO_CLIENT.on('registered', onRegister)
def onRegister(*args):
    SOCKETIO_CLIENT.emit('sendTo')



def doStunRequest():
    result = stun.get_ip_info(source_ip=SOURCE_HOST,
                              source_port=SOURCE_PORT,
                              stun_host=stun.STUN_SERVERS[0]);
    global OWN_EXTERNAL_IP
    global OWN_EXTERNAL_PORT
    global OWN_DATA
    global USERNAME
    global SOCKETIO_CLIENT
    OWN_EXTERNAL_IP = result['external_ip'];
    OWN_EXTERNAL_PORT = result['external_port'];
    OWN_DATA['username'] = USERNAME
    OWN_DATA['remoteAddress']=OWN_EXTERNAL_IP
    OWN_DATA['remotePort'] = OWN_EXTERNAL_PORT
    OWN_DATA['id'] = SOCKETIO_CLIENT._http_session.cookies.values()

    OWN_DATA['localAddress'] = SOURCE_HOST
    OWN_DATA['localPort'] = SOURCE_PORT
    print (result,OWN_DATA)

def regUser():
    global USERNAME
    global SOCKETIO_CLIENT
    updateOwnDataForRequest()
    SOCKETIO_CLIENT.emit('update-info',OWN_DATA)
    SOCKETIO_CLIENT.wait(seconds=5);


def getUser():
    global REMOTE_HOST
    global REMOTE_PORT
    global SOCKETIO_CLIENT
    SOCKETIO_CLIENT.emit('get-user',{'username':REMOTEUSERNAME})
    SOCKETIO_CLIENT.wait(seconds=5);

def updUser():
    global SOCKETIO_CLIENT
    updateOwnDataForRequest()
    request = requests.post(SIGNALSERVERHOST + URLS['update'], data=OWN_DATA)
    response = int(request.text)
    if response:
        print ('Data Changed')
        return 1
    else:
        print ('Data not Changed')
        return 0



def UpdateStunInfo():
    doStunRequest()
    updUser()


def updateOwnDataForRequest():
    global OWN_EXTERNAL_IP
    global OWN_EXTERNAL_PORT
    global OWN_DATA
    global USERNAME
    global SOCKETIO_CLIENT

    OWN_DATA['username'] = USERNAME
    OWN_DATA['remoteAddress'] = OWN_EXTERNAL_IP
    OWN_DATA['remotePort'] = OWN_EXTERNAL_PORT
    OWN_DATA['id'] = SOCKETIO_CLIENT._http_session.cookies.values()
    OWN_DATA['localAddress'] = SOURCE_HOST
    OWN_DATA['localPort'] = SOURCE_PORT

def getInfo():
    print """
    Username {0}
    Local IP {1}
    Local Port {2}
    Own Remote IP {3}
    OwnRemote Port {4}
    =====================
    =====================
    Username {5}
    Remote IP {6}
    Remote Port {7}
    """.format(USERNAME,
               SOURCE_HOST,
               SOURCE_PORT,
               OWN_EXTERNAL_IP,
               OWN_EXTERNAL_PORT,
               REMOTEUSERNAME,
               REMOTE_HOST,
               REMOTE_PORT)

def export(var):
    return eval(var)
def setUsername(user):
    global USERNAME
    USERNAME = user