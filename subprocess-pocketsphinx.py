#!/usr/bin/env python2
import subprocess
from subprocess import Popen, PIPE
'''
p = Popen(['pocketsphinx_continuous', '-inmic', 'yes', '-lm', 'TAR2860/2860.lm', '-dict', 'TAR2860/2860.dic'],
          stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate()
print(output, err)

while True:
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    rc = p.returncode
    print("Output: " + output)
    print("Err: " + err)
    print("Returncode: " + rc)
'''
#print(subprocess.check_output(["pocketsphinx_continuous", "-inmic", "yes", "-lm", "TAR2860/2860.lm", "-dict", "TAR2860/2860.dic"]))

subprocess.call(["pocketsphinx_continuous", "-inmic", "yes", "-lm", "TAR2860/2860.lm", "-dict", "TAR2860/2860.dic"])