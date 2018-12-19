#!/usr/bin/python3

import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import string
import random
from dwUtils import *


def getKey(userID, keyLocation):
    for roots, dirs, files in os.walk(keyLocation):
        for f in files:
            if userID + '.key' == f:
                keyFile = os.path.join(roots, f)
                try:
                    rFile = open(keyFile, 'r', encoding='utf-8')
                    key = rFile.readlines()[0]
                    rFile.close()
                    keyHash = SHA256.new(bytes(key, 'utf-8')).hexdigest()
                except:
                    return None
                else:
                    return (key, keyHash, keyFile)


class dwClientCTRL:

    def __init__(self, usrSocket, dwSettings, usrID, usrIP, usrKey, usrKeyFile, usrKeyHash):

        self.cmdSock = usrSocket
        self.dwConfig = dwSettings
        self.id = usrID
        self.ip = usrIP
        self.key = usrKey
        self.keyFile = usrKeyFile
        self.keyHash = usrKeyHash
        self.cipher = AES.new(self.key)

    def destroy(self):
        try:
            self.sWrite('000')
        except:
            pass
        finally:
            self.sock.close()

    def strPad(chunk):
        while len(chunk) % 16 != 0:
            chunk += ' '
        return chunk

    def encrypt(self, data):
        data = self.cipher.encrypt(self.strPad(data))
        return(data)

    def decrypt(self, data):
        try:
            data = strTrim(self.cipher.decrypt(data).decode('utf-8'))
        except UnicodeDecodeError:
            data = self.cipher.decrypt(data)
            return data
        return data

    def sRead(self, buff):
        data = self.cryptoSock.recv(buff)
        if len(data) == 0:
            return None
        else:
            data = self.decrypt(data)
            return data

    def sWrite(self, data):
        self.sock.send(self.encrypt(data))


def newKey(finCount=None):
    if finCount is None:
        finCount = 32
    finKey = ''
    daPool = []
    xtraChar = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']

    for i in list(string.ascii_lowercase):
        daPool.extend(i)

    for i in list(string.ascii_uppercase):
        daPool.extend(i)

    for i in range(10):
        daPool.extend(str(i))

    for i in range(len(xtraChar)):
        daPool.extend(xtraChar[i])

    for i in range(finCount):
        finKey = finKey + daPool[random.randrange(0, len(daPool), 1)]
    del daPool
    return finKey


class fileMap:

    def __init__(self):
        MB = (1024 * 1024)
        self.buff = (MB)
        self.fileChunk = (5 * MB)
        self.fileDir = '/home/omgimdrunk/Documents/files/'
        self.dwFile = 'deb.iso'
        self.thsFile = self.fileDir + self.dwFile
        self.fs = os.path.getsize(self.thsFile)
        self.numFulChunks = round(self.fs / self.fileChunk)  # How many full chunks are in file

    def makeMap(self):

        totalChunkBytes = self.numFulChunks * self.fileChunk  # Total bytes in full chunks
        lastChunk = self.fs - totalChunkBytes  # Remainder of bytes that does not equal 25 megs

        newFile = open(self.thsFile, 'rb')
        saveMap = open(self.dwFile + '.map', 'wb')
        saveMap.write(bytes('file_name:' + self.dwFile + '\n', 'utf-8'))
        saveMap.write(bytes('file_size:' + str(self.fs) + '\n', 'utf-8'))
        saveMap.write(bytes('file_chunks:' + str(self.numFulChunks) + '\n', 'utf-8'))
        saveMap.write(bytes('last_chunk:' + str(lastChunk) + '\n', 'utf-8'))
        print('Mapping ' + self.thsFile)
        bufCount = 0
        for i in range(self.numFulChunks):
            cHash = SHA256.new()
            while not bufCount == self.fileChunk:
                bufCount = bufCount + self.buff
                bitGrab = newFile.read(self.buff)
                cHash.update(bitGrab)
            bufCount = 0
            chunkHash = str(cHash.digest())
            saveMap.write(bytes(str(i + 1) + ':' + chunkHash + '\n', 'utf-8'))

        assBytes = lastChunk
        while not assBytes == 0:
            if assBytes < self.buff:
                bitGrab = newFile.read(assBytes)
            else:
                bitGrab = newFile.read(self.buff)
            cHash.update(bitGrab)
            assBytes = assBytes - len(bitGrab)
            chunkHash = str(cHash.digest())
            saveMap.write(bytes('lc:' + chunkHash + '\n', 'utf-8'))

        newFile.close()
        saveMap.close()

    def getChunk(self, numChunk):
        pass
