import stun
import time
from sub_tools.externalvars import *
import socket

import sys


#result = stun.get_ip_info(source_ip=SOURCE_HOST,
#                          source_port=SOURCE_PORT,
#                          stun_host=stun.STUN_SERVERS[0]);
#OWN_EXTERNAL_IP = result.external_ip;
#OWN_EXTERNAL_PORT = result.external_port;


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM);
sock.bind((SOURCE_HOST,SOURCE_PORT));

while 1:
    sock.sendto('MSM',(REMOTE_HOST , REMOTE_PORT))
    conn, addr = sock.recvfrom(1024)
    print('client addr: ', (addr,conn))
    time.delay(1);
