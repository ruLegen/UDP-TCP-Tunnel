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
    return parser.parse_args()



