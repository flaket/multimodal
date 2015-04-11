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
                else:
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


balls = [(20,20,2.5,3,10),(100,50,-3.5,-3,15)]
color = 0

def setup():
    '''
    This function is invoked exactly once by processing.run().
    '''
    processing.size(400,400,caption="Smart Home multi-modal input")
    processing.ellipseMode(processing.CENTER)
    processing.noStroke()

def draw():
    '''
    This function is called by processing.run() on every frame update, ~60 times a second.
    '''
    processing.fill(200,50)
    processing.rect(0,0,400,400)
    processing.fill(color)
    for i in range(len(balls)):
        x,y,dx,dy,r = balls[i]
        x += dx
        if processing.constrain(x,r,400-r) != x: dx = -dx
        y += dy
        if processing.constrain(y,r,400-r) != y: dy = -dy
        balls[i] = x,y,dx,dy,r
        processing.ellipse(x,y,r,r)

def keyPressed():
    global color
    if processing.key.code == 65364: # Down arrow
        color = 255
    if processing.key.code == 65363: # Right arrow
        color = 150
    if processing.key.code == 65362: # Up arrow
        color = 100
    if processing.key.code == 65361: # Left arrow
        color = 50


if __name__ == '__main__':
    processing.run()
    #run_pocketsphinx()