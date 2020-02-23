import sys
import argparse

parser = argparse.ArgumentParser(
    description="Slow and low attack tools by Quentin and Stan"
)
def printHelp():
    pass

def initParser():
    parser.add_argument("-a","--addr",type=str,help="Host to perform attack, default localhost",)
    parser.add_argument("-p","--port",default=80,type=int,help="Port of the server, default = 80")
    parser.add_argument("-s","--sockets",default=1000,help="Max socket use",type=int)
    parser.add_argument("-d", "--debug", dest="debug", action="store_true", help="Debug log")
def parsArg():
    initParser()
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit()
    arg = parser.parse_args()
    if not arg.addr:
        print("Host Require")
        parser.print_help()
        sys.exit()
    return parser.parse_args()


