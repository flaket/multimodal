__author__ = 'andreas'

import pyaudio
from sphinxbase import *
from pocketsphinx import *

def config():
    hmm = 'cmusphinx-en-us-5.2/'
    lm = 'TAR2860/2860.lm'
    dic = 'TAR2860/2860.dic'
    config = Decoder.default_config()
    config.set_string('-hmm', hmm)
    config.set_string('-lm', lm)
    config.set_string('-dict', dic)
    return config

def speech_recognition(q):
    decoder = Decoder(config())
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()
    speaking = True
    decoder.start_utt()
    running = True
    while running:
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
                            q.put(('speech', decoded_string), block=True, timeout=1)
                            # Temporary use of 'DOOR' as a quit-keyword:
                            #if decoded_string == 'DOOR':
                            #    running = False
                    except AttributeError:
                        pass
                    decoder.start_utt() # Tell the decoder to prepare for a new sequence of words.
        else:
            break
    decoder.end_utt()
    stream.stop_stream()
    stream.close()
    p.terminate()