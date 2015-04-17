#!/usr/bin/python3

import os
from Crypto.Hash import SHA256



class fileGrab:

    def __init__(self):
        self.fileName = 'deb.iso'

        mFile = open(self.fileName + '.map', 'r')

