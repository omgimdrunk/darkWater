#!/usr/bin/python3

from dwCrypt import *
import socket
import threading
import sys
from dwUtils import *

def newSocket(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(1)
    return s

class serverSettings:

    def __init__(self, settingsFile=None):

        self.ip = None
        self.port = None
        self.keyLocation = None
        self.fileLocation = None
        self.filemapLocation = None
        self.buff = None
        self.sList = []

        if settingsFile is None:
            sFile = '/etc/darkWater/darkWater.conf'
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
                        self.keyLocation = value
                    elif item == 'file_location':
                        self.fileLocation = value
                    elif item == 'file_mapping':
                        self.fileLocation = value
                    elif item == 'server_mem_buffer':
                        self.buff = value
        except:
            print('Bad config file. : ' + sFile)
            f.close()
        else:
            f.close()

        def rmvSocket(self, thsSocket, thsUser):
            print('Socket closed for : ' + thsUser.usrName)
            self.sList.remove(thsSocket)
            thsSocket.destroy()
            del thsUser


class serverCMD:
    def __init__(self, serverSettings):

        self.srvSettings = serverSettings



            def fileList(thsSocket):
                fList = fileSearch(self.srvSettings.fileLocation, True)
                thsSocket.sWrite('300')
                r = thsSocket.sRead(self.srvSettings.buff)
                if not r == '301':
                    break
                else:
                    for i in fList:
                        thsSocket.sWrite(i)
                thsSocket.sWrite('')

            def newKey(thsSocket, thsUser):
                nk = newKey()
                thsSocket.sWrite('200:' + nk)
                ok = thsSocket.sRead(self.srvSettings.buff)
                if '201' in ok:
                    f = open(thsUser.keyFile, 'w')
                    f.write(nk)
                    f.close()
                    print('New key added for ' + thsUser.usrName)
                    serverSettings.rmvSocket(thsSocket, thsUser)

            def getFile(thsSocket, thsArg):
                thsBuff = self.srvSettings.buff
                thsFile = fileSearch(thsArg.split('^')[0], self.srvSettings.file_mapping)
                if thsFile is None:
                    thsSocket.sWrite('399')
                else:
                    thsChunk = thsArg.split('^')[1]
                    if thsChunk == '0':
                        fileSze
                        tf = open(thsFile, 'r')
                        while not fileSize == 0:
                            print(str(fileSize))
                            if fileSize < thsBuff:
                                thsBuff = fileSize
                            chunk = tf.read(thsBuff)
                            thsSocket.sWrite(chunk)
                            fileSize = fileSize - thsBuff
                    ok = thsSocket.sRead(buff)
                    if ok == '399':
                        print('Err on client side')
                    elif ok == '311':


                        tf.close()


def srvLoop(srvConfig, thsSocket):
    global fileLocation

    secSock, thsUser = serverCMD.usrVerify(thsSocket)
    if None in {secSock, thsUser}:
        thsSocket.close()
        del secSock
        del thsUser
    else:
        srvConfig.sList.extend(secSock)

        while secSock in srvConfig.sList:
            try:
                thsCMD = thsSocket.sRead(buff)
            except socket.timeout:
                print('Connection timeout for : ' + thsUser.usrName)
                rmvSocket(thsSocket, thsUser)
            except Exception as e:
                print('Error for ' + thsUser.usrName + ' : ' + str(e))
                srvConfig.rmvSocket(secSock, thsUser)

            if thsCMD is None:
                rmvSocket(thsSocket, thsUser)
            else:
                numCode, thsArg = getCMD(thsCMD)

                if numCode == 'list':
                    serverCMD.fileList(secSock)
                elif numCode == 'newkey':
                    serverCMD.newkey(secSock, thsUser)
                elif numCode == 'getfile':
                    serverCMD.getfile(secSock, thsArg)

            else:
                print(thsCMD)

# Main kick off loop - needs Queue passing to shutdown clean

try:
    srvSet = sys.argv[1]
except:
    serverConfig = serverSettings()
else:
    serverConfig = serverSettings(srvSet)

scmd = serverCMD(serverConfig)

s = newSocket(serverConfig.ip, serverConfig.port)
while 1:
    srvSock, add = s.accept()
    usrTH = threading.Thread(target=srvLoop, args=(scmd, srvSock))
    usrTH.start()