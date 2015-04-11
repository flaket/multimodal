#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'andreas'

import threading

from pocketsphinx import *
from sphinxbase import *

hmm = 'cmusphinx.-en-us-5.2/'
lm = 'TAR2860/2860.lm'
dic = 'TAR2860/2860.dic'

class PocketSphinx(threading.Thread):
    '''
    Pocketsphinx class.
    '''
    def __init__(self):
        threading.Thread.__init__(self)

    def configure(self):
        config = Decoder.default_config()
        config.set_string('-hmm', hmm)
        config.set_string('-lm', lm)
        config.set_string('-dict', dic)
        return config



if __name__ == '__main__':
    print("Starting script..")