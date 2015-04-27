__author__ = 'andreas'

import serial_input
import csv
import matplotlib.pyplot as plt
import numpy as np
import random as r
from sklearn import preprocessing, svm, cross_validation
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier, BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
import Queue
from threading import Thread
import time

#X = np.loadtxt('data/500.csv', delimiter=',')
#X = preprocessing.scale(X)
#y = []
#samples_per_label = 50
#loops = 10

time_out = 3
baud_rate = 9600
data = []
samples = 3
output_filename = 'test.csv'
serial_q = Queue.Queue()

def create_labels():
    for i in range(samples_per_label):
        y.append("far")
    for i in range(samples_per_label):
        y.append("near")
    for i in range(samples_per_label):
        y.append("up-swipe")
    for i in range(samples_per_label):
        y.append("up-flick")
    for i in range(samples_per_label):
        y.append("down-swipe")
    for i in range(samples_per_label):
        y.append("down-flick")
    for i in range(samples_per_label):
        y.append("left-swipe")
    for i in range(samples_per_label):
        y.append("left-flick")
    for i in range(samples_per_label):
        y.append("right-swipe")
    for i in range(samples_per_label):
        y.append("rigth-flick")

def classify():
    if len(X) == len(y):
        results = []
        svc_lin_score = 0
        svc_score = 0
        logisticRegression_score = 0

        for i in range(loops):
            seed = r.randint(0, len(X))
            X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25, random_state=seed)

            svc_lin = svm.LinearSVC().fit(X_train, y_train)
            svc_lin_score = svc_lin_score + svc_lin.score(X_test, y_test)

            svc = svm.SVC(kernel='linear').fit(X_train, y_train)
            svc_score = svc_score + svc.score(X_test, y_test)

            logisticRegression = LogisticRegression().fit(X_train, y_train)
            logisticRegression_score = logisticRegression_score + logisticRegression.score(X_test, y_test)


        results.append([str(svc_lin_score / loops), "Linear-SVC"])
        results.append([str(svc_score / loops), "SVC"])
        results.append([str(logisticRegression_score / loops), "LogisticRegression"])

        results.sort(reverse=True)
        return results
    return "Mismatch in #data samples in data set X and #labels in y"

def trim_data(d, n=512, m=255):
    """
    Partitions an input array of data into a feature vector of size n:
    an n-sized array with normalized values with regard to m.
    If the input data is of a shorter length than n the returned array will be sparse.
    A larger input array will produce a denser result.
    :param d: Input array of data.
    :param n: Size of result array.
    :param m: Normalizing factor (maximum possible data value).
    :return: Array of size param n with input param data distributed over the array
             and normalized with regard to param m.
    """
    l = len(d)
    histogram = [0] * n
    s = int(l / n)
    if s == 0:
        s = int(1. / (float(l) / float(n)))
        for i, x in enumerate(d):
            histogram[i*s] = x/m
    else:
        for i in range(0, n):
            histogram[i] = sum(d[i*s:(i+1)*s])/(m*s)
    return histogram

def test_trim_data():
    assert [1., 1., 1.] == trim_data([1., 1., 1.], n=3, m=1)
    assert [1., 0., 0.] == trim_data([1.], n=3, m=1)
    assert [1., 0., 0., 1., 0., 0., 1., 0., 0., 0.] == trim_data([1., 1., 1.], n=10, m=1)
    assert [0.5, 0.5, 0.5] == trim_data([1., 1., 1.], n=3, m=2)
    assert [0.1, 0.1, 0.1] == trim_data([1., 1., 1.], n=3, m=10)
    assert [.2, 0., 0., .2, 0., 0., .2, 0., 0., 0.] == trim_data([1., 1., 1.], n=10, m=5)
    assert [1., 1., 1.] == trim_data([1., 1., 1., 1., 1., 1.], n=3, m=1)
    assert [.5, .5, .5] == trim_data([.25, .75, .25, .75, .25, .75], n=3, m=1)

def serial_data_to_q(id, port, q):
    ser = serial_input.Serial(port, baud_rate, timeout=time_out)
    buf = []
    while True:
        c = ser.read()
        if c == '\n':
            result = ''.join(buf)
            q.put((id,result), block=True, timeout=1)
            buf = []
        elif c == '\r':
            pass
        else:
            buf.append(c)

def listen_for_gestures():
    # Spin up a thread for each serial port with a common queue for them to write to.
    start_thread(serial_data_to_q, args=(1, '/dev/cu.usbmodem1a1211', serial_q))
    start_thread(serial_data_to_q, args=(2, '/dev/cu.usbmodem1a1231', serial_q))
    start_thread(serial_data_to_q, args=(3, '/dev/cu.usbmodem1a1241', serial_q))
    start_thread(serial_data_to_q, args=(4, '/dev/cu.usbserial-A6026OJT', serial_q))

    total_data = []
    for i in range(0, samples):
        data = []
        one = []
        two = []
        three = []
        four = []
        print("Listening for gesture for " + str(time_out) + " seconds..")
        time.sleep(time_out)
         # Look for new data in the queue. Break and process data when queue is empty.
        while True:
            try:
                data.append(serial_q.get_nowait())
            except Queue.Empty:
                break
        # sort the data from the four sources:
        for d in data:
            if d[0] == 1:
                # sort data from the four photo diodes:
                # ..
                one.extend(process_data(d[1]))
            elif d[0] == 2:
                two.extend(process_data(d[1]))
            elif d[0] == 3:
                three.extend(process_data(d[1]))
            elif d[0] == 4:
                four.extend(process_data(d[1]))
            else:
                pass
        three.extend(four)
        two.extend(three)
        one.extend(two)
        if len(one) > 0:
            one = map(float, one)
            one = trim_data(one)
            total_data.append(one)

    save_data(total_data)

def process_data(raw):
    d = raw.decode()
    d = d.split(' ')
    del d[-1]
    d = list(map(int, d))
    return d

def trim_data(d, n=512, m=255):
    """
    Partitions an input array of data into a feature vector of size n:
    an n-sized array with normalized values with regard to m.
    If the input data is of a shorter length than n the returned array will be sparse.
    A larger input array will produce a denser result.
    :param d: Input array of data.
    :param n: Size of result array.
    :param m: Normalizing factor (maximum possible data value).
    :return: Array of size param n with input param data distributed over the array
             and normalized with regard to param m.
    """
    l = len(d)
    histogram = [0] * n
    s = int(l / n)
    if s == 0:
        s = int(1. / (float(l) / float(n)))
        for i, x in enumerate(d):
            histogram[i*s] = x/m
    else:
        for i in range(0, n):
            histogram[i] = sum(d[i*s:(i+1)*s])/(m*s)
    return histogram

def online_classify(d):
    prediction = svc.predict(d)
    print(prediction)

def store_to_memory(sensor1, n):
    data.append(sensor1)
    print("Stored result to memory: {0}".format(str(n + 1)))

def save_data(data):
    with open(output_filename, 'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(data)
    print("Stored " + str(len(data)) + " data samples to file: " + output_filename)

def train_classifier():
    create_labels()
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25)
    global svc
    svc = svm.SVC(kernel='linear').fit(X_train, y_train)

def start_thread(fn, args):
    worker = Thread(target=fn, args=args)
    worker.setDaemon(True)
    worker.start()

if __name__ == '__main__':
    #test_trim_data()
    #train_classifier()
    listen_for_gestures()
    data1 = np.loadtxt('test.csv', delimiter=',')
    print(len(data1))
    for line in data1:
        print("** " + str(line))