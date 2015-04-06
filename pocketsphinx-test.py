#!/usr/bin/env python2
from pocketsphinx import *
import pyaudio
import sys

dic = 'TAR2860/2860.dic'
lm= 'TAR2860/2860.lm'

config = Decoder.default_config()
config.set_string('-lm', lm)
config.set_string('-dict', dic)

decoder = Decoder(config)

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()
in_speech_bf = True
decoder.start_utt('')
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
        try:
            if  decoder.hyp().hypstr != '':
                print 'Partial decoding result:', decoder.hyp().hypstr
        except AttributeError:
            pass
        if decoder.get_in_speech():
            sys.stdout.write('.')
            sys.stdout.flush()
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                try:
                    if  decoder.hyp().hypstr != '':
                        print 'Stream decoding result:', decoder.hyp().hypstr
                except AttributeError:
                    pass
                decoder.start_utt('')
    else:
        break
decoder.end_utt()
print 'An Error occured:', decoder.hyp().hypstr

'''
hmm = 'pocketsphinx/model/en-us/en-us/'
dic = 'TAR2860/2860.dic'
lm= 'TAR2860/2860.lm'

def decodeSpeech(hmm,lm,dic,wavfile):
    config = ps.Decoder.default_config()
    config.set_string('-hmm', hmm)
    config.set_string('-lm', lm)
    config.set_string('-dict', dic)
    config.set_string('-logfn', '/dev/null')
    speechRec = ps.Decoder(config)
    #speechRec = ps.Decoder(hmm = hmmd, lm = lmdir, dict = dictp)
    wavFile = file(wavfile,'rb')
    wavFile.seek(44)
    speechRec.decode_raw(wavFile)
    result = speechRec.get_hyp()
    return result[0]

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5

for x in range(1):
    fn = "o" + str(x) + ".wav";
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("* recording")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(fn, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    wavfile = fn
    recognised = decodeSpeech(hmm,lm,dic,wavfile)
    print recognised
    cm = 'espeak ' + recognised
    os.system(cm)
'''