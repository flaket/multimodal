#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'andreas'

from multiprocessing import Process, Queue
import serial

time_out = 3
baud_rate = 9600
port = '/dev/cu.usbmodem1411'

def connect_serial():
    ser = serial.Serial(port, baud_rate, timeout=time_out)
    buf = []
    while True:
        byte = ser.read()
        if byte == '\n':
            buf = handle_gesture(buf)
        elif byte == '\r':
            pass
        else:
            buf.append(byte)
    ser.close()

def handle_gesture(buf):
    global queue
    print(''.join(buf))
    if buf == 'DOWN':
        color = 255
        queue.put(color)
    elif buf == 'RIGHT':
        color = 150
        queue.put(color)
    elif buf == 'UP':
        color = 100
        queue.put(color)
    elif buf == 'LEFT':
        color = 50
        queue.put(color)
    else:
        pass
    return []

def load_graphics():
    pr = Process(target=processing.run, args=())
    pr.start()

def load_gestures():
    s = Process(target=connect_serial, args=())
    s.start()

import pyprocessing as processing

balls = [(20,20,2.5,3,10),(100,50,-3.5,-3,15)]
color = 0

def read_from_queue():
    global color, queue
    if not queue.empty():
        return queue.get_nowait()
    else:
        return color

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
    #c = read_from_queue()
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
    queue = Queue()
    processing.run()

    # 1. Start processing graphics
    # 2. Create Queue
    # 3. Start up new threads/processes to handle each input channel.