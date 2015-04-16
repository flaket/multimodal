#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'andreas'

import pyprocessing as processing # This import immediately produces a graphics frame.
from random import randint
from Queue import Queue
from threading import Thread
import serial

time_out = 3
baud_rate = 9600
port = '/dev/cu.usbmodem1411'
#ser = serial.Serial(port, baud_rate, timeout=time_out)

balls = [(20,20,2.5,3,10),(100,50,-3.5,-3,15)]
color = 0
q = Queue()

def fill_queue(q):
    for i in range(100):
        q.put(randint(0,255), False)

def setup():
    '''Invoked exactly once by processing.run().'''
    #Start up new threads/processes to handle each input channel.
    worker = Thread(target=fill_queue, args=(q,))
    worker.setDaemon(True)
    worker.start()

    processing.size(600,600,caption="Smart Home Multi-Modal Input")
    processing.ellipseMode(processing.CENTER)
    processing.noStroke()
    processing.noLoop()

def draw():
    '''Called by processing.run() on every frame update, ~60 times a second.
    If noLoop() was called during setup, this is only called on redraw().'''
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
        color = q.get()
        q.task_done()
        processing.redraw()
    if processing.key.code == 65363: # Right arrow
        color = q.get()
        q.task_done()
        processing.redraw()
    if processing.key.code == 65362: # Up arrow
        color = q.get()
        q.task_done()
        processing.redraw()
    if processing.key.code == 65361: # Left arrow
        color = q.get()
        q.task_done()
        processing.redraw()

if __name__ == '__main__':
    processing.run()