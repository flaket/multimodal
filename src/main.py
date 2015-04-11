#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'andreas'

import threading
import pyaudio

from pocketsphinx import *
from sphinxbase import *

hmm = 'cmusphinx-en-us-5.2/'
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

    def run(self):
        print("Pocketsphinx running..")
        self.running = True
        decoder = Decoder(self.configure())
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        stream.start_stream()
        speaking = True
        decoder.start_utt()

        while self.running:
            buf = stream.read(1024)
            if buf:
                decoder.process_raw(buf, False, False)
                try:
                    # If partial results:
                    if decoder.hyp().hypstr != '':
                        hypstr = decoder.hyp().hypstr
                        print('Partial decoding result: ' + hypstr)
                except AttributeError:
                    pass
                # If the speech has ended:
                if decoder.get_in_speech() != speaking:
                    speaking = decoder.get_in_speech()
                    # If the speech has ended:
                    if not speaking:
                        decoder.end_utt()
                        try:
                            if decoder.hyp().hypstr != '':
                                decoded_string = decoder.hyp().hypstr
                                print('Stream decoding result: ' + decoded_string)
                        except AttributeError:
                            pass
                        decoder.start_utt() # Tell the decoder to prepare for a new sequence of words.
                        #print('Stopped listening.')
                else:
                    #print('Started listening..')
                    pass
            else:
                break
        decoder.end_utt()
        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop(self):
        self.running = False

def run_pocketsphinx():
    try:
        print("Starting script..")
        ps = PocketSphinx()
        ps.start()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print('Keyboard interrupt.')
        ps.stop()

if __name__ == '__main__':
    run_pocketsphinx()