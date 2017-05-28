import argparse
import sys
import stun
import time
import subprocess
from socketIO_client import SocketIO

args = sys.argv[1]
if args.startswith("webhandler://"):
    del sys.argv[1]
    if "%20" in args:
        sys.argv = sys.argv+args.split("webhandler://")[1].split("%20")
    else:
        sys.argv = sys.argv+args.split("webhandler://")[1].split(" ")

print sys.argv


parser = argparse.ArgumentParser(description='Some text');
parser.add_argument('--username',action='store')
parser.add_argument('--action',action='store')
parser.add_argument('--server',action='store')
parser.add_argument('--localport',action='store')
parser.add_argument('--id',action='store')

args = parser.parse_args(sys.argv[1:])

action = args.action
username = args.username
server = args.server
localport = args.localport
id = args.id
print args

socket = SocketIO(server)


if action == "stun":
    result = stun.get_ip_info(source_ip="0.0.0.0",
                              source_port=int(localport),
                              stun_host=stun.STUN_SERVERS[0]);

    DATA_TO_SEND = {
        'id':id,
        "username":username,
        'localAddress':'0.0.0.0',
        'localPort':localport,
        'remoteAddress':result['external_ip'],
        'remotePort': result['external_port']
    }
    socket.emit('update',DATA_TO_SEND)

    exit(1)
