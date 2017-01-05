import argparse

def getargs():
    parser = argparse.ArgumentParser(description='Some text');
    parser.add_argument('--sourceport','-sp',
                        action='store',
                        type=int,
                        help='Source port wich from will be enstabilish connect. Default is 9876',
                        default=9876)
    parser.add_argument('--remoteport','-rp',
                        type=int,
                        action='store',
                        help='Remotr port to enstabilish connect. Default is 9876',
                        default=9876)
    parser.add_argument('--sourcehost','-sh',
                        action='store',
                        help='Host wich will trying connect. Default is 0.0.0.0',
                        default='0.0.0.0')
    parser.add_argument('--remotehost','-rh',
                        action='store',
                        help='Remote host')
    parser.add_argument('--username','-u',
                        action='store',
                        help='Your name',
                        default='User')
    parser.add_argument('--remoteusername', '-ru',
                        action='store',
                        help='Remote username to connect ',
                        )
    parser.add_argument('--directconnection', '-d',
                        action='store_true',
                        help='Remote username to connect ',
                        )
    parser.add_argument('--signalserver', '-ss',
                        action='store',
                        help='Signal server IP or Domain',
                        )

    return parser.parse_args()



