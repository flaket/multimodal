__author__ = 'andreas'

import pyprocessing as p # This import immediately produces a graphics frame.
import Queue
from random import randint
from threading import Thread
from speech import speech_recognition
from serial_input import gesture_recognition

animation_q = Queue.Queue()

def setup():
    '''
    Invoked exactly once by pyprocessing.run().
    '''
    p.size(600,600,caption="Smart Home Multi-Modal Input")
    p.ellipseMode(p.CENTER)
    p.noStroke()

    p.background(200)
    p.fill(200,50)
    p.rect(0,0,600,600)

    start_thread(speech_recognition, (animation_q,))
    start_thread(gesture_recognition, (animation_q,))

def draw():
    '''Called by pyprocessing.run() on every frame update, ~60 times a second.
    If pyprocessing.noLoop() was called during setup,
    this is only called each time pyprocessing.redraw() is invoked.'''
    try:
        simple_multi_modal() # Case 2
        # dimming() # Case 3
        # lighting() # Case 3
        # machine_learning_multi_modal() # Case 3
    except Queue.Empty:
        pass # there was no new data from the input sources in the queue and nothing is drawn to the screen.

def simple_multi_modal():
    data = animation_q.get_nowait() # non-blocking check for items in animation_q.
    # If queue is empty a Queue.Empty exception is raised.
    source = data[0] # data read from queue is a tuple of strings: (source, text)
    text = data[1]
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
    pass

def lighting():
    pass

def machine_learning_multi_modal():
    pass

def start_thread(fn, args):
    worker = Thread(target=fn, args=args)
    worker.setDaemon(True)
    worker.start()

'''
def draw_arrow(x1, y1, x2, y2):
    p.stroke(255, 102, 0)
    p.line(x1, y1, x2, y2)
    p.pushMatrix()
    p.translate(x2, y2)
    a = p.atan2(x1-x2, y2-y1)
    p.rotate(a)
    p.line(0, 0, -20, -20)
    p.line(0, 0, 20, -20)
    p.popMatrix()

def draw_curve():
    p.noFill()
    p.stroke(255, 102, 0)
    p.curve(5, 26, 5, 26, 73, 24, 73, 61)
    p.stroke(0)
    p.curve(5, 26, 73, 24, 73, 61, 15, 65)
    p.stroke(255, 102, 0)
    p.curve(73, 24, 73, 61, 15, 65, 15, 65)
'''

p.run()