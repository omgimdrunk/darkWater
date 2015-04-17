#!/usr/bin/python3
'''
version 1.2 [test] - no server, no main node. just FON objects in flux
Verify that return socket can be opened,

'''

from dwUtils import *
from dwCrypt import *
from time import sleep


class serverSettings:

    def __init__(self, settingsFile=None):

        self.ip = None
        self.port = None
        self.keyLocation = None
        self.fileLocation = None
        self.fileMapLocation = None
        self.buff = None
        self.sList = []

        if settingsFile is None:
            sFile = '/home/jimmy/darkWater/darkWater.conf'
        else:
            sFile = settingsFile
        try:
            with open(sFile) as f:
                for line in f:
                    line = line.lower().replace(' ', '').replace('\n', '')
                    item = line.split(':')[0]
                    value = line.split(':')[1]
                    if item == 'ip':
                        self.ip = value
                    elif item == 'port':
                        self.port = int(value)
                    elif item == 'key_location':
                        self.keyLocation = cleanPath(value)
                    elif item == 'file_location':
                        self.fileLocation = cleanPath(value)
                    elif item == 'file_mapping':
                        self.fileMapLocation = cleanPath(value)
                    elif item == 'server_mem_buffer':
                        self.buff = value
        except:
            print('Bad config file. : ' + sFile)
            f.close()
        else:
            f.close()

def nodeAdd(newNode, srvSettings):
    print('Adding new node for ' + getCMS)
    thsSList = srvSettings.sList
    nkf = open(srvSettings.keyLocation + newNode + '.key', 'w')
    nkf.write(newKey(32))
    nkf.close()



def usrVerify(dwSettings, thsSocket, usrIP):
    thsSocket.send(bytes('001', 'utf-8'))
    cmd = thsSocket.read()
    if getCMD(cmd, 1) == '102':
        usrID = getCMD(cmd, 2)
        usrKey, usrKeyHash, usrKeyFile = getKey(usrID, dwSettings.keyLocation)
        if (usrKey is None) or (usrKeyHash is None):
            sys.exit('Bad auth from ' + usrIP)
        else:
            thsSocket.write('103'),
            cmd = thsSocket.read()
            if getCMD(cmd, 1) == '104':
                cliHash = getCMD(cmd, 2)
                if not cliHash == usrKeyHash:
                    sys.exit('Bad auth from ' + usrIP)
                else:
                    thsSocket.write('105')
                    cmd = thsSocket.read()
                    if getCMD(cmd, 1) == ('106'):
                        uniQid = getCMD(cmd, 2)
                        thsSocket.write('111')
                        thsUser = dwClientCTRL(thsSocket, dwSettings, usrID, usrIP, usrKey,
                                                                usrKeyFile, usrKeyHash)
                        dwSettings.sList.extend(thsUser + ':' + thsSocket)


def usrHandShake()


def rmvSocket(self, thsSocket, thsUser):
    print('Socket closed for : ' + thsUser.usrName)
    self.sList.remove(thsSocket)
    thsSocket.destroy()
    del thsUser


def usrInput(srvSettings):
    while 1:
        cmd = getCMD(data, 1)
        argv = getCMD(data, 2)
        data = input('::# ').lower()
        if cmd == 'newnode':
            nodeADD(argv, srvSettings)


try:
    srvSet = sys.argv[1]
except:
    dwConfig = dwSettings()
else:
    serverConfig = serverSettings(srvSet)

    #  Add choice to Listen or connect

dwSettings = serverCMD(serverConfig)

s = masterSocket(serverConfig.ip, serverConfig.port, serverConfig.buff)
ds = dataSocket(serverConfig.ip, serverComfig.dport
while 1:
    srvSock, addr = s.accept()
    usrTH = threading.Thread(target=usrVerify, args=(dwSettings, srvSock, addr))
    usrTH.start()
    inputTH = threading.Thread(target=usrInput, args=(dwSettings,))
    inputTH.start()


