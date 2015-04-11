#!/usr/bin/env python2
import subprocess

subprocess.call(["pocketsphinx_continuous", "-inmic", "yes", "-lm", "TAR2860/2860.lm", "-dict", "TAR2860/2860.dic"])
