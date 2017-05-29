import argparse
import sys
import time

args = sys.argv[1]
if args.startswith("tunnel://"):
    del sys.argv[1]
    if args[len(args)-1] == "/":
	    args=args[:len(args)-1]

    if "%20" in args:
        sys.argv = sys.argv + args.split("tunnel://")[1].split("%20")
    else:
        sys.argv = sys.argv + args.split("tunnel://")[1].split(" ")

print(sys.argv)

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
                        default=False)
    parser.add_argument('--remoteusername', '-ru',
                        action='store',
                        help='Remote username to connect ',
                        default=False
                        )
    parser.add_argument('--directconnection', '-d',
                        action='store_true',
                        help='Remote username to connect ',
                        )
    parser.add_argument('--signalserver', '-ss',
                        action='store',
                        help='Signal server IP or Domain',
                        default=False
                        )

    parser.add_argument('--forcename', '-f',
                        action='store',
                        help='Use the registered name',
                        default=False
                        )
    parser.add_argument('--server', '-s',
                        action='store',
                        help='Set You as Server',
                        default=False
                        )
    return parser.parse_args(sys.argv[1:])



