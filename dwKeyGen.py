#!/usr/bin/python3

import random
import string
import datetime


finKey = ''
finCount = 32
usrName = None

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


while usrName is None:
    usrName = input(' #: ')

wFile = open(usrName + '.key', 'wb')
wFile.write(bytes(finKey, 'UTF-8'))
wFile.close