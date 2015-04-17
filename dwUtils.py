'''
darkWater Utils
just some junk to make processing data easier
'''

import os
import random
import string
import socket


class masterSocket:

    def new(self, ip, port, buff):
        self.ip = ip
        self.port = port
        self.sock = None
        self.buff = buff

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((self.ip, self.port))
            s.listen(1)
        except Exception as e:
            print(str(e))

        else:
            self.sock = s
            return self.sock

    def write(self, data):
        self.sock.send(bytes(data), 'utf-8')

    def read(self):
        return self.sock.recv(self.buff).decode('utf-8')

    def close(self):
        self.sock.close()

    def accept(self):
        return self.sock.accept()

class syncSock:

    def __init__(self, ip, port, buff):
        self.ip = ip
        self.port = port
        self.sock = None
        self.buff = buff

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, self.port))
        except:
            return False
        else:
            self.sock = s

    def write(self, data):
        self.sock.send(bytes(data), 'utf-8')

    def read(self):
        return self.sock.recv(self.buff).decode('utf-8')

    def close(self):
        self.sock.close


def cleanPath(thsPath):
    if not thsPath[len(thsPath) - 1] == '/':
        thsPath = thsPath + '/'
    if thsPath[0] == '~':
        thsPath = os.path.expanduser('~') + thsPath[1:]
    return thsPath


def fileSearch(thsFile, thsLocation):
    if thsFile is None:
        fList = ''
        for roots, dirs, files in os.walk(thsLocation):
            for f in files:
                fList = fList + f + ':'
            return fList
    elif not thsFile is None:
        for roots, dirs, files in os.walk(thsLocation):
            for f in files:
                if f == thsFile:
                    return os.path.join(roots, f)
        return None
    else:
        print('Err in fileSeach - dwUtils')
        return None


def byteStr2Int(byteStr):
    alpha = []
    kb = 1024
    mb = kb * kb
    gb = mb * kb

    for i in string.ascii_lower():
        alpha.extend(i)
    for i in byteStr:
        if byteStr[i] in alpha:
            num = int(byteStr[:i - 1])
            if byteStr[i] == 'k':
                return(int(num * kb))
            elif byteStr[i] == 'm':
                return(int(num * mb))
            elif byteStr[i] == 'g':
                return(int(num * gb))
    return None


def swirl():
    return chr(random. randrange(5163, 5189, 1))


def strTrim(thsString):
    l = len(thsString)
    thsString = thsString.replace('\n', '')
    while thsString[l - 1] == ' ':
        l -= 1
    return thsString[0:l]


def getCMD(thsString, cmdPos):
    x = []
    x.extend(thsString.split(':'))

    if cmdPos == 0:
        xList = ''
        for i in x:
            i = strTrim(i)
            if not i == '':
                xList = xList + i
        return xList
    else:
        try:
            x = strTrim(x[cmdPos - 1])
        except:
            return None
        if x == '':
            return None
        else:
            return x