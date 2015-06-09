__author__ = 'andreas'

import pyprocessing as p # This import immediately produces a graphics frame.
import Queue
from random import randint
from threading import Thread
from serial_input import recognition
from speech import speech_recognition

animation_q = Queue.Queue()
lights_activated = False

def setup():
    '''
    Invoked exactly once by pyprocessing.run().
    '''
    p.size(600,600,caption="Smart Home Multi-Modal Input")
    p.ellipseMode(p.CENTER)
    p.noStroke()

    start_thread(recognition, ('gesture',animation_q,))
    start_thread(speech_recognition, (animation_q,))

def draw():
    '''Called by pyprocessing.run() on every frame update, ~60 times a second.
    If pyprocessing.noLoop() was called during setup,
    this is only called each time pyprocessing.redraw() is invoked.'''
    try:
        simple_multi_modal() # Case 2
        #dimming() # Case 3
        #lighting() # Case 3
    except Queue.Empty:
        pass # there was no new data from the input sources in the queue and nothing is drawn to the screen.

def simple_multi_modal():
    source, text = animation_q.get_nowait() # non-blocking check for items in animation_q.
    # If queue is empty a Queue.Empty exception is raised.
    if source == 'gesture':
        p.fill(0, 102, randint(50,150))
        p.textSize(48)
    elif source == 'speech':
        p.fill(102, randint(50,150), 0)
        p.textSize(32)
    else:
        pass
    p.text(text, randint(50,550), randint(50,550))

def dimming():
    global lights_activated
    source, text = animation_q.get_nowait() # non-blocking check for items in animation_q.
    # If queue is empty a Queue.Empty exception is raised.
    if source == 'dim' and lights_activated:
        d = int(float(text))
        if d < 200:
            r = d
            g = d
        else:
            r = 255
            g = 255
        b = d - 20
        p.background(200)
        p.fill(r,g,b)
        p.rect(0,0,600,600)
    elif text == 'LIGHTS':
        lights_activated = True
    else:
        pass

def lighting():
    source, text = animation_q.get_nowait() # non-blocking check for items in animation_q.
    # If queue is empty a Queue.Empty exception is raised.
    d = text.split(' ')
    (a, r, g, b) = list(map(int, d)) # max values: 37889
    if source == 'lighting':
        p.fill(a,a,a)
        p.rect(200,100,200,100)

        p.fill(r,0,0,a)
        p.rect(100,300,100,100)

        p.fill(0,g,0,a)
        p.rect(250,300,100,100)

        p.fill(0,0,b,a)
        p.rect(400,300,100,100)
    else:
        pass

def start_thread(fn, args):
    worker = Thread(target=fn, args=args)
    worker.setDaemon(True)
    worker.start()

p.run()