
from socket import *

############################
############################
##                        ##
##  Network-Related Code  ##
##                        ##
############################
############################

# Note: In all of the following functions, conn is a socket object


##############################
# recvall equivalent to sendall

def recvall(conn, msgLength):
    msg = b''
    while len(msg) < msgLength:
        retVal = conn.recv(msgLength - len(msg))
        msg += retVal
        if len(retVal) == 0:
            break    
    return msg


def getLocalIPAddress():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
