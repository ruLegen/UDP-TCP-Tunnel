from sub_tools.argcontroler import getargs
import stun,requests,json,time
args=getargs();

USERNAME = args.username
REMOTEUSERNAME = args.remoteusername

DIRECTCONNECTION = args.directconnection

SOURCE_PORT = args.sourceport
SOURCE_HOST = args.sourcehost
REMOTE_HOST = args.remotehost
REMOTE_PORT = args.remoteport

OWN_EXTERNAL_IP = ''
OWN_EXTERNAL_PORT=0

SIGNALSERVERHOST = args.signalserver
OWN_DATA = {}
URLS = {
    'register':'/reguser',
    'getuser':'/viewuser',
    'update': '/updateuser'
}
REPEAT_TIME_USERSEARCHER = 2
#print(args)

def doStunRequest():
    result = stun.get_ip_info(source_ip=SOURCE_HOST,
                              source_port=SOURCE_PORT,
                              stun_host=stun.STUN_SERVERS[0]);
    global OWN_EXTERNAL_IP
    global OWN_EXTERNAL_PORT
    global OWN_DATA
    global USERNAME
    OWN_EXTERNAL_IP = result['external_ip'];
    OWN_EXTERNAL_PORT = result['external_port'];
    OWN_DATA = {'username': USERNAME,'userip':OWN_EXTERNAL_IP,'userport':OWN_EXTERNAL_PORT}

    #print (result,DATA)

def regUser():
    global USERNAME
    updateOwnDataForRequest()
    request = requests.post(SIGNALSERVERHOST+URLS['register'], data=OWN_DATA)
    response = int(request.text)
    if response:
        print ('Registred')
        return 1
    else:
        print ('This username %s already is using. Please Choose another name'%USERNAME)
        USERNAME = raw_input("Enter user name: ")
        regUser()


def getUser():
    global REMOTE_HOST
    global REMOTE_PORT
    request = requests.post(SIGNALSERVERHOST + URLS['getuser'], data={'username':REMOTEUSERNAME})
    response = request.text
    user = json.loads(response)
    if len(user) > 0:
        REMOTE_HOST = user['userip']
        print REMOTE_HOST
        REMOTE_PORT = user['userport']
        return 1
    else:
        print ('User {0} not found maybe he is not Regsitered. Will try in {1} seconds'.format(REMOTEUSERNAME,REPEAT_TIME_USERSEARCHER))
        time.sleep(REPEAT_TIME_USERSEARCHER)
        getUser();

def updUser():
    updateOwnDataForRequest()
    request = requests.post(SIGNALSERVERHOST + URLS['update'], data=OWN_DATA)
    response = int(request.text)
    if response:
        print ('Data Changed')
        getInfo()
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
    OWN_DATA = {'username': USERNAME,'userip':OWN_EXTERNAL_IP,'userport':OWN_EXTERNAL_PORT}

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
