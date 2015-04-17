#!/usr/bin/python3

from dwCrypt import *
import sys
import socket
import threading

from time import sleep

daIP = '10.1.1.8'
daPort = 60000
serverConfig = '~/.darkWater'
fileLocation = '/home/jimmy/HOST/'

buff = 1024

sList = []


def rmvSocket(thsSocket, thsUser):
    global sList
    global usrName

    print('Socket closed for : ' + thsUser.usrName)
    sList.remove(thsSocket)
    thsSocket.destroy()
    del thsUser
    usrName = None


def srvLogin(thsUser):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((daIP, daPort))
    except Exception as e:
        print('Connection failed as ' + str(e))
        sys.exit()
    else:
        data = s.recv(buff).decode('utf-8')
        if not data == '001':
            print('Unknown error - server sent : ' + data)
            return None
        else:
            s.send(bytes(thsUser.usrName, 'utf-8'))
            data = s.recv(buff).decode('utf-8')
            if not data == '002':
                print('Unknown error - server sent : ' + data)
                return None
            else:
                s.send(bytes(thsUser.keyHash, 'utf-8'))
                data = s.recv(buff).decode('utf-8')
                if not data == '111':
                    print('Unknown error - server sent : ' + data)
                    return None
                else:
                    print('OK ' + data)
                    s.settimeout(300)
                    secSock = cryptSock(s, thsUser.key)
                    return secSock


def readLoop(secSock, buff, thsUser):
    global sList
    global fileLocation

    while secSock in sList:
        try:
            thsCMD = secSock.sRead(buff)
            if ':' in thsCMD:
                numCode = thsCMD.split(':')[0]
                pos = thsCMD.index(':')
                if not thsCMD[pos + 1] is None:
                    thsArg = thsCMD.split(':')[1]
            else:
                numCode = thsCMD
            if numCode.lower() == 'ping':
                secSock.sWrite('pong')
            elif numCode.lower() == '000':
                print('You have been booted')
                rmvSocket(secSock, thsUser)
            elif numCode.lower() == '200':
                try:
                    f = open(thsUser.keyFile, 'w')
                    f.write(thsArg)
                    f.close()
                    print('You have a new cryptoKey.')
                    secSock.sWrite('201')
                except:
                    print('Error adding new key')
            elif numCode == '202':
                print('Your remote key is : ' + thsArg)
            elif numCode == '300':
                secSock.sWrite('301')
                data = ' '
                while not data == '302':
                    data = secSock.sRead(buff)
                    if not data == '302':
                        print(data)
            elif numCode == '310':
                filSize = int(thsArg.split('^')[0])
                thsFile = thsArg.split('^')[1]
                if (thsFile is None) or (filSize is None):
                    secSock.sWrite('399')
                    print('Error getting incoming file data : ' + thsArg + ' : ' + numCode)
                else:
                    print('Incoming file transfer : ' + thsFile + ' : ' + str(filSize))
                    nf = open(fileLocation + thsFile, 'wb')
                    secSock.sWrite('311')
                    while not filSize == 0:
                        data = secSock.sRead(buff)
                        nf.write(data)
                        filSize = filSize - len(data)

                    nf.close()
            else:
                print(numCode)

        except socket.timeout:
            print('Server timeout.')
            rmvSocket(secSock, thsUser)


while True:
    usrName = input('Please input user name: ')
    authUser = thsUser(usrName, serverConfig)
    if authUser.keyHash is None:
        print('User ID is invalid')
        usrName = None
    else:
        secSock = srvLogin(authUser)
        if secSock is None:
            break

        else:
            sList.append(secSock)
            cTh = threading.Thread(target=readLoop, args=(secSock, buff, authUser))
            cTh.start()
            while secSock in sList:
                cmd = input(' #: ')
                try:
                    secSock.sWrite(cmd)
                except:
                    pass