#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'andreas'

import threading
import pyaudio

from sphinxbase import *
from pocketsphinx import *

import pyprocessing as processing

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

def paint_smooth():
    processing.smooth()
    for i in range(10):
        processing.line(i*5+5,20,i*5+50,80)
    processing.run()

balls = [(20,20,2.5,3,10),(100,50,-3.5,-3,15)]

def setup():
    processing.size(400,400)
    processing.ellipseMode(processing.CENTER)
    processing.noStroke()

def draw():
    processing.fill(200,50)
    processing.rect(0,0,400,400)
    processing.fill(0)
    for i in range(len(balls)):
        x,y,dx,dy,r = balls[i]
        x += dx
        if processing.constrain(x,r,400-r) != x: dx = -dx
        y += dy
        if processing.constrain(y,r,400-r) != y: dy = -dy
        balls[i] = x,y,dx,dy,r
        processing.ellipse(x,y,r,r)

processing.run()

#if __name__ == '__main__':
    #paint_smooth()
    #processing = Processing()
    #processing.start()
    #run_pocketsphinx()