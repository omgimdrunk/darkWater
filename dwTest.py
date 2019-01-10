#!/usr/bin/python3


import os
from Crypto.Hash import SHA256


class fileSync:

    def __init__(self):
        MB = (1024 * 1024)
        self.buff = (MB)
        self.fileChunk = (5 * MB)
        self.fileDir = '/home/drunk/Documents/files/'
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


x = fileSync()
x.makeMap()
